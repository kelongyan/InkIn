"""拾景引擎：分析 → 编译 → 生成的编排层

拾景（Gathered Scenes）是 InkIn 的创作方法学：先为照片建立场景卡片，
再按所选风格编译定制提示词，最后调用图像生成 API。

旧「卡通漫画」风格不经过本引擎，保持原有调用路径不变。
"""

from api_handler import (
    generate_with_chat_api,
    generate_with_image_api,
    is_image_generation_model,
)
from prompt_compiler import build_prompt
from scene_analyzer import analyze_scene, BLIND_CARD
from styles import STYLES, resolve_size, ratio_text

# 创作思路摘要的字段顺序（按风格编排）
_RATIONALE_MAP = {
    'zine-gathered': {
        'intro': '实景拼贴：保留照片为真实锚点，让抽象插画场、单一结构色与手撕纸边向纸面延伸。',
        'points': [
            ('scene', '主体「{core}」与「{spatial}」作为真实锚点'),
            ('shape', '以「{shape}」为骨架贯穿摄影、插画与色彩'),
            ('color', '结构色与插画共享来源形状，承担平衡与视线引导'),
            ('edge', '照片与纸面以手撕纤维边界交接'),
            ('text', '微文字落于安静纸区'),
        ],
    },
    'zine-distill': {
        'intro': '影像蒸馏：照片只作语义参考，成品为独立成立的原创插画。',
        'points': [
            ('core', '语义核心「{core}」被重新编排'),
            ('proposition', '命题「{prop}」'),
            ('tension', '张力「{tension}」'),
            ('metaphor', '隐喻「{metaphor}」'),
            ('color', '单一高纯度色（或单色块模式）承载情绪事件'),
        ],
    },
    'morandi-cinema': {
        'intro': '电影海报：照片原样锁定，纯排版营造电影感。',
        'points': [
            ('core', '主角「{core}」保持原样'),
            ('layout', '标题与演职员表依「{gesture}」与安静区排布'),
            ('title', '标题「{title}」为唯一主导字声部'),
            ('text', '虚构信息保持原创且内部自洽'),
        ],
    },
}


def _pick(card, key, fallback=''):
    value = (card or {}).get(key)
    if value and str(value).strip():
        return str(value).strip()
    return fallback


def _short(text, limit=60):
    text = (text or '').strip()
    return text if len(text) <= limit else text[:limit] + '…'


def build_rationale(style_id, card, params, size, title=''):
    """编译一句创作思路摘要（输出格式参考 SKILL 的「创作思路」）。"""
    spec = _RATIONALE_MAP.get(style_id)
    if not spec:
        return ''
    card = card or {}
    params = params or {}

    core = _short(_pick(card, 'core_subjects', '照片主体'))
    spatial = _short(_pick(card, 'spatial_invariants', '现场关系'))
    shape = _short(_pick(card, 'source_shapes', '来源形状'))
    gesture = _short(_pick(card, 'dominant_gesture', '主导动势'))
    prop = _short(_pick(card, 'proposition', '表达命题'))
    tension = _short(_pick(card, 'tension', '中心张力'))
    metaphor = _short(_pick(card, 'metaphor', '视觉隐喻'))
    if not title:
        title = _short(params.get('title') or '', 30) or '场景拟题'

    values = {
        'core': core, 'spatial': spatial, 'shape': shape,
        'gesture': gesture, 'prop': prop, 'tension': tension,
        'metaphor': metaphor, 'title': title,
    }

    points = []
    for _, tmpl in spec['points']:
        line = tmpl.format(**values)
        if line:
            points.append('· ' + line)

    head = f"{spec['intro']}（{ratio_text(size)}）"
    body = '；'.join(points)
    return f'{head} {body}' if body else head


def zine_generate(image_path, config, style_id, params=None):
    """执行一条拾景管线。

    Args:
        image_path: 照片文件路径
        config: API 配置 {'api_key', 'base_url', 'model'}
        style_id: 风格 id（styles.py 中 family='shijing' 的风格）
        params: 用户参数 dict

    Returns:
        dict: {'success': True, 'image_url': ..., 'rationale': ..., 'style': ...}
              或 {'success': False, 'error': ...}
    """
    style = STYLES.get(style_id)
    if not style:
        return {'success': False, 'error': f'未知风格: {style_id}'}

    params = params or {}
    model = config.get('model', '')

    # 1. 分析：建立场景卡片；失败时退化为盲卡
    card = None
    if style.get('needs_analysis'):
        card = analyze_scene(image_path, config)
    if not card:
        card = BLIND_CARD

    # 2. 编译：确定画幅与提示词
    ratio = (params.get('ratio') or style.get('default_ratio') or 'auto').strip()
    size = resolve_size(style_id, ratio, image_path)

    # 用户自定义的「保留关系/表达方向」统一走 keep 参数
    keep_override = (params.get('keep') or '').strip()

    try:
        prompt = build_prompt(style_id, card, params, size, keep_override)
    except ValueError as e:
        return {'success': False, 'error': str(e)}

    # 3. 生成：按模型能力路由到对应 API 路径
    if is_image_generation_model(model):
        result = generate_with_image_api(image_path, config, prompt, size=size)
    else:
        result = generate_with_chat_api(image_path, config, prompt)

    if not result['success']:
        return result

    title = (params.get('title') or '').strip()
    result['rationale'] = build_rationale(style_id, card, params, size, title)
    result['style'] = {
        'id': style_id,
        'name': style['name'],
        'tagline': style['tagline'],
    }
    return result