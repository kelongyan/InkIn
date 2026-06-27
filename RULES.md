# InkIn 开发规范

> 开发前必读，违反规范的 PR 不予合并

---

## 📌 阶段同步规则（强制）

**每完成一个阶段，必须执行以下操作：**

1. **更新文档状态**
   - 修改 `docs/MVP_DEV_PLAN.md` 中对应阶段的任务清单（`[ ]` → `[x]`）
   - 更新进度追踪表的状态、完成时间
   - 记录本阶段的备注（遇到的问题、技术决策等）

2. **本地验证**
   - 后端：确保 `python app.py` 可正常启动
   - 前端：确保 `pnpm dev` 可正常启动
   - 功能：手动测试本阶段新增功能

3. **提交代码**
   ```bash
   git add .
   git commit -m "feat: 完成阶段X - 阶段名称"
   ```

4. **推送到 GitHub**
   ```bash
   git push origin main
   ```

5. **确认 GitHub 状态**
   - 检查推送是否成功
   - 确认文档在 GitHub 上显示正确

---

## 🐍 当前 Python 环境

| 项目 | 值 |
|------|-----|
| Python 版本 | 3.13.11 |
| 包管理器 | pip 25.3 |
| 环境类型 | Anaconda（全局） |

### 项目直接依赖

| 包 | 版本 | 用途 |
|----|------|------|
| Flask | 3.0.0 | Web 框架 |
| Flask-Cors | 4.0.0 | 跨域支持 |
| requests | 2.31.0 | HTTP 请求 |
| Pillow | 12.1.0 | 图片处理（预留） |
| python-dotenv | 1.1.0 | 环境变量管理（预留） |

### 常用工具包（已安装）

| 包 | 版本 | 用途 |
|----|------|------|
| openai | 2.15.0 | OpenAI SDK |
| opencv-python | 4.13.0.90 | 图像处理 |
| numpy | 2.4.1 | 数值计算 |
| pandas | 3.0.1 | 数据处理 |
| torch | 2.9.1 | PyTorch 深度学习 |
| pytest | 9.0.2 | 测试框架 |
| httpx | 0.28.1 | 异步 HTTP 客户端 |
| pydantic | 2.12.4 | 数据校验 |
| rich | 14.2.0 | 终端美化输出 |

> ⚠️ 以上为全局 Anaconda 环境快照（2026-06-27），非项目虚拟环境。

---

## 🔧 技术规范

### 包管理器

| 场景 | 工具 | 命令 |
|------|------|------|
| 前端依赖安装 | pnpm | `pnpm add <package>` |
| 前端开发依赖 | pnpm | `pnpm add -D <package>` |
| 前端启动 | pnpm | `pnpm dev` |
| 前端构建 | pnpm | `pnpm build` |
| 后端依赖 | pip | `pip install -r requirements.txt` |

**禁止混用**：不要使用 npm、yarn，统一 pnpm

### 前端规范

- **框架**：Vue 3 Composition API（`<script setup>`）
- **UI 库**：Element Plus
- **HTTP 客户端**：Axios
- **样式**：Scoped CSS + Element Plus 主题
- **端口**：开发服务器 3000

```vue
<!-- 标准组件模板 -->
<script setup>
import { ref } from 'vue'
</script>

<template>
  <div class="component-name">
    <!-- 内容 -->
  </div>
</template>

<style scoped>
.component-name {
  /* 样式 */
}
</style>
```

### 后端规范

- **框架**：Flask
- **端口**：5000
- **API 格式**：RESTful JSON
- **跨域**：Flask-CORS

```python
# 标准路由模板
@app.route('/api/xxx', methods=['POST'])
def xxx():
    try:
        # 业务逻辑
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
```

### 目录结构

```
backend/
├── app.py              # 主入口，路由注册
├── config_manager.py   # 配置管理
├── api_handler.py      # API 调用处理
├── requirements.txt    # Python 依赖
├── config.json         # 用户配置（gitignore）
└── uploads/            # 上传目录

frontend/
├── src/
│   ├── components/     # Vue 组件
│   ├── views/          # 页面视图
│   ├── utils/          # 工具函数
│   │   └── api.js      # API 请求封装
│   ├── App.vue         # 根组件
│   └── main.js         # 入口文件
├── public/
└── vite.config.js      # Vite 配置
```

