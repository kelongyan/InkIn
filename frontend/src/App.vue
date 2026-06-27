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
    <!-- 顶部墨色装饰条 -->
    <div class="ink-bar"></div>

    <header class="app-header">
      <h1 class="app-title">
        <span class="title-en">InkIn</span>
        <span class="title-divider">·</span>
        <span class="title-cn">入画</span>
      </h1>
      <p class="app-subtitle">让照片走进艺术的世界</p>
    </header>

    <main class="app-main">
      <div class="layout">
        <!-- 左侧：配置面板 -->
        <aside class="sidebar">
          <el-card class="card settings-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span class="card-header-bar"></span>
                <span>API 配置</span>
              </div>
            </template>
            <ApiSettings />
          </el-card>
        </aside>

        <!-- 右侧：上传 + 结果 -->
        <div class="content">
          <el-card class="card upload-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span class="card-header-bar"></span>
                <span>上传图片</span>
              </div>
            </template>
            <ImageUploader
              @upload-start="onUploadStart"
              @upload-success="onUploadSuccess"
              @upload-error="onUploadError"
            />
            <el-button
              type="primary"
              size="large"
              :loading="generating"
              :disabled="!canGenerate"
              class="generate-btn"
              @click="handleGenerate"
            >
              {{ generating ? '生成中...' : '✨ 生成漫画' }}
            </el-button>
          </el-card>

          <el-card class="card result-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span class="card-header-bar"></span>
                <span>生成结果</span>
              </div>
            </template>
            <ResultViewer
              :original-url="originalUrl"
              :result-url="resultUrl"
              :loading="generating"
            />
          </el-card>
        </div>
      </div>
    </main>

    <footer class="app-footer">
      <p>InkIn 入画 &copy; 2026 &middot; 让照片走进艺术的世界</p>
    </footer>
  </div>
</template>

<style scoped>
/* 页面容器 */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--color-bg);
}

/* 顶部墨色装饰条 */
.ink-bar {
  height: 4px;
  background: linear-gradient(90deg, #2c2c2c 0%, #4a4a4a 50%, #2c2c2c 100%);
  flex-shrink: 0;
}

/* Header */
.app-header {
  text-align: center;
  padding: var(--space-8) var(--space-6) var(--space-5);
}

.app-title {
  font-family: var(--font-serif);
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--color-ink);
  letter-spacing: 4px;
  margin: 0;
}

.title-en {
  font-family: var(--font-serif);
}

.title-divider {
  margin: 0 6px;
  color: var(--color-vermilion);
  font-weight: 400;
}

.title-cn {
  font-family: var(--font-serif);
}

.app-subtitle {
  margin-top: var(--space-2);
  font-size: var(--text-base);
  color: var(--color-ink-light);
  letter-spacing: 2px;
}

/* 主内容区 */
.app-main {
  flex: 1;
  max-width: 1100px;
  margin: 0 auto;
  width: 100%;
  padding: 0 var(--space-6) var(--space-8);
}

.layout {
  display: flex;
  gap: var(--space-6);
  align-items: flex-start;
}

/* 左侧栏 */
.sidebar {
  width: 320px;
  flex-shrink: 0;
  position: sticky;
  top: var(--space-6);
}

/* 右侧内容 */
.content {
  flex: 1;
  min-width: 0;
}

/* 卡片通用样式 */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  transition: box-shadow 0.3s ease;
  margin-bottom: var(--space-6);
}

.card:hover {
  box-shadow: var(--shadow-card-hover);
}

/* 卡片标题 */
.card-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: var(--text-lg);
  font-weight: 500;
  color: var(--color-ink);
}

.card-header-bar {
  display: inline-block;
  width: 3px;
  height: 18px;
  background-color: var(--color-vermilion);
  border-radius: 2px;
  flex-shrink: 0;
}

/* 生成按钮 */
.generate-btn {
  width: 100%;
  margin-top: var(--space-5);
  height: 44px;
  font-size: var(--text-lg);
  letter-spacing: 2px;
  border-radius: var(--radius-sm);
}

/* Footer */
.app-footer {
  text-align: center;
  padding: var(--space-5) var(--space-6);
  color: var(--color-ink-faint);
  font-size: var(--text-sm);
  border-top: 1px solid var(--color-border-light);
}

/* 响应式 */
@media (max-width: 768px) {
  .layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    position: static;
  }

  .app-title {
    font-size: var(--text-2xl);
  }

  .app-main {
    padding: 0 var(--space-4) var(--space-6);
  }
}
</style>
