<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import ImageUploader from './components/ImageUploader.vue'
import ApiSettings from './components/ApiSettings.vue'
import ResultViewer from './components/ResultViewer.vue'
import { generateComic } from './utils/api.js'

const uploadedFile = ref(null)
const originalUrl = ref('')
const resultUrl = ref('')
const generating = ref(false)
const uploading = ref(false)

const canGenerate = computed(() => uploadedFile.value && !generating.value && !uploading.value)

function onUploadStart() {
  uploading.value = true
}

function onUploadSuccess(data) {
  uploadedFile.value = data.filename
  originalUrl.value = data.url
  resultUrl.value = ''
  uploading.value = false
}

function onUploadError() {
  uploading.value = false
}

async function handleGenerate() {
  if (!uploadedFile.value) {
    ElMessage.warning('请先上传图片')
    return
  }

  generating.value = true
  resultUrl.value = ''

  try {
    const res = await generateComic(uploadedFile.value)

    if (res.success && res.data) {
      if (res.data.image_url) {
        resultUrl.value = res.data.image_url
        ElMessage.success('漫画生成成功！')
      } else if (res.data.content) {
        ElMessage.info('模型返回了文字描述，请检查模型是否支持图片生成')
      }
    } else {
      ElMessage.error(res.error || '生成失败')
    }
  } catch (err) {
    ElMessage.error('生成失败: ' + (err.message || '网络错误'))
  } finally {
    generating.value = false
  }
}
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1>🎨 InkIn 入画</h1>
      <p>照片变漫画，一键生成</p>
    </header>

    <main class="app-main">
      <el-row :gutter="24">
        <el-col :xs="24" :sm="24" :md="10" :lg="8">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <span>⚙️ API 配置</span>
            </template>
            <ApiSettings />
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="24" :md="14" :lg="16">
          <el-card class="upload-card" shadow="hover">
            <template #header>
              <span>📷 上传图片</span>
            </template>
            <ImageUploader @upload-start="onUploadStart" @upload-success="onUploadSuccess" @upload-error="onUploadError" />
            <el-button
              type="primary"
              size="large"
              :loading="generating"
              :disabled="!canGenerate"
              @click="handleGenerate"
              style="width: 100%; margin-top: 16px"
            >
              {{ generating ? '生成中...' : '✨ 生成漫画' }}
            </el-button>
          </el-card>

          <el-card class="result-card" shadow="hover" style="margin-top: 24px">
            <template #header>
              <span>🖼️ 生成结果</span>
            </template>
            <ResultViewer
              :original-url="originalUrl"
              :result-url="resultUrl"
              :loading="generating"
            />
          </el-card>
        </el-col>
      </el-row>
    </main>

    <footer class="app-footer">
      <p>InkIn 入画 &copy; 2026</p>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.app-header {
  text-align: center;
  color: white;
  padding: 20px 0;
}

.app-header h1 {
  font-size: 2rem;
  margin: 0;
}

.app-header p {
  margin: 8px 0 0;
  opacity: 0.8;
}

.app-main {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.settings-card,
.upload-card,
.result-card {
  margin-bottom: 0;
}

.app-footer {
  text-align: center;
  color: white;
  padding: 20px 0;
  opacity: 0.7;
  font-size: 14px;
}
</style>
