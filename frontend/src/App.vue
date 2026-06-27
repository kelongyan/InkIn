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
        // 滚动到结果区
        setTimeout(() => {
          document.getElementById('gallery')?.scrollIntoView({ behavior: 'smooth' })
        }, 300)
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

function scrollToStudio() {
  document.getElementById('studio')?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="app">
    <!-- ====== Hero 首屏 ====== -->
    <section class="hero paper-texture">
      <!-- 水墨装饰 -->
      <div class="hero-ink hero-ink-1"></div>
      <div class="hero-ink hero-ink-2"></div>
      <div class="hero-ink hero-ink-3"></div>

      <!-- 配置入口 -->
      <el-button
        class="settings-trigger"
        :icon="Setting"
        circle
        plain
        @click="drawerVisible = true"
      />

      <div class="hero-content">
        <h1 class="hero-title">
          <span class="hero-title-en">InkIn</span>
          <span class="hero-dot">·</span>
          <span class="hero-title-cn">入画</span>
        </h1>
        <div class="hero-line"></div>
        <p class="hero-subtitle">将你的照片，绘入艺术的世界</p>
      </div>

      <div class="hero-scroll" @click="scrollToStudio">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14M5 12l7 7 7-7" />
        </svg>
      </div>
    </section>

    <!-- ====== 创作工作台 ====== -->
    <section id="studio" class="studio paper-texture">
      <div class="studio-inner">
        <div class="studio-label">
          <span class="studio-label-line"></span>
          <span class="studio-label-text">创 作 工 作 台</span>
          <span class="studio-label-line"></span>
        </div>

        <div class="canvas-area">
          <ImageUploader
            @upload-start="onUploadStart"
            @upload-success="onUploadSuccess"
            @upload-error="onUploadError"
          />
        </div>

        <el-button
          type="primary"
          size="large"
          :loading="generating"
          :disabled="!canGenerate"
          class="generate-btn"
          @click="handleGenerate"
        >
          {{ generating ? '水墨晕染中...' : '✨ 开始入画' }}
        </el-button>
      </div>
    </section>

    <!-- ====== 作品展厅 ====== -->
    <section id="gallery" class="gallery paper-texture">
      <div class="gallery-inner">
        <div class="gallery-label">
          <span class="gallery-label-line"></span>
          <span class="gallery-label-text">作 品 展 厅</span>
          <span class="gallery-label-line"></span>
        </div>

        <ResultViewer
          :original-url="originalUrl"
          :result-url="resultUrl"
          :loading="generating"
        />
      </div>
    </section>

    <!-- ====== 页脚印章 ====== -->
    <footer class="app-footer">
      <span class="seal">InkIn</span>
      <span class="footer-text">入画 &copy; 2026</span>
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
/* ====== 页面整体 ====== */
.app {
  min-height: 100vh;
  background-color: var(--color-bg);
  overflow-x: hidden;
}

/* ====== Hero 首屏 ====== */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(ellipse at 30% 20%, rgba(194, 53, 49, 0.04) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 80%, rgba(44, 44, 44, 0.03) 0%, transparent 50%),
    var(--color-bg);
  overflow: hidden;
}

/* 水墨装饰圆 */
.hero-ink {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(44, 44, 44, 0.06) 0%, transparent 70%);
  pointer-events: none;
}
.hero-ink-1 {
  width: 400px;
  height: 400px;
  top: -100px;
  left: -100px;
  animation: ink-drop 3s ease-out forwards;
}
.hero-ink-2 {
  width: 250px;
  height: 250px;
  bottom: 10%;
  right: 5%;
  animation: ink-drop 3s 0.5s ease-out forwards;
}
.hero-ink-3 {
  width: 150px;
  height: 150px;
  top: 30%;
  right: 20%;
  background: radial-gradient(circle, rgba(194, 53, 49, 0.05) 0%, transparent 70%);
  animation: ink-drop 3s 1s ease-out forwards;
}

