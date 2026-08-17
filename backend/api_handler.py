import base64
import os
import re
import requests

from app_config import config


# 图像生成模型列表（使用 /v1/images/generations 端点）
IMAGE_GENERATION_MODELS = {
    'gpt-image-1', 'gpt-image-2',
    'dall-e-2', 'dall-e-3',
    'stable-diffusion', 'midjourney',
}


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


def is_image_generation_model(model):
    """判断是否为图像生成模型"""
    model_lower = model.lower()
    return any(m in model_lower for m in IMAGE_GENERATION_MODELS)


def generate_with_image_api(image_path, config, style_prompt, size=(1024, 1024)):
    """
    使用图像生成 API（/v1/images/generations）生成图片
    适用于 gpt-image-2、dall-e-3 等模型

    Args:
        image_path: 图片文件路径
        config: API 配置
        style_prompt: 生成提示词
        size: (width, height) 输出尺寸，部分平台不支持非 1024 尺寸时自动回退
    """
    api_key = config.get('api_key', '')
    base_url = config.get('base_url', '').rstrip('/')
    model = config.get('model', '')

    size_str = f'{size[0]}x{size[1]}'

    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    try:
        # 尝试 images/edits 端点（支持图片编辑，需要 multipart/form-data）
        url = f'{base_url}/images/edits'
        mime_type = get_image_mime_type(image_path)

        with open(image_path, 'rb') as f:
            files = {
                'image': (os.path.basename(image_path), f, mime_type),
            }
            data = {
                'model': model,
                'prompt': style_prompt,
                'n': '1',
                'size': size_str,
            }
            response = requests.post(url, headers=headers, files=files, data=data, timeout=config.API_TIMEOUT_LONG)

        # 如果 edits 端点不可用，回退到 generations 端点
        if response.status_code in (404, 405):
            headers['Content-Type'] = 'application/json'
            payload = {
                'model': model,
                'prompt': style_prompt,
                'n': 1,
                'size': size_str,
            }
            url = f'{base_url}/images/generations'
            response = requests.post(url, headers=headers, json=payload, timeout=config.API_TIMEOUT_LONG)

        # 部分平台不支持自定义尺寸（如仅 1024x1024），回退重试一次
        if response.status_code in (400, 422) and size_str != '1024x1024':
            if '/images/edits' in url:
                url = f'{base_url}/images/generations'
            headers['Content-Type'] = 'application/json'
            payload = {
                'model': model,
                'prompt': style_prompt,
                'n': 1,
                'size': '1024x1024',
            }
            response = requests.post(url, headers=headers, json=payload, timeout=config.API_TIMEOUT_LONG)

        response.raise_for_status()
        result = response.json()

        # 解析返回的图片数据
        if 'data' in result and len(result['data']) > 0:
            item = result['data'][0]
            if 'b64_json' in item:
                return {'success': True, 'image_url': f'data:image/png;base64,{item["b64_json"]}'}
            elif 'url' in item:
                return {'success': True, 'image_url': item['url']}

        return {'success': False, 'error': 'API 未返回有效图片'}

    except requests.exceptions.Timeout:
        return {'success': False, 'error': '请求超时，请稍后重试'}
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        try:
            err_msg = e.response.json().get('error', {}).get('message', str(e))
        except Exception:
            err_msg = str(e)

        if status == 401:
            return {'success': False, 'error': 'API Key 无效'}
        elif status == 429:
            return {'success': False, 'error': '请求过于频繁，请稍后重试'}
        return {'success': False, 'error': f'API 错误 ({status}): {err_msg}'}
    except Exception as e:
        return {'success': False, 'error': f'请求失败: {str(e)}'}


def generate_with_chat_api(image_path, config, prompt=None):
    """
    使用 Chat Completions API（/v1/chat/completions）生成图片
    适用于支持 vision 的模型（如 gpt-4o、qwen-vl 等）

    Args:
        image_path: 图片文件路径
        config: API 配置
        prompt: 生成提示词；缺省使用经典卡通漫画提示词（保持旧行为）
    """
    api_key = config.get('api_key', '')
    base_url = config.get('base_url', '').rstrip('/')
    model = config.get('model', '')

    # 编码图片
    base64_image = encode_image_to_base64(image_path)
    mime_type = get_image_mime_type(image_path)

    if not prompt:
        prompt = '请将这张照片转换为卡通漫画风格，保持主要特征和构图，使用鲜艳的色彩和清晰的线条。直接输出图片，不要文字描述。'

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
                        'text': prompt
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

    try:
        url = f'{base_url}/chat/completions'
        response = requests.post(url, headers=headers, json=payload, timeout=config.API_TIMEOUT_MEDIUM)
        response.raise_for_status()

        result = response.json()
        content = result['choices'][0]['message']['content']

        # 提取图片 URL
        if content.startswith('http'):
            return {'success': True, 'image_url': content}
        elif content.startswith('data:image'):
            return {'success': True, 'image_url': content}
        else:
            url_match = re.search(r'!\[.*?\]\((.*?)\)', content)
            if url_match:
                return {'success': True, 'image_url': url_match.group(1)}
            return {'success': True, 'image_url': None, 'content': content}

    except requests.exceptions.Timeout:
        return {'success': False, 'error': '请求超时，请稍后重试'}
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        try:
            err_msg = e.response.json().get('error', {}).get('message', str(e))
        except Exception:
            err_msg = str(e)

        if status == 401:
            return {'success': False, 'error': 'API Key 无效'}
        elif status == 429:
            return {'success': False, 'error': '请求过于频繁，请稍后重试'}
        return {'success': False, 'error': f'API 错误 ({status}): {err_msg}'}
    except Exception as e:
        return {'success': False, 'error': f'请求失败: {str(e)}'}


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
    model = config.get('model', '')

    if not api_key:
        return {'success': False, 'error': 'API Key 未配置'}

    # 根据模型类型选择 API 端点
    if is_image_generation_model(model):
        style_prompt = '将这张照片转换为卡通漫画风格，保持主要特征和构图，使用鲜艳的色彩和清晰的线条'
        return generate_with_image_api(image_path, config, style_prompt)
    else:
        return generate_with_chat_api(image_path, config)
