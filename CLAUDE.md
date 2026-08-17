# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**InkIn（入画）** 是一个本地运行的 AI 艺术创作工作台，将普通照片转换为艺术作品。

- **前端**：Vue 3 + Vite + Element Plus（端口 3000/9527）
- **后端**：Flask 3.0 + Python 3.8+（端口 5000）
- **核心特性**：拾景创作引擎——先分析照片场景，再为每张照片定制专属提示词

---

## 常用命令

### 启动服务

**一键启动（推荐，后台常驻）：**
```powershell
.\start.ps1      # Windows PowerShell
./start.sh       # Linux/macOS Bash
```

服务后台运行，关闭终端不影响运行。日志保存在 `.run/logs/`。

**停止服务：**
```powershell
.\stop.ps1       # Windows
./stop.sh        # Linux/macOS
```

**手动启动（开发调试）：**
```bash
# 后端
cd backend
pip install -r requirements.txt
python app.py

# 前端
cd frontend
pnpm install
pnpm dev
```

### 前端开发

```bash
cd frontend
pnpm dev          # 开发服务器（http://localhost:9527）
pnpm build        # 生产构建
pnpm preview      # 预览构建产物
```

### 后端开发

```bash
cd backend
python app.py     # 启动 Flask 服务（http://localhost:5000）
```

**健康检查：**
```bash
curl http://localhost:5000/api/health
```

---

## 架构概览

### 双路径生成架构

InkIn 支持两种生成路径：

1. **直接生成（旧路径）**：`卡通漫画`风格，直接调用 API，无场景分析
2. **拾景管线（新路径）**：`zine-*` 和 `morandi-*` 风格，经过 **分析 → 编译 → 生成** 三阶段

### 后端核心模块

```
backend/
├── app.py                  # Flask 主应用：路由、上传、配置管理
├── api_handler.py          # API 调用封装：支持 OpenAI Chat/Images API
├── styles.py               # 风格注册表：画幅、参数、元数据
├── scene_analyzer.py       # 场景分析器：vision 模型构建场景卡片
├── prompt_compiler.py      # 提示词编译器：将场景卡片编译为风格化 prompt
└── zine_engine.py          # 拾景引擎：编排 analyze → compile → generate
```

### 拾景管线流程

**拾景**（Gathered Scenes）是核心创作方法学：

1. **场景分析** (`scene_analyzer.py`)
   - 调用 vision 模型（如 `gpt-4o`）分析上传的照片
   - 构建「场景卡片」：主体、空间、色彩、情绪、张力等结构化信息
   - 如果分析失败，返回 `BLIND_CARD`（盲卡，兜底继续生成）

2. **提示词编译** (`prompt_compiler.py`)
   - 按所选风格（`zine-gathered`、`zine-distill`、`morandi-cinema`）的规则
   - 将场景卡片 + 用户参数编译为最终 prompt
   - 不同风格有不同的编译策略和模板

3. **图像生成** (`api_handler.py`)
   - 自动检测模型类型（Chat API 或 Images API）
   - Chat API：发送编译后的 prompt
   - Images API：使用 `dall-e-3` 等模型生成

### 前端组件结构

```
frontend/src/
├── App.vue                 # 主布局：工作台 + 画廊双区
└── components/
    ├── ImageUploader.vue   # 上传区：拖拽上传、预览
    ├── StylePicker.vue     # 风格选择器：卡片式风格展示
    ├── ApiSettings.vue     # API 配置：Base URL、Model ID、API Key
    └── ResultViewer.vue    # 结果展示：生成图、创作思路、下载
```

### API 接口契约

#### 核心生成接口

**POST** `/api/generate`

**请求体（multipart/form-data）：**
```json
{
  "image": "<文件>",
  "style": "comic | zine-gathered | zine-distill | morandi-cinema",
  "params": {
    "ratio": "auto | 1:1 | 3:4 | 4:3 | 3:5 | 5:3",
    "micro_text": "微文字内容",
    "relations": "要保留的场景关系",
    "mono_mode": "单色块模式 | 渐变与质感",
    "cinema_title": "电影标题",
    ...
  }
}
```

**响应体：**
```json
{
  "success": true,
  "image_url": "http://...",       // 生成的图片 URL
  "scene_card": {...},              // 场景卡片（仅拾景风格）
  "rationale": "创作思路说明",      // 解释保留/舍弃了什么
  "prompt": "最终 prompt"           // 实际发送的提示词
}
```

#### 其他接口

- `GET /api/health` — 健康检查
- `GET /api/config` — 获取当前 API 配置（API Key 脱敏）
- `POST /api/config` — 保存 API 配置
- `GET /api/styles` — 获取所有风格定义

---

## 风格系统

### 内置风格

| 风格 ID | 名称 | 引擎 | 说明 |
|---------|------|------|------|
| `comic` | 卡通漫画 | 直接生成 | 旧版简单风格，不经过拾景管线 |
| `zine-gathered` | 拾景·实景拼贴 | 拾景管线 | 保留照片为锚点，插画与色彩向纸面延伸 |
| `zine-distill` | 拾景·影像蒸馏 | 拾景管线 | 照片只作语义参考，重创为独立插画 |
| `morandi-cinema` | 拾景·电影海报 | 拾景管线 | 照片不动，纯排版营造电影感 |

### 风格注册（`styles.py`）

每个风格定义包含：

- **展示信息**：`title`、`icon`、`tagline`（卡片展示）
- **引擎类型**：`engine: "direct" | "zine"`
- **画幅规则**：`auto` 时按原图方向选择合适比例
- **可调参数**：每个风格有独立的 `params` 配置

**添加新风格时：**

1. 在 `styles.py` 的 `STYLES` 字典中注册
2. 如果使用拾景管线，在 `prompt_compiler.py` 添加编译规则
3. 在 `zine_engine.py` 的 `_RATIONALE_MAP` 添加创作思路模板

