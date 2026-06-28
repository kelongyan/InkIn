<script setup>
const props = defineProps({
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
  <div class="result-viewer" :class="{ 'has-result': resultUrl, loading }">
    <div class="gallery-stage" :class="{ 'has-result': resultUrl, loading }">
      <Transition name="label-fade">
        <div v-if="resultUrl" class="stage-label">
          <span>Gallery Proof</span>
          <strong>Final</strong>
        </div>
      </Transition>

      <Transition name="developing-fade">
        <div v-if="loading && !resultUrl" class="developing-scene">
          <div class="ink-orbit" aria-hidden="true">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <p>正在显影</p>
          <small>墨色铺开，画面即将成形</small>
        </div>
      </Transition>

      <Transition name="art-reveal" mode="out-in" appear>
        <figure v-if="resultUrl" :key="resultUrl" class="final-art">
          <img :src="resultUrl" alt="生成后的艺术图" />
        </figure>
      </Transition>
    </div>

    <Transition name="action-in">
      <button
        v-if="resultUrl && !loading"
        class="download-btn"
        type="button"
        @click="downloadImage"
      >
        <span aria-hidden="true">↓</span>
        下载作品
      </button>
    </Transition>
  </div>
</template>

<style scoped>
.result-viewer {
  width: 100%;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.gallery-stage {
  position: relative;
  min-height: 310px;
  border-radius: 24px;
  background:
    radial-gradient(circle at 68% 22%, rgba(201, 154, 75, 0.2), transparent 24%),
    linear-gradient(135deg, rgba(24, 34, 38, 0.96), rgba(49, 37, 26, 0.9)),
    var(--color-blueblack);
  overflow: hidden;
  box-shadow: inset 0 0 0 1px rgba(255, 250, 240, 0.1);
}

.gallery-stage.has-result {
  min-height: 340px;
}

.gallery-stage::before {
  content: "";
  position: absolute;
  inset: 18px;
  border: 1px solid rgba(255, 250, 240, 0.16);
  border-radius: 18px;
  pointer-events: none;
  z-index: 5;
}

.gallery-stage::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
  background:
    linear-gradient(transparent 0 92%, rgba(0, 0, 0, 0.22)),
    radial-gradient(circle at 28% 72%, rgba(255, 250, 240, 0.08), transparent 32%);
  pointer-events: none;
}

.stage-label {
  position: absolute;
  top: 22px;
  left: 26px;
  z-index: 7;
  display: inline-grid;
  gap: 2px;
  color: rgba(255, 250, 240, 0.86);
}

.stage-label span {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(255, 250, 240, 0.55);
}

.stage-label strong {
  font-family: var(--font-display);
  font-size: 24px;
  line-height: 1;
}

.developing-scene {
  position: absolute;
  inset: 0;
  z-index: 4;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--color-paper);
  text-align: center;
  background: rgba(24, 34, 38, 0.34);
  backdrop-filter: blur(4px);
}

.ink-orbit {
  position: relative;
  width: 96px;
  height: 96px;
  margin-bottom: 18px;
  border: 1px solid rgba(255, 250, 240, 0.2);
  border-radius: 50%;
  animation: spin 3.6s linear infinite;
}

.ink-orbit::before {
  content: "";
  position: absolute;
  inset: 22px;
  border-radius: 50%;
  background:
    radial-gradient(circle at 50% 50%, var(--color-gold) 0 22%, transparent 23%),
    radial-gradient(circle at 50% 50%, rgba(201, 154, 75, 0.2) 0 58%, transparent 59%);
  animation: ink-breathe 1.2s ease-in-out infinite alternate;
}

.ink-orbit span {
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-paper);
  opacity: 0.78;
}

.ink-orbit span:nth-child(1) {
  top: 8px;
  left: 43px;
}

.ink-orbit span:nth-child(2) {
  right: 11px;
  bottom: 22px;
  background: var(--color-gold);
}

.ink-orbit span:nth-child(3) {
  left: 13px;
  bottom: 24px;
  opacity: 0.48;
}

.developing-scene p {
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 900;
}

.developing-scene small {
  margin-top: 6px;
  color: rgba(255, 250, 240, 0.68);
}

.final-art {
  position: absolute;
  inset: 58px 28px 26px;
  z-index: 4;
  margin: 0;
  padding: 0;
  background: transparent;
  border: 0;
  border-radius: 12px;
  box-shadow: 0 22px 48px rgba(0, 0, 0, 0.34);
  overflow: hidden;
}

.final-art::before {
  content: "";
  position: absolute;
  inset: -18%;
  z-index: 2;
  background: linear-gradient(105deg, transparent 0 30%, rgba(255, 250, 240, 0.64) 44%, rgba(244, 216, 162, 0.42) 50%, transparent 64%);
  mix-blend-mode: screen;
  transform: translateX(-115%) skewX(-10deg);
  animation: brush-sweep 1.1s 0.12s ease-out forwards;
  pointer-events: none;
}

.final-art img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: inherit;
  background: rgba(255, 250, 240, 0.06);
}

.download-btn {
  align-self: flex-end;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-height: 44px;
  padding: 0 20px;
  color: var(--color-ink);
  background: rgba(255, 250, 240, 0.72);
  border: 1px solid rgba(64, 43, 28, 0.24);
  border-radius: 999px;
  cursor: pointer;
  box-shadow: 0 12px 28px rgba(66, 41, 20, 0.14);
  transition: transform 0.22s ease, background 0.22s ease, border-color 0.22s ease;
}

.download-btn:hover {
  transform: translateY(-2px);
  background: var(--color-paper);
  border-color: rgba(201, 71, 45, 0.36);
}

.download-btn span {
  color: var(--color-vermilion);
  font-size: 18px;
  line-height: 1;
}

.art-reveal-enter-active {
  transition: opacity 0.92s ease, transform 0.92s ease, filter 0.92s ease, clip-path 0.92s ease;
}

.art-reveal-enter-from {
  opacity: 0;
  clip-path: inset(0 100% 0 0 round 10px);
  filter: blur(18px) saturate(1.25) brightness(1.12);
  transform: scale(0.96) rotate(-1deg);
}

.label-fade-enter-active,
.label-fade-leave-active,
.developing-fade-enter-active,
.developing-fade-leave-active,
.action-in-enter-active,
.action-in-leave-active {
  transition: opacity 0.32s ease, transform 0.32s ease;
}

.label-fade-enter-from,
.label-fade-leave-to,
.developing-fade-enter-from,
.developing-fade-leave-to,
.action-in-enter-from,
.action-in-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@keyframes brush-sweep {
  to {
    transform: translateX(115%) skewX(-10deg);
  }
}

@keyframes ink-breathe {
  from {
    opacity: 0.28;
    transform: scale(0.88);
  }
  to {
    opacity: 0.96;
    transform: scale(1.1);
  }
}

@media (max-width: 780px) {
  .gallery-stage,
  .gallery-stage.has-result {
    min-height: 360px;
  }

  .final-art {
    inset: 58px 22px 26px;
  }

  .download-btn {
    align-self: stretch;
  }
}
</style>
