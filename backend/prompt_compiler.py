"""提示词编译器：把场景卡片 + 用户参数编译为最终生成提示词

拾景各管线的提示词结构：
- 实景拼贴：四段式（画布与注意力几何 / 场景保真 / 插画场·色彩结构·撕纸边·微文字 / 质感与禁止）
- 影像蒸馏：五段式（表达 / 画布 / 蒸馏主体 / 边缘·色彩·文字 / 质感与禁止）+ 照片禁止句
- 电影海报：照片锁定 + 布局原型 + 字体层级 + 虚构信息规则

编译只输出能成为像素的指令，不夹带设计理论说明。
"""

from styles import ratio_text


def _cv(card, key):
    """取卡片字段；空值回退为盲卡引导语。"""
    value = (card or {}).get(key)
    return value.strip() if value and str(value).strip() else None


# ---------------------------------------------------------------------------
# 实景拼贴 · Gathered Scenes
# ---------------------------------------------------------------------------

def _language_clause(lang):
    if lang == 'zh':
        return '中文，不超过 8 个汉字，单行'
    if lang == 'bilingual':
        return '中英双语两行：中文 ≤8 字为主行，英文 ≤5 词为次行，两行语义呼应，一行为主一行为次，绝不双行同权重'
    return '英文，不超过 5 个单词：一个词、关键词序列或极短短语，单行'


def compile_gathered(card, params, size, keep_override):
    """实景拼贴：照片为真实锚点，插画场 + 单一结构色 + 手撕纸边 + 微文字。"""
    core = _cv(card, 'core_subjects') or '照片中的核心主体'
    supporting = _cv(card, 'supporting_elements') or '照片中建立地点与氛围的次要元素'
    invariants = _cv(card, 'spatial_invariants') or '照片中真实存在的主体位置与空间关系'
    gesture = _cv(card, 'dominant_gesture') or '照片中最强的主导动势'
    weight = _cv(card, 'visual_weight') or '照片中的视觉重量分布'
    palette = _cv(card, 'color_atmosphere') or '照片原有的色彩氛围'
    shapes = _cv(card, 'source_shapes') or '从照片中提取的轮廓或形状'
    quiet = _cv(card, 'quiet_areas') or '照片中的安静区域'
    mood = _cv(card, 'mood') or '照片留下的情绪余韵'

    keep = (keep_override or '').strip()
    keep_clause = f' 用户明确要求保留的关系：{keep}。' if keep else ''

    lang = params.get('language') or 'en'
    text = (params.get('text') or '').strip()
    if text:
        text_clause = f'微文字内容严格使用用户提供：「{text}」'
    else:
        suggestion = _cv(card, 'micro_text_suggestion')
        if suggestion:
            text_clause = f'微文字内容：{suggestion}'
        else:
            text_clause = '微文字内容：根据场景情绪即兴一句（{lang_rule}）'.format(
                lang_rule=_language_clause(lang)
            )
    lang_clause = _language_clause(lang)

    return f"""生成一张竖版纸刊海报，画布为{ratio_text(size)}。

【画布与注意力几何】暖米色做旧纸面，平面扫描质感，无相框、无样机边框。照片约 30-50% 画面作为真实锚点，插画场延伸约 45-70% 画面。{weight}决定主次分配：先进入照片锚点，经插画场与结构色过渡，最终停在安静纸面。

【场景保真（照片锚点）】核心主体「{core}」必须以真实摄影质感保留，不允许重绘或卡通化。{invariants}必须清晰可辨。{gesture}是主导动势，留白方向顺应它。{keep_clause}

【插画场、色彩结构、撕纸边界、微文字】
插画场：将「{supporting}」与「{shapes}」转译为大型简化插画场，不描摹照片：压缩密集细节，把树叶、人群、纹理等微观细节合并为少数大形与方向性笔势，省略约 80% 的小描述性细节；插画场内部与周围保留 55-75% 安静纸面；使用一种主导插画文法（剪影/断线轮廓/墨场/重复节奏/剪纸），最多一种辅助文法。
色彩结构：从「{palette}」中选取一个高纯度印刷色（如钴蓝、番茄红、梨绿、柠檬黄、品红），以「{shapes}」之一为形状来源，作为贯穿摄影与插画的结构色，约占画面 6-15%，必须承担平衡、引导视线或衔接摄影与插画的功能；禁止漂浮的装饰色块、角落色块或任意亮点。
撕纸边界：照片与纸面的主要交接处保留清晰可见的手撕纤维边缘：不规则撕口、窄纤维须、暖纸色露出，占照片周长的 35-70%，宽度约为画面短边的 1-4%；禁止干净数码裁剪、贴纸描边、均匀装饰撕边、厚重投影。
微文字：{text_clause}（语言规则：{lang_clause}）。小字置于「{quiet}」等安静纸区，尺寸约为画面高度的 1.5-3.5%，纸张印刷体/手写感，墨色取炭黑、暖灰或结构色的克制回声，保持可读；不做标题、不加装饰线。

【质感与约束】整体情绪：{mood}。纸纤维、印刷墨点、扫描噪点、平光、无 3D 景深。禁止：霓虹、贴图感、商业广告层级、Logo、水印、写实卡通/动漫风格、过度锐化、AI 平滑感、数码字体排版感。"""


