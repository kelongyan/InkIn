# InkIn MVP 开发方案书

> **版本**：v1.0 MVP  
> **目标**：实现基本功能，保证项目可以跑通  
> **原则**：最小可用，快速验证

---

## 🎯 MVP 目标

**一句话描述**：用户上传照片，配置 API，生成漫画，下载结果。

### 核心功能清单

| 功能 | 优先级 | 状态 |
|------|--------|------|
| 图片上传（点击+拖拽） | P0 | ⬜ 未开始 |
| API 配置（Key/URL/Model） | P0 | ⬜ 未开始 |
| 调用大模型 API | P0 | ⬜ 未开始 |
| 显示漫画结果 | P0 | ⬜ 未开始 |
| 下载漫画图片 | P0 | ⬜ 未开始 |
| 错误处理 | P1 | ⬜ 未开始 |
| 加载状态 | P1 | ⬜ 未开始 |

### 技术栈（精简版）

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue 3 + Vite + Axios | 核心框架 |
| 后端 | Flask + Requests | 最小依赖 |
| 样式 | 内联 CSS / 少量自定义 | 先跑通再说 |

---

## 📋 阶段划分

### 阶段一：项目初始化 ⬜

**目标**：搭建项目骨架，确保前后端能独立运行

#### 任务清单

- [ ] 1.1 创建后端目录结构
  ```
  backend/
  ├── app.py
  ├── requirements.txt
  └── config.json
  ```

- [ ] 1.2 创建前端项目
  ```bash
  npm create vite@latest frontend -- --template vue
  ```

- [ ] 1.3 编写后端最小 Flask 应用
  ```python
  from flask import Flask, jsonify
  from flask_cors import CORS
  
  app = Flask(__name__)
  CORS(app)
  
  @app.route('/api/health')
  def health():
      return jsonify({'status': 'ok'})
  
  if __name__ == '__main__':
      app.run(debug=True, port=5000)
  ```

- [ ] 1.4 编写 `requirements.txt`
  ```
  flask==3.0.0
  flask-cors==4.0.0
  requests==2.31.0
  ```

- [ ] 1.5 验证后端启动
  ```bash
  cd backend
  pip install -r requirements.txt
  python app.py
  # 访问 http://localhost:5000/api/health 应返回 {"status": "ok"}
  ```

- [ ] 1.6 验证前端启动
  ```bash
  cd frontend
  npm install
  npm run dev
  # 访问 http://localhost:5173 应看到 Vue 默认页面
  ```

**完成标准**：前后端都能独立启动，无报错

---

### 阶段二：后端核心功能 ⬜

**目标**：实现 API 调用和图片处理的核心逻辑

#### 任务清单

- [ ] 2.1 编写 API 配置管理 `config_manager.py`
  ```python
  # 功能：
  # - 读取 config.json
  # - 保存配置
  # - 获取当前配置
  ```

- [ ] 2.2 编写 API 调用处理 `api_handler.py`
  ```python
  # 功能：
  # - 接收 base64 图片
  # - 构造 OpenAI 格式请求
  # - 调用大模型 API
  # - 解析返回结果
  ```

- [ ] 2.3 实现图片上传接口 `POST /api/upload`
  ```python
  @app.route('/api/upload', methods=['POST'])
  def upload_image():
      # 接收图片文件
      # 保存到 uploads/ 目录
      # 返回图片路径
  ```

- [ ] 2.4 实现配置接口
  ```python
  @app.route('/api/config', methods=['GET'])    # 获取配置
  @app.route('/api/config', methods=['POST'])   # 保存配置
  ```

- [ ] 2.5 实现生成漫画接口 `POST /api/generate`
  ```python
  @app.route('/api/generate', methods=['POST'])
  def generate_comic():
      # 获取图片路径
      # 读取 API 配置
      # 调用大模型 API
      # 返回生成的图片
  ```

- [ ] 2.6 测试后端 API（用 curl 或 Postman）
  ```bash
  # 测试配置保存
  curl -X POST http://localhost:5000/api/config \
    -H "Content-Type: application/json" \
    -d '{"api_key": "test", "base_url": "https://api.openai.com/v1", "model": "gpt-4o"}'
  
  # 测试图片上传
  curl -X POST http://localhost:5000/api/upload \
    -F "file=@test.jpg"
  ```

**完成标准**：所有 API 接口可正常调用，返回正确结果

---

### 阶段三：前端核心功能 ⬜

**目标**：实现图片上传、配置、生成、下载的完整流程

#### 任务清单

- [ ] 3.1 编写图片上传组件 `ImageUploader.vue`
  ```vue
  <!-- 功能：
  - 拖拽上传区域
  - 点击选择文件
  - 图片预览
  - 文件格式/大小校验
  -->
  ```

- [ ] 3.2 编写 API 配置组件 `ApiSettings.vue`
  ```vue
  <!-- 功能：
  - API Key 输入框
  - Base URL 输入框
  - Model ID 输入框
  - 保存按钮
  -->
  ```

- [ ] 3.3 编写结果展示组件 `ResultViewer.vue`
  ```vue
  <!-- 功能：
  - 显示原图
  - 显示漫画结果
  - 下载按钮
  -->
  ```

- [ ] 3.4 编写主组件 `App.vue`
  ```vue
  <!-- 功能：
  - 整合所有子组件
  - 状态管理（图片、配置、结果）
  - 调用后端 API
  -->
  ```

- [ ] 3.5 编写 API 请求工具 `utils/api.js`
  ```javascript
  // 功能：
  // - axios 实例
  // - 上传图片
  // - 获取/保存配置
  // - 生成漫画
  ```

- [ ] 3.6 添加基础样式
  ```css
  /* 简洁风格：
  - 居中布局
  - 圆角卡片
  - 柔和阴影
  - 响应式适配
  */
  ```

