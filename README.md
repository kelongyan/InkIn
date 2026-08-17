<div align="center">

# 🎨 InkIn · 入画

> 让照片走进艺术的世界 ✨

<p align="center">
  <img src="https://img.shields.io/badge/🎨 InkIn-v1.0-blue" alt="InkIn">
  <img src="https://img.shields.io/badge/⚡ Vue-3-brightgreen" alt="Vue 3">
  <img src="https://img.shields.io/badge/🐍 Flask-3.0-yellow" alt="Flask">
  <img src="https://img.shields.io/badge/🆓 MIT License-orange" alt="MIT License">
</p>

</div>

---

## 🤔 InkIn 是什么？

**InkIn（入画）** 是一个本地运行的 AI 艺术创作工作台。

你拍下一张普通照片，InkIn 为它选择一条创作路径——是保留现场的真实，还是把情绪蒸馏成一张全新的作品：

- 📸 上传一张照片
- 🪄 选择一种画法
- 🎭 作品在画廊中显影

**照片提供事实，创作决定如何留下它。**

---

## ✨ 为什么是 InkIn？

| 特性 | 说明 |
|------|------|
| 🖌️ **拾景创作引擎** | 先阅读照片的场景关系，再为每一张照片定制专属提示词，而不是套用固定模板 |
| 🎨 **多种绘画风格** | 卡通漫画、实景拼贴、影像蒸馏、电影海报…… 同一张照片，不同的艺术世界 |
| 🌍 **开放兼容** | 任意 OpenAI 格式的 API 都可以接入，模型由你选择 |
| 🔒 **本地运行** | 照片只保存在你的电脑上，只发送给你配置的 API |
| 🎯 **简单易用** | 拖拽上传 → 选择风格 → 开始入画，三步完成 |
| ⚡ **轻量快速** | Vue 3 + Flask，前后端架构清晰，跑起来飞快 |

---

## 🚀 快速开始

### 一键启动（推荐）

**Windows (PowerShell)：**
```powershell
.\start.ps1
```

**Linux / macOS：**
```bash
./start.sh
```

> 服务后台常驻运行，关闭终端不会中断，日志保存在 `.run/logs/` 目录下。

### 手动启动

**1️⃣ 启动后端**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
🎉 后端跑起来了！访问 http://localhost:5000/api/health

**2️⃣ 启动前端**
```bash
cd frontend
pnpm install
pnpm dev
```
🎉 前端跑起来了！访问 http://localhost:9527

**3️⃣ 配置 API**

打开浏览器，点击右上角齿轮图标，填入你的 API 信息：

- **API Key**：你的密钥
- **Base URL**：API 地址
- **Model ID**：模型名称

**4️⃣ 开始入画！**

拖拽一张照片到艺术工作台，选择一种画法，点击「开始入画」。生成完成后，画廊区会直接显影最终作品，并提供下载按钮。

---

## 🎨 四种画法

| 风格 | 理念 | 效果 |
|------|------|------|
| 🖍️ **卡通漫画** | 经典入画 | 鲜艳色彩与清晰线条，保持照片主要特征与构图 |
| 🪡 **拾景 · 实景拼贴** | 真景为锚，插画成场 | 照片作为真实锚点，抽象插画、单一高纯度色彩与手撕纤维边缘向纸面延伸 |
| 🧪 **拾景 · 影像蒸馏** | 事实入墨，情绪成画 | 照片只作语义参考，提取情绪张力与视觉隐喻，重创为独立成立的原创插画 |
| 🎬 **拾景 · 电影海报** | 原片不动，排版成戏 | 照片原样锁定为银幕，纯靠标题字体、排版层级与负空间营造电影感 |

### 拾景：InkIn 的创作方法学

拾景不把照片当作等待套用的模板，而是先阅读场景——辨认主体、空间、色彩、动作与没有说完的情绪——再决定保留真实现场，或把现场蒸馏成一件新的纸上作品。

1. **阅读**：视觉模型为照片建立「场景卡片」——核心主体、空间关系、色彩氛围、情绪余韵……
2. **定制**：引擎按所选风格的规则，为这一张照片编译专属提示词
3. **生成**：作品在画廊中显影，并附「创作思路」，说明保留了什么、舍弃了什么

每个拾景风格都提供可调参数：微文字语言、想保留的关系、单色块模式、电影标题、画幅……

---

## 📁 项目结构

```
InkIn/
├── backend/                # Flask 后端
│   ├── app.py              # 主应用与路由
│   ├── api_handler.py      # API 调用与响应解析
│   ├── styles.py           # 风格注册表（画幅 / 参数 / 元数据）
│   ├── scene_analyzer.py   # 场景分析器（vision 建卡）
│   ├── prompt_compiler.py  # 提示词编译器（拾景管线）
│   └── zine_engine.py      # 拾景引擎（分析 → 编译 → 生成）
├── frontend/               # Vue 3 前端
│   └── src/
│       ├── App.vue         # 主组件
│       └── components/     # 上传 / 设置 / 风格选择 / 结果展示
├── start.ps1 / start.sh    # 启动脚本
└── stop.ps1  / stop.sh     # 停止脚本
```

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源：

- ✅ 可以商用
- ✅ 可以修改
- ✅ 可以分发
- ✅ 可以私用

---

<p align="center">
  <b>🎨 InkIn · 让照片走进艺术的世界</b>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/kelongyan">kelong</a>
</p>