# ---------------------------------------------------------------------------
# 影像蒸馏 · Scene Distillation
# ---------------------------------------------------------------------------

def compile_distill(card, params, size, keep_override):
    """影像蒸馏：照片仅作语义参考，成品必须是原创插画作品。"""
    nucleus = _cv(card, 'core_subjects') or '照片的语义核心'
    proposition = _cv(card, 'proposition') or '从照片的情绪余韵中提炼的表达命题'
    tension = _cv(card, 'tension') or '从照片中自然浮现的中心张力'
    metaphor = _cv(card, 'metaphor') or '从照片中提取的视觉隐喻'
    gesture = _cv(card, 'dominant_gesture') or '照片中最强的主导动势'
    palette = _cv(card, 'color_atmosphere') or '照片原有的色彩氛围'
    shapes = _cv(card, 'source_shapes') or '从照片中提取的轮廓或形状'
    mood = _cv(card, 'mood') or '照片留下的情绪余韵'

    keep = (keep_override or '').strip()
    keep_clause = f' 用户指定表达方向：「{keep}」，作品需呼应它。' if keep else ''

    color_block = bool(params.get('color_block'))
    if color_block:
        color_clause = (
            'Color mode: Solid Color-Block Mode. 全图只允许三种颜色类别：'
            '纸色、一套统一的中性墨系统（炭黑/石墨/暖灰/棕黑）用于所有线条与形体、'
            '以及恰好一整块连续的高饱和色场（约画面 3-12%），'
            '色场必须是主体、窗口、门、日、水面、剪影等源自照片的核心形体，'
            '而非装饰矩形；禁止第二块彩色区域、禁止色点/条纹/回声。'
        )
    else:
        color_clause = (
            f'色彩：从「{palette}」中选取一个高纯度印刷色作为唯一强调色'
            '（约占画面 0.8-3%），承担焦点、配重、桥梁或方向提示的功能，'
            '必须通过「移除测试」：删掉它构图与情绪就变弱；禁止第二强调色。'
        )

    return f"""生成一张原创纸刊插画作品，画布为{ratio_text(size)}。

【表达与可见后果】作品命题：{proposition}。中心张力：{tension}。视觉隐喻：{metaphor}。{keep_clause} 作品应通过这些可见形式承载命题：尺度与留白、方向与节奏、边界与边缘、色彩事件、纸张材料、自由文字，而非说明性文案。

【画布与注意力几何】暖米色做旧纸面，平面扫描质感，无相框。留白纸面约占 68-85%，一个主导插画簇约占 12-32%；一个主导形体、一到三个支撑形、一个克制的纹理场。构图遵循「{gesture}」的动势，非对称平衡，留出明确的观看路径与一个未解答的开口（情绪方向明确，但留一处关系不说完）。

【蒸馏主体与创作改写】语义核心「{nucleus}」只作为灵感来源，保留两到四个来源锚点：「{shapes}」。其余现实细节全部舍弃：删掉背景杂物、冗余物体与写实信息。允许改变尺度、比例、朝向，允许合并、重复、拉伸、错位元素，允许把风、水、光、影、雪、运动转译为抽象场与笔痕。使用一种主导插画文法（剪纸形/干印剪影/断线轮廓/节奏场/碎片堆叠/轨道漂移），最多一种辅助文法。

【边缘、色彩与文字】
边缘：从来源几何选择一种主边界处理（手撕纤维边/分层灰阶边/点状溶解/不规则记号边/自然孤立轮廓），边界必须对齐来源的地平线、动势或材料变化；若自然孤立轮廓最合适，允许无任何可见过渡装置。
{color_clause}
文字：文字完全自由——可用任何语言、任何体量、任何排版方式（标题、对白、重复词、散落碎片、超大字、被遮挡的片段等），只要它加深命题、张力或隐喻；若不需要文字则不用；禁止把文字当图片说明。

【质感与禁止】整体情绪：{mood}。纸纤维、干墨、颗粒、剪纸质感、平光、无 3D 景深。禁止：照片像素、写实区域、卡通/动漫、儿童绘本甜腻感、装饰性符号散落、胶带、贴纸、多重亮色、商业广告层级、Logo、水印、霓虹、电影感布光。"""


