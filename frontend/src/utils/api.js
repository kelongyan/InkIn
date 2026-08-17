import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 200000,  // 200 秒，匹配后端最长超时时间（180s）+ 缓冲
})

// 获取配置
export async function getConfig() {
  const res = await api.get('/config')
  return res.data
}

// 保存配置
export async function saveConfig(config) {
  const res = await api.post('/config', config)
  return res.data
}

// 上传图片
export async function uploadImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

// 获取创作风格列表
export async function getStyles() {
  const res = await api.get('/styles')
  return res.data
}

// 生成作品（style 缺省 'comic' 保持旧行为；params 为风格参数）
export async function generateComic(filename, style = 'comic', params = {}) {
  const res = await api.post('/generate', { filename, style, params })
  return res.data
}
