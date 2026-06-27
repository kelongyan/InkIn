<script setup>
import { Loading } from '@element-plus/icons-vue'

const props = defineProps({
  originalUrl: String,
  resultUrl: String,
  loading: Boolean,
})

function downloadImage() {
  if (!props.resultUrl) return

  const link = document.createElement('a')
  link.href = props.resultUrl
  link.download = 'inkin-comic.png'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<template>
  <div class="result-viewer">
    <!-- 加载中 -->
    <div v-if="loading" class="state loading-state">
      <el-icon class="is-loading spin-icon" :size="40"><Loading /></el-icon>
      <p class="state-title">正在生成漫画</p>
      <p class="state-tip">水墨晕染中，请稍候…</p>
    </div>

    <!-- 有结果 -->
    <div v-else-if="resultUrl" class="result-content">
      <div class="image-compare">
        <div class="image-box">
          <p class="image-label">原图</p>
          <img v-if="originalUrl" :src="originalUrl" alt="原图" />
        </div>
        <div class="image-box">
          <p class="image-label">漫画</p>
          <img :src="resultUrl" alt="漫画" />
        </div>
      </div>
      <el-button type="primary" class="download-btn" @click="downloadImage">
        下载漫画
      </el-button>
    </div>

    <!-- 空状态 -->
    <div v-else class="state empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="8" y="12" width="48" height="40" rx="4" stroke="currentColor" stroke-width="2" />
          <path d="M8 40l14-12 10 8 8-6 16 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
          <circle cx="22" cy="26" r="4" stroke="currentColor" stroke-width="2" />
        </svg>
      </div>
      <p class="state-title">等待生成</p>
      <p class="state-tip">上传图片后点击「生成漫画」</p>
    </div>
  </div>
</template>

<style scoped>
.result-viewer {
  width: 100%;
  min-height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 通用状态 */
.state {
  text-align: center;
  padding: var(--space-8) var(--space-5);
}

.state-title {
  font-size: var(--text-base);
  color: var(--color-ink-light);
  margin-top: var(--space-3);
  font-weight: 500;
}

.state-tip {
  font-size: var(--text-xs);
  color: var(--color-ink-faint);
  margin-top: var(--space-1);
}

/* 加载动画 */
.spin-icon {
  color: var(--color-vermilion);
}

/* 空状态图标 */
.empty-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--space-3);
  color: var(--color-border);
}

.empty-icon svg {
  width: 100%;
  height: 100%;
}

/* 结果展示 */
.result-content {
  text-align: center;
  width: 100%;
}

.image-compare {
  display: flex;
  gap: var(--space-5);
  justify-content: center;
  flex-wrap: wrap;
}

.image-box {
  flex: 1;
  min-width: 200px;
  max-width: 420px;
}

.image-label {
  font-size: var(--text-sm);
  color: var(--color-ink-light);
  margin-bottom: var(--space-2);
  font-weight: 500;
}

.image-box img {
  width: 100%;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-card);
}

.download-btn {
  margin-top: var(--space-5);
  height: 40px;
  padding: 0 var(--space-8);
  font-size: var(--text-base);
  letter-spacing: 1px;
  border-radius: var(--radius-sm);
}
</style>