# ---------------------------------------------------------------------------
# 电影海报 · Morandi Cinematic Poster
# ---------------------------------------------------------------------------

def compile_morandi(card, params, size, keep_override):
    """电影海报：照片原样锁定，纯排版营造电影感。"""
    hero = _cv(card, 'core_subjects') or '照片中的视觉主角'
    gesture = _cv(card, 'dominant_gesture') or '照片中最强的主导动势'
    quiet = _cv(card, 'quiet_areas') or '照片中的安静区域'
    palette = _cv(card, 'color_atmosphere') or '照片原有的色彩氛围'
    mood = _cv(card, 'mood') or '照片留下的情绪余韵'
    supporting = _cv(card, 'supporting_elements') or '照片中的次要元素'

    title = (params.get('title') or '').strip()
    title_clause = (
        f'电影标题严格使用用户提供：「{title}」'
        if title else
        '根据场景拟一个原创标题（1-4 词，易记可读，源自主角「%s」）' % hero
    )
    keep = (keep_override or '').strip()
    keep_clause = f' 用户要求：{keep}。' if keep else ''

    return f"""生成一张电影感海报，画布为{ratio_text(size)}。照片本身必须是最终画面的主体，不得重绘、不得加全局滤镜。

【锁定照片】照片保持原样：构图、人物、建筑、云、窗户、色彩、曝光、对比、锐度、原生噪点与纹理一律不变；允许的最小编辑仅为按目标画幅从低信息边缘（天空、路面、墙面）做最小安全裁切；禁止拉伸、修复、重绘、调色、模糊、老化、加纸纹。

【场景与排版布局】视觉主角「{hero}」与「{supporting}」构成画面；「{gesture}」是主导动势；「{quiet}」是安静纸区，可承载文字。选择一种剧院式布局原型并贯彻到底：底部锚定（主角在上，标题与演职员表稳定下沿）/ 顶部宣言（标题占据天空或墙面）/ 中央徽记（标题与主角以尺度与对齐构成单一焦点）/ 轴线整合（标题顺应地平线、道路、光束或透视轴）/ 边缘缩放（标题部分出画，可读核心保持完整）。禁止四边均布文字：一个主导文字簇、一个支撑簇、一个安静区。{keep_clause}

【字体层级】使用 3-5 级文字层级，相对尺寸（标题=100）：片名 100；副题/作者行 20-32；标语 12-20；氛围信息 8-12；微缩演职员表 5-9。仅一个 L1 元素；相邻层级必须明显区分。标题是唯一主导字体声部，可做 1-3 处源自场景结构（屋脊线、窗节奏、道路、阴影、剪影）的定制字形细节，禁止整体扭曲、金属/霓虹/发光/斜角效果。

【文字内容与虚构规则】{title_clause}。标语：一句 3-10 词的情绪命题。可虚构作者名、制作行、年代码、章节号等，保持内部自洽；禁止使用真实人物、真实工作室、真实奖项、商标化名称；禁止伪造桂冠与评级标记；微缩演职员表仅在画面可承载时使用，置于低细节区，紧凑对齐。

【文字与照片的关系】小字只放在「{quiet}」等局部安静处；标题可跨两个区域但关键字形必须落在安静段；保护面孔、眼睛、关键手势、地标冠部不被遮挡；最多 1-3 处有意的字画穿插；小字全部保持可读。

【质感与禁止】主色调参考「{palette}」与「{mood}」：2-3 色低饱和字色（标题墨色、安静中性、一个克制点缀），纹理只允许出现在大字字形内部且止于字形边缘，禁止全局纸纹。禁止：装饰符号、圆形/矩形/线框、贴纸、胶带、伪造桂冠、非用户提供的真实身份信息、复制著名海报字样、全局效果、剪贴、描边、发光、阴影、斜角、水印。"""


# ---------------------------------------------------------------------------
# 编译入口
# ---------------------------------------------------------------------------

def build_prompt(style_id, card, params, size, keep_override=''):
    """按风格编译最终生成提示词。

    Args:
        style_id: styles.py 中的风格 id
        card: 场景卡片（分析结果或盲卡）
        params: 用户参数 dict
        size: (width, height)
        keep_override: 用户想保留的关系 / 表达方向
    """
    params = params or {}
    if style_id == 'zine-gathered':
        return compile_gathered(card, params, size, keep_override)
    if style_id == 'zine-distill':
        return compile_distill(card, params, size, keep_override)
    if style_id == 'morandi-cinema':
        return compile_morandi(card, params, size, keep_override)
    raise ValueError(f'未知风格: {style_id}')