**完成标准**：页面可正常显示，所有按钮可点击，能调用后端 API

---

### 阶段四：前后端联调 ⬜

**目标**：打通完整流程，确保端到端可用

#### 任务清单

- [ ] 4.1 配置 Vite 代理
  ```javascript
  // vite.config.js
  export default defineConfig({
    server: {
      proxy: {
        '/api': 'http://localhost:5000'
      }
    }
  })
  ```

- [ ] 4.2 测试完整流程
  ```
  1. 启动后端：python app.py
  2. 启动前端：npm run dev
  3. 打开浏览器：http://localhost:5173
  4. 配置 API Key
  5. 上传一张照片
  6. 点击"生成漫画"
  7. 等待结果
  8. 下载漫画图片
  ```

- [ ] 4.3 修复联调中发现的问题
  - 跨域问题
  - 请求/响应格式问题
  - 错误处理问题

**完成标准**：完整流程跑通，能成功生成漫画

---

### 阶段五：错误处理和优化 ⬜

**目标**：提升用户体验，处理异常情况

#### 任务清单

- [ ] 5.1 后端错误处理
  ```python
  # - API Key 无效
  # - 网络超时
  # - API 返回错误
  # - 图片格式不支持
  ```

- [ ] 5.2 前端错误提示
  ```vue
  <!-- 使用 Element Plus 的 ElMessage -->
  <!-- 显示友好的错误信息 -->
  ```

- [ ] 5.3 加载状态
  ```vue
  <!-- - 上传时显示进度
  - 生成时显示 loading
  - 按钮禁用状态 -->
  ```

- [ ] 5.4 输入校验
  ```vue
  <!-- - API Key 不能为空
  - URL 格式校验
  - 图片格式/大小校验 -->
  ```

**完成标准**：各种异常情况都有友好提示，不会白屏或卡死

---

### 阶段六：启动脚本和文档 ⬜

**目标**：简化启动流程，完善文档

#### 任务清单

- [ ] 6.1 编写 Windows 启动脚本 `start.bat`
  ```bat
  @echo off
  echo Starting InkIn...
  
  echo.
  echo [1/2] Starting Backend...
  cd /d %~dp0backend
  start "InkIn Backend" cmd /k "python app.py"
  
  echo [2/2] Starting Frontend...
  cd /d %~dp0frontend
  start "InkIn Frontend" cmd /k "npm run dev"
  
  echo.
  echo InkIn is starting...
  echo Backend: http://localhost:5000
  echo Frontend: http://localhost:5173
  echo.
  echo Press any key to exit...
  pause > nul
  ```

- [ ] 6.2 编写 Linux/Mac 启动脚本 `start.sh`
  ```bash
  #!/bin/bash
  echo "Starting InkIn..."
  
  # 启动后端
  cd backend
  python app.py &
  BACKEND_PID=$!
  
  # 启动前端
  cd ../frontend
  npm run dev &
  FRONTEND_PID=$!
  
  echo "InkIn is running!"
  echo "Frontend: http://localhost:5173"
  
  # 等待 Ctrl+C
  trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
  wait
  ```

- [ ] 6.3 更新 README 启动说明
  ```markdown
  ## 快速开始
  
  ### Windows
  双击 `start.bat`
  
  ### Linux/Mac
  chmod +x start.sh && ./start.sh
  ```

- [ ] 6.4 编写 API 配置指南 `docs/API_GUIDE.md`
  ```
  如何获取各个平台的 API Key
  ```

**完成标准**：一键启动成功，文档清晰完整

---

## 📊 进度追踪

| 阶段 | 状态 | 开始时间 | 完成时间 | 备注 |
|------|------|----------|----------|------|
| 阶段一：项目初始化 | ⬜ 未开始 | - | - | - |
| 阶段二：后端核心功能 | ⬜ 未开始 | - | - | - |
| 阶段三：前端核心功能 | ⬜ 未开始 | - | - | - |
| 阶段四：前后端联调 | ⬜ 未开始 | - | - | - |
| 阶段五：错误处理和优化 | ⬜ 未开始 | - | - | - |
| 阶段六：启动脚本和文档 | ⬜ 未开始 | - | - | - |

**状态说明**：
- ⬜ 未开始
- 🔄 进行中
- ✅ 已完成
- ❌ 阻塞

---

## 🎯 MVP 完成标准

当以下条件全部满足时，MVP 可以交付：

- [ ] 后端服务可正常启动
- [ ] 前端页面可正常访问
- [ ] API 配置可保存和读取
- [ ] 图片可正常上传
- [ ] 调用大模型 API 成功
- [ ] 漫画结果可正常显示
- [ ] 漫画图片可正常下载
- [ ] 错误情况有友好提示
- [ ] 一键启动脚本可用

---

## 📝 开发注意事项

### 代码规范
- 变量命名：驼峰命名（JS）/ 下划线命名（Python）
- 注释：关键逻辑必须有注释
- 提交信息：使用 `feat:` / `fix:` / `docs:` 前缀

### Git 提交规范
```
feat: 添加新功能
fix: 修复 bug
docs: 更新文档
style: 代码格式调整
refactor: 重构
test: 添加测试
chore: 构建/工具变动
```

### 测试策略
- MVP 阶段：手动测试为主
- 每个阶段完成后进行端到端测试
- 记录发现的问题，及时修复

---

## 🚀 下一步（MVP 之后）

MVP 完成后的迭代方向：

1. **v1.1**：多风格预设
2. **v1.2**：历史记录
3. **v1.3**：参数调节
4. **v1.4**：批量处理
5. **v2.0**：Docker 部署

---

*文档版本：v1.0*  
*创建日期：2024-01-XX*  
*最后更新：2024-01-XX*
