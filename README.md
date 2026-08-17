# 🎨 InkIn - 入画

> 让照片走进艺术的世界 ✨

<p align="center">
  <img src="https://img.shields.io/badge/🎨 InkIn-v1.0-blue" alt="InkIn">
  <img src="https://img.shields.io/badge/⚡ Vue-3-brightgreen" alt="Vue 3">
  <img src="https://img.shields.io/badge/🐍 Flask-3.0-yellow" alt="Flask">
  <img src="https://img.shields.io/badge/🆓 MIT License-orange" alt="MIT License">
</p>

---

## 🤔 InkIn 是什么？

**InkIn（入画）** 是一个神奇的工具，能把你的照片变成漫画！

想象一下：
- 📸 你拍了一张普通照片
- 🪄 点一下按钮
- 🎭 变成了漫画/动漫/水彩/油画风格

**就像打开了次元壁的大门！**

---

## ✨ 为什么选择 InkIn？

| 特性 | 说明 |
|------|------|
| 🌍 **开放兼容** | 不挑食！豆包、GPT、通义、智谱... 任意 OpenAI 格式的 API 都能用 |
| 🔒 **本地运行** | 你的照片不会上传到奇怪的地方（除了你配置的 API） |
| 🎯 **简单易用** | 拖拽上传 → 点击生成 → 下载漫画，三步搞定 |
| 🖼️ **艺术工作台** | 一页式画廊界面，默认聚焦上传，生成后用显影动画展示作品 |
| 🎨 **多风格** | 日漫、美漫、水彩、油画、赛博朋克... 想变啥变啥 |
| ⚡ **快速开发** | Vue 3 + Flask，代码量少，跑得快 |

---

## 🚀 快速开始

### 方式一：一键启动（推荐）

**Windows (PowerShell)：**
```powershell
.\start.ps1      # 启动
.\stop.ps1       # 停止
```

**Linux / macOS：**
```bash
chmod +x start.sh stop.sh
./start.sh       # 启动
./stop.sh        # 停止
```

> 服务后台常驻运行，关闭终端不会中断。日志保存在 `.run/logs/` 目录下。

### 方式二：手动启动

**1️⃣ 克隆项目**
```bash
git clone https://github.com/kelongyan/InkIn.git
cd InkIn
```

**2️⃣ 启动后端**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
🎉 后端跑起来了！访问 http://localhost:5000/api/health

**3️⃣ 启动前端**
```bash
cd frontend
pnpm install
pnpm dev
```
🎉 前端跑起来了！访问 http://localhost:3000

**4️⃣ 配置 API**

打开浏览器 http://localhost:3000，点击右上角齿轮图标，填入你的 API 信息：

- **API Key**: 你的密钥
- **Base URL**: API 地址（如 `https://api.openai.com/v1`）
- **Model ID**: 模型名称（如 `gpt-4o`）

**5️⃣ 开始入画！**

拖拽一张照片到艺术工作台，点击「开始入画」。生成完成后，画廊区会直接显影最终作品，并提供下载按钮。

---

## 🎯 支持的 API 平台

InkIn 不挑食，只要是 OpenAI 格式的 API 都能用：

| 平台 | Base URL | 模型示例 |
|------|----------|----------|
| 🤖 **OpenAI** | `https://api.openai.com/v1` | gpt-4o |
| 🫘 **豆包** | `https://ark.cn-beijing.volces.com/api/v3` | ep-xxxxx |
| ☁️ **通义千问** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | qwen-vl-max |
| 🧠 **智谱AI** | `https://open.bigmodel.cn/api/paas/v4` | glm-4v |
| 🌐 **其他** | 任意兼容 OpenAI 格式的服务 | - |

---

## 🎨 内置风格预设

| 风格 | 家族 | 效果 |
|------|------|------|
| 🇯🇵 卡通漫画 | 经典 | InkIn 经典风格：鲜艳色彩、清晰线条、保持主要特征与构图 |
| 🪡 拾景 · 实景拼贴 | 拾景 | 保留照片为真实锚点，抽象插画场、单一高纯度结构色与手撕纤维边缘向纸面延伸 |
| 🧪 拾景 · 影像蒸馏 | 拾景 | 照片只作语义参考，提取情绪张力与视觉隐喻，重创为独立成立的原创插画 |
| 🎬 拾景 · 电影海报 | 拾景 | 照片原样锁定为银幕，纯靠电影标题字体、排版层级与负空间营造电影感 |

