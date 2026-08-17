"""场景分析器：让 vision 模型为照片建立「场景卡片」

拾景方法学要求先阅读照片——辨认核心主体、空间关系、色彩、动势
与情绪余韵，再据此编译定制生成提示词。

若用户配置的模型不具备视觉能力（如纯图像生成模型），分析会失败，
此时返回「盲卡」：由编译器使用通用引导语完成创作，功能不中断。
"""

import json
import re

import requests

from api_handler import encode_image_to_base64, get_image_mime_type

ANALYSIS_PROMPT = """阅读这张照片，仅输出一个 JSON 对象，不要输出其他任何文字。字段如下：
{
  "core_subjects": "1-2 个让场景可辨识的核心主体",
  "supporting_elements": "2-3 个建立地点或氛围的次要元素",
  "spatial_invariants": "必须保留的空间关系：地平线、相对位置、朝向、路径、剪影、重叠",
  "dominant_gesture": "最强的动势：水平/垂直/对角/曲线/汇聚/视线/运动",
  "visual_weight": "视觉重量分布：面积、明暗、饱和、面孔、孤立、边缘张力",
  "color_atmosphere": "原生色彩氛围：主色相家族、冷暖、明度范围、现有高饱和区域",
  "source_shapes": "1-2 个可同时成为插画与色彩结构的形状候选：剪影、平面、阴影、路径、建筑节奏",
  "quiet_areas": "自然安静区域：天空、水面、墙面、地面、雾、低信息区域",
  "mood": "剥离事实描述后留下的情绪余韵",
  "micro_text_suggestion": "一句命名场景情绪的短语：不超过 5 个英文单词，或不超过 8 个汉字",
  "proposition": "一句表达命题：这件作品想让观看者感受、注意或重新思考什么",
  "tension": "一个中心张力：亲昵/距离、庇护/禁锢、移动/静止、渺小/辽阔、温暖/寒冷、记忆/消失等",
  "metaphor": "一个源自照片的视觉隐喻：某物承载某种含义"
}
字段值使用简体中文。"""

# 无法分析时的占位卡片：编译器会用通用引导语兜底
BLIND_CARD = {
    "core_subjects": "照片中的核心主体",
    "supporting_elements": "照片中建立地点与氛围的次要元素",
    "spatial_invariants": "照片中真实存在的主体位置与空间关系",
    "dominant_gesture": "照片中最强的主导动势",
    "visual_weight": "照片中的视觉重量分布",
    "color_atmosphere": "照片原有的色彩氛围",
    "source_shapes": "从照片中提取的轮廓或形状",
    "quiet_areas": "照片中的安静区域",
    "mood": "照片留下的情绪余韵",
    "micro_text_suggestion": "",
    "proposition": "从照片的情绪余韵中提炼的表达命题",
    "tension": "从照片中自然浮现的中心张力",
    "metaphor": "从照片中提取的视觉隐喻",
}


def _extract_json(content):
    """从模型回复中提取 JSON 对象（容忍 ```json 围栏与多余文字）。"""
    if not content:
        return None
    text = content.strip()
    # 去掉 markdown 围栏
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    # 提取最外层大括号块
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


def analyze_scene(image_path, config):
    """调用 vision 模型建立场景卡片；失败返回 None（由调用方退化盲卡）。

    Args:
        image_path: 照片文件路径
        config: API 配置 {'api_key', 'base_url', 'model'}

    Returns:
        dict 场景卡片，或 None
    """
    api_key = config.get('api_key', '')
    base_url = config.get('base_url', '').rstrip('/')
    model = config.get('model', '')

    if not api_key or not base_url or not model:
        return None

    try:
        base64_image = encode_image_to_base64(image_path)
        mime_type = get_image_mime_type(image_path)

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
                        {'type': 'text', 'text': ANALYSIS_PROMPT},
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:{mime_type};base64,{base64_image}'
                            },
                        },
                    ],
                }
            ],
            'max_tokens': 1500,
            'temperature': 0.3,
        }

        response = requests.post(
            f'{base_url}/chat/completions',
            headers=headers,
            json=payload,
            timeout=90,
        )
        response.raise_for_status()

        content = response.json()['choices'][0]['message']['content']
        card = _extract_json(content)
        if not card:
            return None

        # 只保留已知字段，避免脏数据扩散
        known = set(BLIND_CARD.keys())
        cleaned = {k: str(v).strip() for k, v in card.items() if k in known and str(v).strip()}
        if not cleaned:
            return None
        return cleaned
    except Exception:
        return None