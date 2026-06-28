<script setup>
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Setting } from '@element-plus/icons-vue'
import ImageUploader from './components/ImageUploader.vue'
import ApiSettings from './components/ApiSettings.vue'
import ResultViewer from './components/ResultViewer.vue'
import { generateComic } from './utils/api.js'

const uploadedFile = ref(null)
const resultUrl = ref('')
const generating = ref(false)
const uploading = ref(false)
const drawerVisible = ref(false)

const canGenerate = computed(() => uploadedFile.value && !generating.value && !uploading.value)
const showPreviewStage = computed(() => generating.value || Boolean(resultUrl.value))
const workbenchHasPreview = computed(() => showPreviewStage.value)

function onUploadStart() {
  uploading.value = true
}

function onUploadSuccess(data) {
  uploadedFile.value = data.filename
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
        ElMessage.success('入画完成')
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
  <div class="app-shell">
    <div class="ambient-mark mark-one">入</div>
    <div class="ambient-mark mark-two">画</div>

    <header class="topbar">
      <a class="brand-lockup" href="#" aria-label="InkIn 入画首页">
        <span class="brand-seal" aria-hidden="true">
          <img class="brand-logo" src="/favicon.svg" alt="" />
        </span>
        <span class="brand-text">
          <strong>InkIn</strong>
          <small>photo to art atelier</small>
        </span>
      </a>

      <button
        class="settings-button"
        type="button"
        aria-label="打开 API 设置"
        title="API 设置"
        @click="drawerVisible = true"
      >
        <el-icon><Setting /></el-icon>
      </button>
    </header>

    <main class="atelier">
      <section class="hero-copy" aria-labelledby="hero-title">
        <p class="label-kicker">local art studio</p>
        <h1 id="hero-title">把一张照片，<span>挂进你的漫画画廊。</span></h1>
      </section>

      <section
        class="workbench atelier-panel"
        :class="{ 'has-preview': workbenchHasPreview }"
        aria-label="入画创作工作台"
      >
        <div class="workbench-header">
          <div>
            <p class="panel-eyebrow">Studio Desk</p>
            <h2>创作台</h2>
          </div>
        </div>

        <div class="desk-grid" :class="{ 'has-preview': showPreviewStage }">
          <div class="upload-zone">
            <ImageUploader
              @upload-start="onUploadStart"
              @upload-success="onUploadSuccess"
              @upload-error="onUploadError"
            />

            <button
              class="generate-btn ink-button"
              :class="{ 'is-loading': generating }"
              :disabled="!canGenerate"
              type="button"
              @click="handleGenerate"
            >
              <span v-if="generating" class="generate-spinner" aria-hidden="true"></span>
              <span v-else class="spark" aria-hidden="true"></span>
              {{ generating ? '正在入画' : '开始入画' }}
            </button>
          </div>

          <Transition name="gallery-panel">
            <div v-if="showPreviewStage" class="result-zone">
              <ResultViewer
                :result-url="resultUrl"
                :loading="generating"
              />
            </div>
          </Transition>
        </div>
      </section>
    </main>

    <footer class="app-footer">
      <span>InkIn 入画</span>
      <span>本地创作工具</span>
    </footer>

    <el-drawer
      v-model="drawerVisible"
      title="API 器材箱"
      direction="rtl"
      size="min(420px, 92vw)"
      :z-index="100"
      class="settings-drawer"
    >
      <ApiSettings @config-saved="drawerVisible = false" />
    </el-drawer>
  </div>
</template>

<style scoped>
.app-shell {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding: 14px clamp(16px, 3vw, 42px) 10px;
  display: flex;
  flex-direction: column;
}

.ambient-mark {
  position: fixed;
  z-index: -1;
  font-family: var(--font-display);
  font-size: clamp(150px, 22vw, 360px);
  font-weight: 900;
  line-height: 1;
  color: rgba(79, 54, 35, 0.055);
  pointer-events: none;
  user-select: none;
}

.mark-one {
  top: 7vh;
  left: -4vw;
  transform: rotate(-9deg);
}

.mark-two {
  right: -4vw;
  bottom: 0;
  transform: rotate(7deg);
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.brand-lockup {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  color: inherit;
  text-decoration: none;
}

.brand-seal {
  display: inline-flex;
  width: 42px;
  height: 42px;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: var(--color-vermilion);
  border-radius: 12px;
  box-shadow: 0 12px 24px rgba(159, 46, 34, 0.24);
}

.brand-logo {
  display: block;
  width: 100%;
  height: 100%;
}

.brand-text {
  display: grid;
  gap: 1px;
}

.brand-text strong {
  font-family: var(--font-display);
  font-size: 20px;
  line-height: 1;
}

.brand-text small {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.16em;
  color: var(--color-muted);
  text-transform: uppercase;
}

.settings-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  padding: 0;
  color: var(--color-ink);
  background: rgba(255, 250, 240, 0.66);
  border: 1px solid var(--color-line);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 10px 26px rgba(66, 41, 20, 0.1);
  transition: transform 0.22s ease, background 0.22s ease, border-color 0.22s ease;
}

.settings-button:hover {
  transform: translateY(-1px);
  background: var(--color-paper);
  border-color: rgba(201, 71, 45, 0.42);
}

.atelier {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  grid-template-rows: auto minmax(0, 1fr);
  gap: clamp(22px, 3vw, 36px);
  align-items: start;
  justify-items: center;
  width: 100%;
  max-width: 1280px;
  min-height: 0;
  margin: 0 auto;
  padding: clamp(10px, 1.6vw, 18px) 0 0;
}

.hero-copy {
  width: 100%;
  text-align: center;
  animation: reveal-up 0.62s ease both;
}

.hero-copy h1 {
  max-width: none;
  margin-top: 6px;
  font-family: var(--font-display);
  font-size: clamp(34px, 4.2vw, 56px);
  font-weight: 900;
  line-height: 1.02;
  letter-spacing: 0;
  color: var(--color-ink);
  white-space: nowrap;
}

.hero-copy h1 span {
  display: inline;
  color: var(--color-vermilion-deep);
}

.workbench {
  width: min(100%, 760px);
  padding: clamp(12px, 1.6vw, 18px) clamp(14px, 2vw, 22px);
  animation: reveal-up 0.62s 0.08s ease both;
}

.workbench.has-preview {
  width: min(100%, 980px);
}

.workbench:not(.has-preview) {
  padding: clamp(18px, 2vw, 24px);
}

.workbench-header {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 8px;
}

.panel-eyebrow {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.2em;
  color: var(--color-muted);
  text-transform: uppercase;
}

.workbench-header h2 {
  margin-top: 4px;
  font-family: var(--font-display);
  font-size: clamp(24px, 2.4vw, 32px);
  line-height: 1;
}

.desk-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(360px, 640px);
  gap: 16px;
  align-items: stretch;
  justify-content: center;
}

