<script setup>
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
    <!-- 整个舞台：未生成时不显示 -->
    <Transition name="stage-in">
      <div
        v-if="originalUrl || resultUrl || loading"
        class="stage"
      >
        <!-- 底层：原图（生成时显影登场）-->
        <img
          v-if="originalUrl"
          :src="originalUrl"
          class="layer layer-original"
          alt="原图"
        />

        <!-- 覆盖层：漫画（变身特效，覆盖原图）-->
        <Transition name="transform">
          <img
            v-if="resultUrl"
            :src="resultUrl"
            class="layer layer-result"
            alt="漫画"
          />
        </Transition>

        <!-- 生成中：halftone 网点覆盖 -->
        <Transition name="fade">
          <div v-if="loading" class="loading-overlay">
            <div class="loading-halftone"></div>
            <p class="loading-title">正在绘制</p>
            <p class="loading-tip">将你的照片绘入漫画…</p>
          </div>
        </Transition>
      </div>
    </Transition>

    <!-- 下载按钮：漫画变身完成后浮现 -->
    <Transition name="fade-up">
      <div v-if="resultUrl && !loading" class="gallery-actions">
        <button class="download-btn" @click="downloadImage">
          <svg viewBox="0 0 20 20" fill="none" class="btn-icon">
            <path d="M10 3v10M6 9l4 4 4-4M4 15h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          下载作品
        </button>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.result-viewer {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

/* ====== 舞台：整体登场 ====== */
.stage {
  position: relative;
  width: 100%;
  min-height: 380px;
  background: var(--color-canvas);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

/* 舞台入场：从无到有，带轻微缩放 */
.stage-in-enter-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.stage-in-enter-from {
  opacity: 0;
  transform: scale(0.96);
}

.layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.layer-original {
  z-index: 1;
  animation: fade-in 0.5s ease-out;
}

.layer-result {
  z-index: 2;
}

/* ====== 变身特效：漫画覆盖原图 ======
   模拟「变身」：从模糊+放大+高亮 → 清晰定格 */
.transform-enter-active {
  transition: opacity 0.8s ease-out, filter 0.8s ease-out, transform 0.8s ease-out;
}
.transform-enter-from {
  opacity: 0;
  filter: blur(16px) brightness(1.4);
  transform: scale(1.1);
}

/* ====== loading 覆盖 ====== */
.loading-overlay {
  position: absolute;
  inset: 0;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: rgba(250, 250, 247, 0.72);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.loading-halftone {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-image: radial-gradient(circle, var(--color-pop) 1.5px, transparent 1.5px);
  background-size: 6px 6px;
  animation: halftone-reveal 1.5s ease-in-out infinite alternate;
  opacity: 0.5;
}

.loading-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--color-ink);
  letter-spacing: 0.5px;
  margin-top: 10px;
}

.loading-tip {
  font-size: var(--text-sm);
  color: var(--color-muted);
}

/* ====== 下载按钮 ====== */
.gallery-actions {
  display: flex;
  justify-content: center;
}

.fade-up-enter-active {
  transition: opacity 0.5s ease 0.4s, transform 0.5s ease 0.4s;
}
.fade-up-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.download-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 44px;
  padding: 0 28px;
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 500;
  letter-spacing: 0.5px;
  color: var(--color-pop);
  background: transparent;
  border: 2px solid var(--color-pop);
  border-radius: var(--radius-xs);
  cursor: pointer;
  transition: all 0.25s ease;
}
.download-btn:hover {
  background: var(--color-pop);
  color: var(--color-panel);
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* ====== 响应式 ====== */
@media (max-width: 900px) {
  .stage {
    min-height: 300px;
  }
}
</style>
