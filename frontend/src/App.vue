<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Setting } from '@element-plus/icons-vue'
import ImageUploader from './components/ImageUploader.vue'
import ApiSettings from './components/ApiSettings.vue'
import ResultViewer from './components/ResultViewer.vue'
import { generateComic } from './utils/api.js'

const uploadedFile = ref(null)
const originalUrl = ref('')
const resultUrl = ref('')
const generating = ref(false)
const uploading = ref(false)
const drawerVisible = ref(false)

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
  <div class="app">
    <!-- ====== 顶栏 ====== -->
    <header class="app-header">
      <div class="brand">
        <h1 class="brand-logo">
          <span class="brand-en">InkIn</span>
          <span class="brand-dot">·</span>
          <span class="brand-cn">入画</span>
        </h1>
        <p class="brand-tagline">你的照片，值得一个漫画版本</p>
      </div>

      <el-button
        class="settings-trigger"
        :icon="Setting"
        circle
        plain
        @click="drawerVisible = true"
      />
    </header>

    <!-- ====== 工作区（上传 + 结果 并排一页）====== -->
    <main class="workspace">
      <!-- 左：创作工作台 -->
      <section class="studio-col">
        <div class="section-label">
          <span class="section-label-text">STUDIO</span>
          <span class="section-label-line"></span>
        </div>

        <div class="upload-panel panel-frame">
          <ImageUploader
            @upload-start="onUploadStart"
            @upload-success="onUploadSuccess"
            @upload-error="onUploadError"
          />
        </div>

        <button
          class="generate-btn"
          :class="{ 'is-loading': generating }"
          :disabled="!canGenerate"
          @click="handleGenerate"
        >
          <svg v-if="!generating" class="generate-icon" viewBox="0 0 20 20" fill="none">
            <path d="M10 2l2.5 5 5.5.8-4 3.9.9 5.3L10 14.5 5.1 17l.9-5.3-4-3.9 5.5-.8L10 2z"
              stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="currentColor" opacity="0.15"/>
          </svg>
          <span v-if="generating" class="generate-spinner"></span>
          {{ generating ? '绘制中...' : '开始变身' }}
        </button>
      </section>

      <!-- 右：作品展厅 -->
      <section class="gallery-col">
        <div class="section-label">
          <span class="section-label-text">GALLERY</span>
          <span class="section-label-line"></span>
        </div>

        <div class="gallery-panel panel-frame">
          <ResultViewer
            :original-url="originalUrl"
            :result-url="resultUrl"
            :loading="generating"
          />
        </div>
      </section>
    </main>

    <!-- ====== Footer ====== -->
    <footer class="app-footer">
      <span class="footer-mark">InkIn</span>
      <span class="footer-copy">&copy; 2026</span>
    </footer>

    <!-- ====== API 配置抽屉 ====== -->
    <el-drawer
      v-model="drawerVisible"
      title="API 配置"
      direction="rtl"
      size="380px"
      :z-index="100"
    >
      <ApiSettings @config-saved="drawerVisible = false" />
    </el-drawer>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background-color: var(--color-canvas);
  display: flex;
  flex-direction: column;
}

/* ====== 顶栏 ====== */
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 32px;
  border-bottom: 1px solid var(--color-border-light);
}

.brand {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-logo {
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--color-ink);
  margin: 0;
  line-height: 1.1;
  letter-spacing: -0.5px;
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.brand-en {
  font-size: var(--text-2xl);
}

.brand-dot {
  font-size: var(--text-xl);
  color: var(--color-pop);
  font-weight: 400;
}

.brand-cn {
  font-size: var(--text-lg);
  font-weight: 500;
  color: var(--color-ink-soft);
  letter-spacing: 2px;
}

.brand-tagline {
  font-size: var(--text-xs);
  color: var(--color-muted);
  letter-spacing: 0.5px;
  margin: 0;
}

.settings-trigger {
  background: var(--color-panel);
  border-color: var(--color-border);
  color: var(--color-muted);
  box-shadow: var(--panel-shadow);
  transition: all 0.25s ease;
}
.settings-trigger:hover {
  color: var(--color-pop);
  border-color: var(--color-pop);
}

/* ====== 工作区 ====== */
.workspace {
  flex: 1;
  display: flex;
  gap: 32px;
  padding: 32px;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  align-items: stretch;
}

.studio-col {
  flex: 0 0 380px;
  display: flex;
  flex-direction: column;
}

.gallery-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* 区域标签 */
.section-label {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.section-label-text {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 500;
  color: var(--color-muted);
  letter-spacing: 3px;
  white-space: nowrap;
}

.section-label-line {
  flex: 1;
  height: 1px;
  background: var(--color-border);
}

/* 上传分镜框 */
.upload-panel {
  padding: 24px 20px;
  margin-bottom: 16px;
}

/* 生成按钮 */
.generate-btn {
  width: 100%;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 600;
  letter-spacing: 1px;
  color: var(--color-panel);
  background: var(--color-pop);
  border: none;
  border-radius: var(--radius-xs);
  cursor: pointer;
  transition: all 0.25s ease;
}
.generate-btn:hover:not(:disabled) {
  background: var(--color-pop-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.3);
}
.generate-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.generate-btn.is-loading {
  opacity: 0.7;
  cursor: wait;
}

.generate-icon {
  width: 16px;
  height: 16px;
}

.generate-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 结果分镜框 */
.gallery-panel {
  flex: 1;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ====== Footer ====== */
.app-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  border-top: 1px solid var(--color-border-light);
}

.footer-mark {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--color-ink);
  letter-spacing: 1px;
}

.footer-copy {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-muted);
}

/* ====== 响应式 ====== */
@media (max-width: 900px) {
  .workspace {
    flex-direction: column;
    padding: 20px;
    gap: 24px;
  }

  .studio-col {
    flex: none;
  }

  .gallery-panel {
    min-height: 320px;
  }
}

@media (max-width: 768px) {
  .app-header {
    padding: 16px 20px;
  }

  .brand-en {
    font-size: var(--text-xl);
  }

  .brand-cn {
    font-size: var(--text-base);
  }
}
</style>