> **拾景（Gathered Scenes）**：InkIn 内化的创作方法学（参考 Zeejay0 的拾景纸刊 Gathered Scenes Zine Skills）。它不把照片当作等待套用的模板，而是先阅读场景——辨认主体、空间、色彩、动作与没有说完的情绪——再选择保留真实现场，或把现场蒸馏为一件新的纸上作品。**照片提供事实，创作决定如何留下它。**

### 拾景风格的使用

1. 上传照片后，在创作台选择一种风格（默认「卡通漫画」保持原行为）。
2. 拾景风格会先让视觉模型阅读照片、建立「场景卡片」，再按风格规则编译定制提示词——每张照片的提示词都是现场定制的，不是固定模板。
3. 可展开风格参数面板调整细节：微文字语言/自定文字、想保留的关系、单色块模式、电影标题、画幅等。
4. 生成后展示「创作思路」，说明引擎保留了什么、舍弃了什么。

> 提示：拾景风格需要视觉模型（如 gpt-4o、qwen-vl-max）来完成场景分析；若配置的是纯图像生成模型，引擎会自动退化为通用引导，功能不中断。

---

## 📁 项目结构

```
InkIn/
├── 📄 README.md                 # 你在看的这个
├── 📄 start.ps1 / stop.ps1     # Windows 启动/停止
├── 📄 start.sh  / stop.sh      # Linux/Mac 启动/停止
├── 📂 docs/                     # 文档
│   └── PROJECT_PLAN.md          # 详细规划书
├── 📂 backend/                  # 后端（Flask）
│   ├── app.py                   # 主应用
│   ├── api_handler.py           # API 调用
│   ├── styles.py                # 风格注册表（画幅/参数/元数据）
│   ├── scene_analyzer.py        # 场景分析器（vision 建卡）
│   ├── prompt_compiler.py       # 提示词编译器（拾景三条管线）
│   ├── zine_engine.py           # 拾景引擎（分析→编译→生成编排）
│   └── config.json              # 配置文件（gitignore）
└── 📂 frontend/                 # 前端（Vue）
    └── src/
        ├── App.vue              # 主组件
        └── components/          # 各种组件
```

---

## 🛠️ 开发计划

- [x] ✅ 项目规划
- [ ] 🔨 基础搭建（Vue + Flask）
- [ ] 🎯 核心功能（上传 → 生成 → 下载）
- [ ] 🎨 多风格支持
- [ ] 📊 历史记录
- [ ] 🚀 批量处理
- [ ] 🐳 Docker 部署
- [ ] 💻 桌面应用

---

## 🤝 参与贡献

欢迎参与 InkIn 的开发！

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/xxx`
3. 提交更改：`git commit -m 'feat: add xxx'`
4. 推送分支：`git push origin feature/xxx`
5. 提交 Pull Request

---

## 📝 更新日志

### v1.0.0 (2024-xx-xx)
- 🎉 项目初始化
- ✨ 核心功能：照片转漫画
- 🖼️ 一页式艺术工作台：默认聚焦拖拽上传，生成后直接展示最终作品
- 🖌️ 新增 Ink 艺术字标识，统一页面 Logo 和浏览器标签页图标
- 🎨 多风格支持
- 📱 响应式设计

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源。

**翻译成人话就是**：
- ✅ 可以商用
- ✅ 可以修改
- ✅ 可以分发
- ✅ 可以私用
- ❌ 不提供担保

---

## 🙏 致谢

感谢所有大模型 API 提供商，让我们能用上这么棒的 AI 能力！

感谢开源社区，让我们站在巨人的肩膀上！

---

## 📞 联系方式

- 🐛 Issues: [GitHub Issues](https://github.com/kelongyan/InkIn/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/kelongyan/InkIn/discussions)
- 📧 Email: zhaxideler@gmail.com
- 🐙 GitHub: [@kelong](https://github.com/kelongyan)

---

<p align="center">
  <b>🎨 InkIn - 让照片走进艺术的世界</b>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/kelongyan">kelong</a>
</p>
