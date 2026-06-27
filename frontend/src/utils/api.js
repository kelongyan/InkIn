import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000,
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

// 生成漫画
export async function generateComic(filename) {
  const res = await api.post('/generate', { filename })
  return res.data
}
