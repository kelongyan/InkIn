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

| 风格 | 效果 |
|------|------|
| 🇯🇵 日系动漫 | 大眼睛、精致线条、二次元老婆/老公 |
| 🇺🇸 美式漫画 | 粗线条、高对比度、超级英雄风 |
| 🎨 水彩画 | 柔和色彩、晕染效果、文艺范儿 |
| 🖼️ 油画 | 厚涂笔触、丰富质感、艺术气息 |
| 👾 像素风 | 复古游戏感、8-bit 魅力 |
| 🌃 赛博朋克 | 霓虹灯、未来感、科技风 |
| 🏯 水墨画 | 黑白为主、写意、东方美学 |

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