.desk-grid.has-preview {
  grid-template-columns: minmax(280px, 0.78fr) minmax(420px, 1.08fr);
  justify-content: stretch;
}

.upload-zone,
.result-zone {
  min-width: 0;
}

.desk-grid:not(.has-preview) .upload-zone {
  width: min(100%, 640px);
  justify-self: center;
}

.desk-grid:not(.has-preview) :deep(.uploader-frame) {
  min-height: 360px;
}

.desk-grid:not(.has-preview) :deep(.upload-state),
.desk-grid:not(.has-preview) :deep(.empty-state),
.desk-grid:not(.has-preview) :deep(.preview-state) {
  min-height: 312px;
}

.generate-btn {
  width: 100%;
  min-height: 44px;
  margin-top: 12px;
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.generate-btn.is-loading {
  background: var(--color-vermilion-deep);
}

.generate-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 250, 240, 0.35);
  border-top-color: var(--color-paper);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spark {
  position: relative;
  width: 16px;
  height: 16px;
}

.spark::before,
.spark::after {
  content: "";
  position: absolute;
  inset: 7px 0;
  background: currentColor;
  border-radius: 999px;
}

.spark::after {
  transform: rotate(90deg);
}

.gallery-panel-enter-active,
.gallery-panel-leave-active {
  transition: opacity 0.42s ease, transform 0.42s ease, filter 0.42s ease;
}

.gallery-panel-enter-from,
.gallery-panel-leave-to {
  opacity: 0;
  filter: blur(10px);
  transform: translateY(16px) scale(0.98);
}

.app-footer {
  display: none;
  justify-content: center;
  gap: 14px;
  padding: 8px 0 0;
  color: rgba(89, 74, 61, 0.72);
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

:deep(.el-drawer) {
  background:
    linear-gradient(135deg, rgba(255, 250, 240, 0.98), rgba(239, 224, 201, 0.96)),
    var(--color-paper);
}

:deep(.el-drawer__header) {
  margin-bottom: 18px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--color-line);
  color: var(--color-ink);
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 800;
}

@media (min-width: 1121px) {
  .app-shell {
    height: 100vh;
  }
}

@media (max-width: 1120px) {
  .atelier {
    align-items: start;
  }

  .hero-copy h1 {
    max-width: none;
  }
}

@media (max-width: 780px) {
  .app-shell {
    padding: 16px;
  }

  .topbar {
    align-items: flex-start;
  }

  .atelier {
    padding-top: 34px;
  }

  .hero-copy h1 {
    font-size: clamp(44px, 16vw, 72px);
    white-space: normal;
  }

  .desk-grid,
  .desk-grid.has-preview {
    grid-template-columns: 1fr;
  }

  .desk-grid:not(.has-preview) .upload-zone {
    width: 100%;
  }

  .desk-grid:not(.has-preview) :deep(.uploader-frame) {
    min-height: 260px;
  }

  .desk-grid:not(.has-preview) :deep(.upload-state),
  .desk-grid:not(.has-preview) :deep(.empty-state),
  .desk-grid:not(.has-preview) :deep(.preview-state) {
    min-height: 210px;
  }

  .workbench {
    padding: 18px;
  }

  .workbench-header {
    flex-direction: column;
  }
}
</style>