---

## 关键约定

### 安全措施

**文件上传安全**：
- 上传文件名经过 `werkzeug.utils.secure_filename()` 验证，防止路径遍历攻击
- 允许的文件格式：`png, jpg, jpeg, gif, webp`
- 访问上传文件时验证文件名安全性

**文件清理策略**：
- 每次上传时自动清理超过 24 小时的旧文件
- 保留 `.gitkeep` 占位文件
- 防止 `backend/uploads/` 目录无限增长

**API Key 保护**：
- `GET /api/config` 返回的 API Key 已脱敏（`sk-****abcd` 格式）
- 配置保存在 `backend/config.json`（git ignored）

### 画幅处理

- **用户指定比例**：直接使用（映射到最近的 API 支持尺寸）
- **`auto`（默认）**：根据原图方向 + 风格的方向偏好自动选择
- **3:4 竖版**：API 不支持精确 3:4，映射到 2:3 (1024x1536)

### 场景卡片字段

`scene_analyzer.py` 返回的卡片包含：

- `core`：核心主体
- `spatial`：空间信息
- `color_sense`：色彩印象
- `emotion`：情绪基调
- `shape`：视觉骨架（实景拼贴）
- `proposition`、`tension`、`metaphor`：命题、张力、隐喻（影像蒸馏）
- `gesture`：姿态/朝向（电影海报）

**盲卡（`BLIND_CARD`）**：分析失败时的兜底字段，让生成继续进行。

### 配置管理

- 配置保存在 `backend/config.json`（git ignored）
- 前端通过 `/api/config` 读写
- API Key 在返回时中间部分脱敏

---

## 开发注意事项

### 日志系统

**后端日志**：
- 使用 Python `logging` 模块
- 场景分析器已配置详细日志
- 日志级别：INFO
- 查看日志：`.run/logs/backend.log`

**日志类型**：
- 场景分析超时
- HTTP 错误（含状态码）
- JSON 解析失败
- 响应字段缺失
- 未知错误（含异常类型）

### 修改风格或提示词逻辑

- **风格元数据**：修改 `styles.py` 的 `STYLES` 字典
- **编译规则**：修改 `prompt_compiler.py` 的 `build_prompt()` 函数
- **场景分析**：修改 `scene_analyzer.py` 的 system prompt 或字段定义

### API 兼容性

- 后端支持任何 OpenAI 格式的 API（Base URL 可配置）
- 自动检测模型类型：
  - `dall-e-*` → Images API
  - 其他 → Chat API（带 vision）

### 文件上传

- 上传文件保存在 `backend/uploads/`（每次请求生成 UUID 文件名）
- 允许的格式：`png, jpg, jpeg, gif, webp`
- 生成完成后文件仍保留（用户可能需要重新生成）

### 前端状态管理

- 无全局状态库（Vuex/Pinia）
- 组件间通过 props/emit 通信
- API 配置存储在 `localStorage`

---

## 测试与验证

### 后端验证

```bash
# 健康检查
curl http://localhost:5000/api/health

# 获取风格列表
curl http://localhost:5000/api/styles

# 手动测试生成（需要先配置 API）
curl -X POST http://localhost:5000/api/generate \
  -F "image=@test.jpg" \
  -F "style=zine-gathered" \
  -F "params={\"ratio\":\"auto\"}"
```

### 前端验证

1. 打开 `http://localhost:3000`（或 9527）
2. 配置 API（右上角齿轮图标）
3. 上传测试图片
4. 选择风格并生成
5. 检查生成结果和创作思路显示

---

## 故障排查

### 服务启动失败

1. 检查端口占用：`netstat -ano | findstr "5000"` 或 `lsof -i :5000`
2. 查看日志：`.run/logs/backend.log` 和 `frontend.log`
3. 检查 Python/pnpm 是否已安装

### API 调用失败

1. 检查后端控制台日志
2. 确认 API Key 和 Base URL 配置正确
3. 测试 API 连通性：`curl -H "Authorization: Bearer YOUR_KEY" YOUR_BASE_URL/v1/models`

### 生成结果异常

- **返回 BLIND_CARD**：vision 分析失败，检查模型是否支持图像输入
- **prompt 不符合预期**：检查 `prompt_compiler.py` 的编译逻辑
- **生成风格偏差**：可能需要调整 system prompt 或编译模板

---

## 扩展指南

### 添加新的拾景风格

1. **注册风格**（`styles.py`）：
   ```python
   STYLES['my-style'] = {
       'title': '我的风格',
       'engine': 'zine',
       'params': {...},
       ...
   }
   ```

2. **添加编译规则**（`prompt_compiler.py`）：
   ```python
   if style_id == 'my-style':
       # 编写 prompt 构建逻辑
       return compiled_prompt
   ```

3. **添加创作思路模板**（`zine_engine.py`）：
   ```python
   _RATIONALE_MAP['my-style'] = {
       'intro': '...',
       'points': [...]
   }
   ```

### 支持新的 API 提供商

修改 `api_handler.py`：

- 如果 API 完全兼容 OpenAI 格式，无需修改
- 如果有特殊字段或响应格式，扩展 `generate_with_chat_api()` 或 `generate_with_image_api()`

---

## 项目依赖

### 后端

- `flask==3.0.0` — Web 框架
- `flask-cors==4.0.0` — CORS 支持
- `requests==2.31.0` — HTTP 客户端
- `pillow==12.1.0` — 图像处理（探测方向）

### 前端

- `vue==3.5.38` — 响应式框架
- `element-plus==2.14.2` — UI 组件库
- `axios==1.18.1` — HTTP 客户端
- `vite==8.1.0` — 构建工具
