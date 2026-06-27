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
      <div class="loading-ring">
        <el-icon class="is-loading" :size="36"><Loading /></el-icon>
      </div>
      <p class="state-title">水墨晕染中</p>
      <p class="state-tip">正在将你的照片绘入画中…</p>
      <div class="loading-dots">
        <span></span><span></span><span></span>
      </div>
    </div>

    <!-- 有结果 — 画廊展示 -->
    <div v-else-if="resultUrl" class="gallery-show">
      <div class="compare-row">
        <!-- 原图 -->
        <div class="artwork">
          <div class="artwork-frame img-frame">
            <img v-if="originalUrl" :src="originalUrl" alt="原图" />
          </div>
          <p class="artwork-label">原 作</p>
        </div>

        <!-- 转换箭头 -->
        <div class="arrow-wrap">
          <svg class="arrow-svg" viewBox="0 0 48 48" fill="none">
            <path d="M8 24h28M28 16l8 8-8 8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>

        <!-- 漫画 -->
        <div class="artwork">
          <div class="artwork-frame img-frame">
            <img :src="resultUrl" alt="漫画" />
          </div>
          <p class="artwork-label">入 画</p>
        </div>
      </div>

      <div class="gallery-actions">
        <el-button type="primary" class="collect-btn" @click="downloadImage">
          <svg viewBox="0 0 20 20" fill="none" class="btn-icon">
            <path d="M10 3v10M6 9l4 4 4-4M4 15h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          收藏作品
        </el-button>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="state empty-state">
      <div class="empty-scroll">
        <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="10" y="16" width="60" height="48" rx="3" stroke="currentColor" stroke-width="1.5"/>
          <rect x="10" y="16" width="60" height="8" rx="3" stroke="currentColor" stroke-width="1.5"/>
          <rect x="10" y="56" width="60" height="8" rx="3" stroke="currentColor" stroke-width="1.5"/>
          <path d="M24 40h32M40 32v16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>
        </svg>
      </div>
      <p class="state-title">画卷尚空</p>
      <p class="state-tip">上传图片并点击「开始入画」，作品将在此展出</p>
    </div>
  </div>
</template>

<style scoped>
.result-viewer {
  width: 100%;
  min-height: 260px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ====== 通用状态 ====== */
.state {
  text-align: center;
  padding: 48px 20px;
  width: 100%;
}

.state-title {
  font-family: var(--font-serif);
  font-size: 16px;
  color: var(--color-ink);
  font-weight: 600;
  letter-spacing: 3px;
  margin-top: 16px;
}

.state-tip {
  font-size: 13px;
  color: var(--color-ink-faint);
  margin-top: 8px;
  letter-spacing: 1px;
}

/* ====== 加载状态 ====== */
.loading-ring {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-vermilion);
  color: var(--color-vermilion);
}

.loading-dots {
  display: flex;
  gap: 6px;
  justify-content: center;
  margin-top: 16px;
}
.loading-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-vermilion);
  opacity: 0.3;
  animation: fade-in 1s ease-in-out infinite alternate;
}
.loading-dots span:nth-child(2) { animation-delay: 0.3s; }
.loading-dots span:nth-child(3) { animation-delay: 0.6s; }

/* ====== 画廊展示 ====== */
.gallery-show {
  width: 100%;
  animation: fade-up 0.6s ease-out;
}

.compare-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

/* 作品卡片 */
.artwork {
  flex: 1;
  min-width: 200px;
  max-width: 380px;
  text-align: center;
}

.artwork-frame {
  overflow: hidden;
}
.artwork-frame img {
  width: 100%;
  display: block;
  border-radius: 1px;
}

.artwork-label {
  font-family: var(--font-serif);
  font-size: 14px;
  color: var(--color-ink-light);
  letter-spacing: 6px;
  margin-top: 12px;
  font-weight: 500;
}

/* 转换箭头 */
.arrow-wrap {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-vermilion);
  opacity: 0.6;
}

.arrow-svg {
  width: 36px;
  height: 36px;
}

/* 操作区 */
.gallery-actions {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.collect-btn {
  height: 44px;
  padding: 0 32px;
  font-size: 15px;
  letter-spacing: 2px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* ====== 空状态 ====== */
.empty-scroll {
  width: 72px;
  height: 72px;
  margin: 0 auto 12px;
  color: var(--color-border);
}
.empty-scroll svg {
  width: 100%;
  height: 100%;
}

/* ====== 响应式 ====== */
@media (max-width: 640px) {
  .compare-row {
    flex-direction: column;
    gap: 12px;
  }

  .artwork {
    max-width: 100%;
  }

  .arrow-wrap {
    transform: rotate(90deg);
  }
}
</style>
