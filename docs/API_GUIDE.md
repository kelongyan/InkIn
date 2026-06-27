# InkIn API 配置指南

> 各平台 API Key 获取方法和配置说明

---

## 📋 通用配置项

| 配置项 | 说明 | 示例 |
|--------|------|------|
| **API Key** | 你的 API 密钥 | `sk-xxxxx` |
| **Base URL** | API 接口地址 | `https://api.openai.com/v1` |
| **Model ID** | 模型名称 | `gpt-4o` |

---

## 🤖 OpenAI

**获取 API Key：**
1. 访问 [platform.openai.com](https://platform.openai.com)
2. 登录 → API Keys → Create new secret key
3. 复制保存（只显示一次）

**配置：**
```
API Key:  sk-xxxxxxxxxxxxxxxxxxxx
Base URL: https://api.openai.com/v1
Model:    gpt-4o
```

**费用：** 按量付费，GPT-4o 约 $0.01-0.03/张

---

## 🫘 豆包（字节跳动）

**获取 API Key：**
1. 访问 [console.volcengine.com/ark](https://console.volcengine.com/ark)
2. 开通模型服务 → 创建 API Key
3. 创建推理接入点（获得 endpoint ID）

**配置：**
```
API Key:  ep-xxxxxxxxxxxxxxxxxxxx
Base URL: https://ark.cn-beijing.volces.com/api/v3
Model:    ep-xxxxxxxxxxxx（你的接入点 ID）
```

**费用：** 新用户有免费额度

---

## ☁️ 通义千问（阿里云）

**获取 API Key：**
1. 访问 [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com)
2. 开通服务 → API-KEY 管理 → 创建新的 API-KEY

**配置：**
```
API Key:  sk-xxxxxxxxxxxxxxxxxxxx
Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1
Model:    qwen-vl-max
```

**费用：** 有免费额度，超出后按量付费

---

## 🧠 智谱 AI

**获取 API Key：**
1. 访问 [open.bigmodel.cn](https://open.bigmodel.cn)
2. 注册登录 → API Keys → 创建

**配置：**
```
API Key:  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Base URL: https://open.bigmodel.cn/api/paas/v4
Model:    glm-4v
```

**费用：** 新用户有免费 Token

---

## 🔥 DeepSeek

**获取 API Key：**
1. 访问 [platform.deepseek.com](https://platform.deepseek.com)
2. 注册登录 → API Keys → 创建

**配置：**
```
API Key:  sk-xxxxxxxxxxxxxxxxxxxx
Base URL: https://api.deepseek.com/v1
Model:    deepseek-chat
```

---

## 🌐 其他兼容平台

InkIn 支持所有 OpenAI 格式的 API，包括但不限于：

- **Moonshot (月之暗面)**：`https://api.moonshot.cn/v1`
- **零一万物**：`https://api.lingyiwanwu.com/v1`
- **百川智能**：`https://api.baichuan-ai.com/v1`
- **MiniMax**：`https://api.minimax.chat/v1`

配置方式统一为：
```
API Key:  平台提供的密钥
Base URL: 平台的 API 地址
Model:    平台支持的模型名称
```

---

## ⚠️ 注意事项

1. **API Key 安全**：不要泄露给他人，不要提交到 Git
2. **图片生成**：部分模型不支持图片输出，建议选择多模态模型
3. **超时时间**：大模型生成较慢，默认超时 120 秒
4. **费用控制**：注意各平台的计费规则，避免意外扣费

---

## 🐛 常见问题

**Q: 提示「API Key 无效」？**
A: 检查 Key 是否正确复制，是否有额外空格

**Q: 提示「请求超时」？**
A: 模型生成图片较慢，稍后重试；或检查网络连接

**Q: 生成的是文字不是图片？**
A: 部分模型不支持图片输出，请更换支持图片生成的多模态模型

**Q: 如何选择模型？**
A: 推荐使用 GPT-4o、通义千问 VL、豆包等多模态模型

---

*文档版本：v1.0*
*最后更新：2026-06-27*
