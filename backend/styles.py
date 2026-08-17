"""拾景（Gathered Scenes）风格注册表

InkIn 内置创作风格元数据：展示信息、生成引擎、画幅与可调参数。

「拾景」家族先阅读照片中的场景关系（主体、空间、色彩、情绪），
再选择保留真实现场（实景拼贴），或把现场蒸馏为新的纸上作品（影像蒸馏）。
"""

# ---------------------------------------------------------------------------
# 画幅
# ---------------------------------------------------------------------------

# OpenAI Images API 支持的输出尺寸（宽 x 高）。
# 注意：API 没有精确的 3:4 尺寸，竖版 3:4 请求映射到最接近的 2:3 (1024x1536)。
RATIO_SIZES = {
    "1:1": (1024, 1024),
    "3:4": (1024, 1536),
    "4:3": (1536, 1024),
    "3:5": (1024, 1792),
    "5:3": (1792, 1024),
}

# 「auto」画幅按风格各自的方向规则
AUTO_ORIENTATION = {
    "zine-gathered": {"portrait": "3:5", "landscape": "5:3", "square": "1:1"},
    "zine-distill": {"portrait": "3:5", "landscape": "5:3", "square": "3:5"},
    "morandi-cinema": {"portrait": "3:4", "landscape": "5:3", "square": "1:1"},
}

DEFAULT_AUTO = {"portrait": "3:5", "landscape": "5:3", "square": "1:1"}


def probe_orientation(image_path):
    """读取图片方向，返回 portrait / landscape / square；失败返回 None。"""
    try:
        from PIL import Image
        with Image.open(image_path) as im:
            w, h = im.size
    except Exception:
        return None
    if w == h:
        return "square"
    return "landscape" if w > h else "portrait"


def resolve_size(style_id, ratio, image_path=None):
    """把比例解析为 (width, height) 像素。

    - 明确比例按最近支持尺寸映射；
    - 'auto'（缺省）按风格的方向规则 + 原图方向决定；
      无法探测方向时回退竖版 3:5。
    """
    ratio = (ratio or "auto").strip().lower()
    if ratio in RATIO_SIZES:
        return RATIO_SIZES[ratio]

    if ratio != "auto":
        try:
            x, y = (int(p) for p in ratio.split(":", 1))
            if x <= 0 or y <= 0:
                raise ValueError
            key = f"{x}:{y}"
            if key in RATIO_SIZES:
                return RATIO_SIZES[key]
            target = x / y
            best = min(
                RATIO_SIZES.items(),
                key=lambda kv: abs(kv[1][0] / kv[1][1] - target),
            )
            return best[1]
        except (ValueError, AttributeError):
            pass

    auto_map = AUTO_ORIENTATION.get(style_id, DEFAULT_AUTO)
    orientation = probe_orientation(image_path) if image_path else None
    if orientation is None:
        orientation = "portrait"
    if orientation not in auto_map:
        orientation = "portrait"
    return RATIO_SIZES[auto_map[orientation]]


def ratio_text(size):
    """像素尺寸 → 人类可读比例描述，如 'vertical 3:5 (1024x1792)'。"""
    w, h = size
    for key, (rw, rh) in RATIO_SIZES.items():
        if (rw, rh) == (w, h):
            orientation = "vertical" if h > w else ("landscape" if w > h else "square")
            return f"{orientation} {key} ({w}x{h})"
    return f"{w}x{h}"


# ---------------------------------------------------------------------------
# 风格注册表
# ---------------------------------------------------------------------------

STYLE_LIST = [
    {
        "id": "comic",
        "name": "卡通漫画",
        "family": "classic",
        "tagline": "经典入画，鲜艳清晰",
        "description": "InkIn 经典风格：把照片转换为卡通漫画，保持主要特征与构图，鲜艳色彩与清晰线条。",
        "engine": "auto",
        "default_ratio": "1:1",
        "ratios": ["1:1"],
        "needs_analysis": False,
        "params": [],
    },
    {
        "id": "zine-gathered",
        "name": "拾景 · 实景拼贴",
        "family": "shijing",
        "tagline": "真景为锚，插画成场",
        "description": "保留照片中不可替代的现场关系：真实摄影作为锚点，让源自原图的抽象插画、单一高纯度色彩与手撕纤维边缘向纸面延伸。",
        "engine": "auto",
        "default_ratio": "auto",
        "ratios": ["auto", "3:5", "5:3", "1:1"],
        "needs_analysis": True,
        "params": [
            {
                "key": "language",
                "label": "微文字语言",
                "type": "select",
                "options": [
                    {"value": "en", "label": "英文（默认）"},
                    {"value": "zh", "label": "中文"},
                    {"value": "bilingual", "label": "中英双语"},
                ],
                "default": "en",
                "hint": "纸刊角落的安静小字：英文默认 ≤5 词，中文 ≤8 字",
            },
            {
                "key": "text",
                "label": "自定文字（可选）",
                "type": "text",
                "default": "",
                "hint": "留空则由引擎按场景即兴一句",
            },
            {
                "key": "keep",
                "label": "想保留的关系（可选）",
                "type": "text",
                "default": "",
                "hint": "例如：人物与海岸线的距离",
            },
        ],
    },
    {
        "id": "zine-distill",
        "name": "拾景 · 影像蒸馏",
        "family": "shijing",
        "tagline": "事实入墨，情绪成画",
        "description": "不在成品中保留原照片：从照片提取语义核心、情绪张力与视觉隐喻，用纸张、插画、色彩与自由文字创作一件全新的作品。",
        "engine": "auto",
        "default_ratio": "auto",
        "ratios": ["auto", "3:5", "5:3", "1:1"],
        "needs_analysis": True,
        "params": [
            {
                "key": "color_block",
                "label": "单色块模式",
                "type": "switch",
                "default": False,
                "hint": "全图只用纸色 + 中性墨 + 一整块高饱和色场",
            },
            {
                "key": "keep",
                "label": "想表达的方向（可选）",
                "type": "text",
                "default": "",
                "hint": "例如：靠近与错过",
            },
        ],
    },
    {
        "id": "morandi-cinema",
        "name": "拾景 · 电影海报",
        "family": "shijing",
        "tagline": "原片不动，排版成戏",
        "description": "照片原样锁定为银幕，纯靠电影标题字体、排版层级、负空间与选择性遮挡营造电影感，可虚构演职员表，不加任何装饰符号。",
        "engine": "auto",
        "default_ratio": "auto",
        "ratios": ["auto", "3:4", "4:3", "3:5", "5:3", "1:1"],
        "needs_analysis": True,
        "params": [
            {
                "key": "title",
                "label": "电影标题（可选）",
                "type": "text",
                "default": "",
                "hint": "留空则由引擎按场景拟题",
            },
            {
                "key": "ratio",
                "label": "画幅",
                "type": "select",
                "options": [
                    {"value": "auto", "label": "跟随原图"},
                    {"value": "3:4", "label": "3:4 竖版（默认人像）"},
                    {"value": "5:3", "label": "5:3 横版"},
                    {"value": "1:1", "label": "1:1 方形"},
                ],
                "default": "auto",
                "hint": "人像默认 3:4，横图保持原方向",
            },
        ],
    },
]

STYLES = {s["id"]: s for s in STYLE_LIST}


def get_styles():
    """对外输出风格列表（无内部敏感字段，直接可用）。"""
    return STYLE_LIST