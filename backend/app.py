import os
import uuid
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from app_config import config
from config_manager import get_config, save_config
from api_handler import generate_comic
from styles import get_styles
from zine_engine import zine_generate

app = Flask(__name__)
CORS(app, origins=config.CORS_ORIGINS)


@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': '接口不存在'}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'success': False, 'error': '请求方法不允许'}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'success': False, 'error': '服务器内部错误'}), 500

# 配置上传目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_old_uploads(max_age_hours=None):
    """清理超过指定时间的上传文件"""
    if max_age_hours is None:
        max_age_hours = config.UPLOAD_MAX_AGE_HOURS

    try:
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600

        for filename in os.listdir(UPLOAD_FOLDER):
            if filename == '.gitkeep':
                continue

            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > max_age_seconds:
                    try:
                        os.remove(filepath)
                        print(f'已清理过期文件: {filename}')
                    except Exception as e:
                        print(f'清理文件失败 {filename}: {e}')
    except Exception as e:
        print(f'清理上传目录失败: {e}')


@app.route('/api/health')
def health():
    """健康检查接口"""
    import sys
    import shutil

    checks = {
        'status': 'ok',
        'message': 'InkIn Backend Running',
        'version': '1.0.2',
        'python_version': f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}',
    }

    # 检查上传目录
    try:
        upload_writable = os.access(UPLOAD_FOLDER, os.W_OK)
        upload_size = sum(
            os.path.getsize(os.path.join(UPLOAD_FOLDER, f))
            for f in os.listdir(UPLOAD_FOLDER)
            if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
        )
        checks['uploads'] = {
            'writable': upload_writable,
            'size_bytes': upload_size,
            'size_mb': round(upload_size / 1024 / 1024, 2),
        }
    except Exception as e:
        checks['uploads'] = {'error': str(e)}

    # 检查磁盘空间
    try:
        disk = shutil.disk_usage(os.path.dirname(__file__))
        checks['disk'] = {
            'free_gb': round(disk.free / 1024 / 1024 / 1024, 2),
            'total_gb': round(disk.total / 1024 / 1024 / 1024, 2),
            'used_percent': round(disk.used / disk.total * 100, 1),
        }
    except Exception as e:
        checks['disk'] = {'error': str(e)}

    # 检查依赖
    try:
        import flask
        import requests
        import PIL
        checks['dependencies'] = {
            'flask': flask.__version__,
            'requests': requests.__version__,
            'pillow': PIL.__version__,
        }
    except Exception as e:
        checks['dependencies'] = {'error': str(e)}

    return jsonify(checks)


@app.route('/api/config', methods=['GET'])
def get_config_route():
    """获取当前配置"""
    config = get_config()
    # 隐藏 API Key 中间部分
    masked = config.copy()
    if masked.get('api_key') and len(masked['api_key']) > 8:
        key = masked['api_key']
        masked['api_key'] = key[:4] + '****' + key[-4:]
    return jsonify({'success': True, 'data': masked})


@app.route('/api/config', methods=['POST'])
def save_config_route():
    """保存配置"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '无效的请求数据'}), 400

    config = save_config(data)
    return jsonify({'success': True, 'data': config})


@app.route('/api/upload', methods=['POST'])
def upload_image():
    """上传图片"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '没有文件'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': '未选择文件'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': '不支持的文件格式'}), 400

    # 每次上传时清理过期文件（异步执行，不阻塞响应）
    cleanup_old_uploads()

    # 生成唯一文件名
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f'{uuid.uuid4().hex}.{ext}'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'data': {
            'filename': filename,
            'url': f'/api/uploads/{filename}'
        }
    })


@app.route('/api/uploads/<filename>')
def serve_upload(filename):
    """提供上传文件访问"""
    # 验证文件名安全性，防止路径遍历攻击
    safe_name = secure_filename(filename)
    if safe_name != filename or not safe_name:
        return jsonify({'success': False, 'error': '非法文件名'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, safe_name)
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': '文件不存在'}), 404

    return send_from_directory(UPLOAD_FOLDER, safe_name)


@app.route('/api/styles', methods=['GET'])
def get_styles_route():
    """获取内置创作风格列表"""
    return jsonify({'success': True, 'data': get_styles()})


@app.route('/api/generate', methods=['POST'])
def generate():
    """生成作品

    请求体:
        filename: 图片文件名
        style: 风格 id（缺省 'comic'，保持旧行为）
        params: 风格参数 dict（画幅、文字、模式开关等）
    """
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({'success': False, 'error': '缺少图片文件名'}), 400

    filename = data['filename']
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': '图片文件不存在'}), 404

    # 获取配置
    config_data = get_config()
    if not config_data.get('api_key'):
        return jsonify({'success': False, 'error': '请先配置 API Key'}), 400

    style_id = data.get('style') or 'comic'
    params = data.get('params') or {}

    # 验证 style 参数
    if not isinstance(style_id, str):
        return jsonify({'success': False, 'error': 'style 必须是字符串'}), 400

    # 验证 params 参数
    if not isinstance(params, dict):
        return jsonify({'success': False, 'error': 'params 必须是对象'}), 400

    # 验证 style 是否存在
    from styles import STYLES
    if style_id not in STYLES and style_id != 'comic':
        return jsonify({'success': False, 'error': f'未知风格: {style_id}'}), 400

    # 旧「卡通漫画」风格保持原有调用路径
    if style_id == 'comic':
        result = generate_comic(filepath, config_data)
    else:
        result = zine_generate(filepath, config_data, style_id, params)

    if result['success']:
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'error': result['error']}), 400


if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
