import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from config_manager import get_config, save_config
from api_handler import generate_comic
from styles import get_styles
from zine_engine import zine_generate

app = Flask(__name__)
CORS(app)


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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'message': 'InkIn Backend Running'})


@app.route('/api/config', methods=['GET'])
def get_config_route():
    """获取当前配置"""
    config = get_config()
    # 隐藏 API Key 中间部分
    masked = config.copy()
    if masked.get('api_key') and len(masked['api_key']) > 8:
        key = masked['api_key']
        masked['api_key_masked'] = key[:4] + '****' + key[-4:]
    return jsonify({'success': True, 'data': config})


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
    return send_from_directory(UPLOAD_FOLDER, filename)


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
    config = get_config()
    if not config.get('api_key'):
        return jsonify({'success': False, 'error': '请先配置 API Key'}), 400

    style_id = data.get('style') or 'comic'
    params = data.get('params') or {}

    # 旧「卡通漫画」风格保持原有调用路径
    if style_id == 'comic':
        result = generate_comic(filepath, config)
    else:
        result = zine_generate(filepath, config, style_id, params)

    if result['success']:
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'error': result['error']}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