/* 配置齿轮 */
.settings-trigger {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 50;
  background: var(--color-surface);
  border-color: var(--color-border);
  color: var(--color-ink-light);
  box-shadow: var(--shadow-card);
  transition: all 0.3s ease;
}
.settings-trigger:hover {
  color: var(--color-vermilion);
  border-color: var(--color-vermilion);
}

/* Hero 内容 */
.hero-content {
  text-align: center;
  animation: fade-up 1.2s ease-out;
  z-index: 1;
}

.hero-title {
  font-family: var(--font-serif);
  font-size: clamp(40px, 8vw, 80px);
  font-weight: 700;
  color: var(--color-ink);
  letter-spacing: 8px;
  margin: 0;
  line-height: 1.2;
}

.hero-title-en {
  display: inline-block;
}

.hero-dot {
  color: var(--color-vermilion);
  font-weight: 400;
  margin: 0 4px;
}

.hero-title-cn {
  display: inline-block;
}

/* 毛笔横扫装饰线 */
.hero-line {
  width: 80px;
  height: 3px;
  background: var(--color-vermilion);
  margin: 20px auto;
  border-radius: 2px;
  animation: brush-stroke 1s 0.5s ease-out both;
  transform-origin: left;
}

.hero-subtitle {
  font-family: var(--font-sans);
  font-size: clamp(14px, 2.5vw, 18px);
  color: var(--color-ink-light);
  letter-spacing: 4px;
  margin: 0;
  animation: fade-up 1.2s 0.3s ease-out both;
}

/* 向下滚动箭头 */
.hero-scroll {
  position: absolute;
  bottom: 40px;
  color: var(--color-ink-faint);
  cursor: pointer;
  animation: bounce-down 2s ease-in-out infinite;
  transition: color 0.3s ease;
  z-index: 1;
}
.hero-scroll:hover {
  color: var(--color-vermilion);
}

/* ====== 创作工作台 ====== */
.studio {
  padding: 80px 24px;
  display: flex;
  justify-content: center;
}

.studio-inner {
  width: 100%;
  max-width: 680px;
  animation: fade-up 0.8s ease-out;
}

/* 区域标签 */
.studio-label,
.gallery-label {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 40px;
  justify-content: center;
}

.studio-label-text,
.gallery-label-text {
  font-family: var(--font-serif);
  font-size: 15px;
  color: var(--color-ink-light);
  letter-spacing: 6px;
  white-space: nowrap;
}

.studio-label-line,
.gallery-label-line {
  flex: 1;
  max-width: 120px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-border), transparent);
}

/* 画布区域 */
.canvas-area {
  margin-bottom: 32px;
}

/* 生成按钮 */
.generate-btn {
  width: 100%;
  height: 52px;
  font-size: 18px;
  letter-spacing: 4px;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}
.generate-btn:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(194, 53, 49, 0.3);
}

/* ====== 作品展厅 ====== */
.gallery {
  padding: 60px 24px 80px;
  display: flex;
  justify-content: center;
  background:
    radial-gradient(ellipse at 50% 0%, rgba(44, 44, 44, 0.02) 0%, transparent 60%),
    var(--color-bg);
}

.gallery-inner {
  width: 100%;
  max-width: 900px;
}

/* ====== 页脚 ====== */
.app-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid var(--color-border-light);
}

.seal {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 2px solid var(--color-vermilion);
  color: var(--color-vermilion);
  font-family: var(--font-serif);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  border-radius: 2px;
  transform: rotate(-3deg);
}

.footer-text {
  font-size: 13px;
  color: var(--color-ink-faint);
  letter-spacing: 1px;
}

/* ====== 响应式 ====== */
@media (max-width: 768px) {
  .hero {
    min-height: 80vh;
  }

  .hero-ink-1 { width: 200px; height: 200px; }
  .hero-ink-2 { width: 120px; height: 120px; }
  .hero-ink-3 { display: none; }

  .studio { padding: 60px 16px; }
  .gallery { padding: 40px 16px 60px; }

  .settings-trigger {
    top: 12px;
    right: 12px;
  }
}
</style>
