import base64
import requests


def encode_image_to_base64(image_path):
    """将图片文件编码为 base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def get_image_mime_type(image_path):
    """根据文件扩展名获取 MIME 类型"""
    ext = image_path.lower().rsplit('.', 1)[-1] if '.' in image_path else ''
    mime_map = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp',
    }
    return mime_map.get(ext, 'image/jpeg')


def generate_comic(image_path, config):
    """
    调用大模型 API 生成漫画风格图片

    Args:
        image_path: 图片文件路径
        config: API 配置 {'api_key', 'base_url', 'model'}

    Returns:
        dict: {'success': True, 'image_url': '...'} 或 {'success': False, 'error': '...'}
    """
    api_key = config.get('api_key', '')
    base_url = config.get('base_url', '').rstrip('/')
    model = config.get('model', '')

    if not api_key:
        return {'success': False, 'error': 'API Key 未配置'}

    # 编码图片
    base64_image = encode_image_to_base64(image_path)
    mime_type = get_image_mime_type(image_path)

    # 构造请求
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    payload = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': '请将这张照片转换为卡通漫画风格，保持主要特征和构图，使用鲜艳的色彩和清晰的线条。直接输出图片，不要文字描述。'
                    },
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:{mime_type};base64,{base64_image}'
                        }
                    }
                ]
            }
        ],
        'max_tokens': 4096,
    }

    # 调用 API
    try:
        url = f'{base_url}/chat/completions'
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        content = result['choices'][0]['message']['content']

        # 尝试从返回内容中提取图片 URL
        # 有些模型会直接返回图片 URL，有些会返回 base64
        if content.startswith('http'):
            return {'success': True, 'image_url': content}
        elif content.startswith('data:image'):
            return {'success': True, 'image_url': content}
        else:
            # 可能是文字描述或包含 markdown 图片链接
            import re
            url_match = re.search(r'!\[.*?\]\((.*?)\)', content)
            if url_match:
                return {'success': True, 'image_url': url_match.group(1)}
            # 如果没有图片，返回原始内容供前端处理
            return {'success': True, 'image_url': None, 'content': content}

    except requests.exceptions.Timeout:
        return {'success': False, 'error': '请求超时，请稍后重试'}
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status == 401:
            return {'success': False, 'error': 'API Key 无效'}
        elif status == 429:
            return {'success': False, 'error': '请求过于频繁，请稍后重试'}
        else:
            try:
                err_msg = e.response.json().get('error', {}).get('message', str(e))
            except Exception:
                err_msg = str(e)
            return {'success': False, 'error': f'API 错误 ({status}): {err_msg}'}
    except Exception as e:
        return {'success': False, 'error': f'请求失败: {str(e)}'}