---

## 📝 Git 提交规范

### 提交信息格式

```
<type>: <description>

[optional body]
[optional footer]
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加图片上传组件` |
| `fix` | 修复 bug | `fix: 解决跨域问题` |
| `docs` | 文档更新 | `docs: 更新 MVP 进度` |
| `style` | 代码格式 | `style: 格式化 App.vue` |
| `refactor` | 重构 | `refactor: 提取 API 请求函数` |
| `test` | 测试 | `test: 添加配置接口测试` |
| `chore` | 构建/工具 | `chore: 更新 .gitignore` |

### 提交粒度

- ✅ 一个功能一个提交
- ✅ 一个 bug 修复一个提交
- ❌ 不要把所有改动放在一个提交
- ❌ 不要提交半成品代码

### 分支策略

- **main**：稳定版本，可直接运行
- **开发**：直接在 main 上开发（MVP 阶段）
- **功能分支**：复杂功能创建 `feat/xxx` 分支

---

## 🧪 测试规范

### 阶段测试

每个阶段完成后必须测试：

1. **后端启动测试**
   ```bash
   cd backend && python app.py
   # 访问 http://localhost:5000/api/health
   ```

2. **前端启动测试**
   ```bash
   cd frontend && pnpm dev
   # 访问 http://localhost:3000
   ```

3. **功能测试**
   - 测试本阶段新增的所有功能
   - 测试边界情况（空输入、大文件等）
   - 测试错误处理

### 测试记录

在提交信息中记录测试结果：
```
feat: 完成阶段二 - 后端核心功能

测试结果：
- POST /api/config 正常保存配置
- POST /api/upload 正常上传图片
- POST /api/generate 正常调用 API
```

---

## 📚 文档规范

### 必须维护的文档

| 文档 | 更新时机 | 负责人 |
|------|----------|--------|
| `docs/MVP_DEV_PLAN.md` | 每个阶段完成后 | 开发者 |
| `README.md` | 功能变更时 | 开发者 |
| `RULES.md` | 规范变更时 | 开发者 |

### 文档更新清单

每个阶段完成后检查：

- [ ] MVP_DEV_PLAN.md 任务清单已勾选
- [ ] MVP_DEV_PLAN.md 进度表已更新
- [ ] README.md 功能列表已更新（如有新功能）
- [ ] 代码注释完整（关键逻辑必须有注释）

---

## 🚫 禁止事项

1. **不要提交敏感信息**
   - API Key、密码、Token
   - `config.json` 已在 `.gitignore` 中

2. **不要提交临时文件**
   - `node_modules/`
   - `__pycache__/`
   - `*.pyc`
   - `dist/`

3. **不要在 main 分支提交无法运行的代码**

4. **不要使用过时的依赖版本**

5. **不要跳过阶段**（按顺序完成 1→2→3→4→5→6）

---

## ✅ 阶段完成检查清单

每个阶段完成后，逐项检查：

```
□ 本阶段所有任务已完成
□ 后端可正常启动（python app.py）
□ 前端可正常启动（pnpm dev）
□ 新增功能手动测试通过
□ MVP_DEV_PLAN.md 已更新
□ 代码已提交（git commit）
□ 代码已推送（git push）
□ GitHub 上确认推送成功
□ README.md 已更新（如有必要）
```

全部勾选后才能进入下一阶段。

---

## 🔄 版本迭代规范

### MVP 完成后

1. 创建版本标签
   ```bash
   git tag -a v0.1.0 -m "MVP 版本发布"
   git push origin v0.1.0
   ```

2. 更新 README 添加版本信息

3. 创建 GitHub Release

### 后续版本

遵循语义化版本：`vX.Y.Z`

- **X**：重大功能更新
- **Y**：新功能添加
- **Z**：Bug 修复

---

*规范版本：v1.0*
*创建日期：2026-06-27*
*最后更新：2026-06-27*
