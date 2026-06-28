<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadImage } from '../utils/api.js'

const emit = defineEmits(['upload-start', 'upload-success', 'upload-error'])

const fileInput = ref(null)
const isDragging = ref(false)
const previewUrl = ref('')
const uploading = ref(false)

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
const MAX_SIZE = 10 * 1024 * 1024

function validateFile(file) {
  if (!ALLOWED_TYPES.includes(file.type)) {
    ElMessage.error('仅支持 JPG / PNG / GIF / WebP 格式')
    return false
  }
  if (file.size > MAX_SIZE) {
    ElMessage.error('文件大小不能超过 10MB')
    return false
  }
  return true
}

function openFilePicker() {
  fileInput.value?.click()
}

function handleKeydown(e) {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault()
    openFilePicker()
  }
}

function handleFile(file) {
  if (!validateFile(file)) return

  const reader = new FileReader()
  reader.onload = (e) => {
    previewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)

  uploadFile(file)
}

async function uploadFile(file) {
  uploading.value = true
  emit('upload-start')
  try {
    const res = await uploadImage(file)
    if (res.success) {
      ElMessage.success('照片已装裱')
      emit('upload-success', res.data)
    } else {
      ElMessage.error(res.error || '上传失败')
      emit('upload-error')
    }
  } catch (err) {
    ElMessage.error('上传失败: ' + (err.message || '网络错误'))
    emit('upload-error')
  } finally {
    uploading.value = false
  }
}

function onDrop(e) {
  e.preventDefault()
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) handleFile(file)
}

function onDragOver(e) {
  e.preventDefault()
  isDragging.value = true
}

function onDragLeave() {
  isDragging.value = false
}

function onFileChange(e) {
  const file = e.target.files[0]
  if (file) handleFile(file)
  e.target.value = ''
}
</script>

<template>
  <div class="image-uploader">
    <div
      class="uploader-frame"
      :class="{ dragging: isDragging, 'has-image': previewUrl, 'is-uploading': uploading }"
      role="button"
      tabindex="0"
      aria-label="上传照片"
      @drop="onDrop"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      @click="openFilePicker"
      @keydown="handleKeydown"
    >
      <div class="tape tape-left" aria-hidden="true"></div>
      <div class="tape tape-right" aria-hidden="true"></div>

      <div v-if="uploading" class="upload-state">
        <div class="ink-loader" aria-hidden="true"></div>
        <p class="state-title">正在装裱</p>
        <p class="state-hint">把照片固定到创作台...</p>
      </div>

      <div v-else-if="previewUrl" class="preview-state">
        <div class="preview-card">
          <img :src="previewUrl" alt="已选择照片预览" />
        </div>
        <div class="preview-caption">
          <span>Source Photo</span>
          <strong>点击替换照片</strong>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="frame-icon" aria-hidden="true">
          <span></span>
        </div>
        <p class="state-title">把照片放上画架</p>
        <p class="state-hint">拖入图片，或点击选择 JPG / PNG / GIF / WebP</p>
        <p class="state-limit">最大 10MB</p>
      </div>
    </div>

    <input
      ref="fileInput"
      type="file"
      accept="image/jpeg,image/png,image/gif,image/webp"
      class="file-input"
      @change="onFileChange"
    />
  </div>
</template>

<style scoped>
.image-uploader {
  width: 100%;
}

.uploader-frame {
  position: relative;
  min-height: 250px;
  padding: 20px;
  border: 1px dashed rgba(64, 43, 28, 0.36);
  border-radius: 22px;
  background:
    linear-gradient(145deg, rgba(255, 250, 240, 0.92), rgba(235, 218, 190, 0.62)),
    var(--color-paper);
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.24s ease, border-color 0.24s ease, box-shadow 0.24s ease;
}

.uploader-frame::before {
  content: "";
  position: absolute;
  inset: 16px;
  border: 1px solid rgba(64, 43, 28, 0.14);
  border-radius: 16px;
  pointer-events: none;
}

.uploader-frame::after {
  content: "";
  position: absolute;
  left: 22px;
  right: 22px;
  bottom: 22px;
  height: 12px;
  border-radius: 999px;
  background: radial-gradient(ellipse at center, rgba(66, 41, 20, 0.2), transparent 70%);
  filter: blur(6px);
  opacity: 0.45;
}

.uploader-frame:hover,
.uploader-frame:focus-visible,
.uploader-frame.dragging {
  outline: none;
  transform: translateY(-2px);
  border-color: rgba(201, 71, 45, 0.72);
  box-shadow: var(--shadow-float);
}

.uploader-frame.dragging {
  background:
    linear-gradient(145deg, rgba(250, 231, 225, 0.96), rgba(255, 250, 240, 0.92)),
    var(--color-paper);
}

.uploader-frame.has-image {
  border-style: solid;
}

.tape {
  position: absolute;
  top: 14px;
  width: 58px;
  height: 18px;
  background: rgba(230, 204, 165, 0.64);
  border: 1px solid rgba(64, 43, 28, 0.1);
  box-shadow: 0 4px 10px rgba(66, 41, 20, 0.1);
  z-index: 2;
}

.tape-left {
  left: 24px;
  transform: rotate(-7deg);
}

.tape-right {
  right: 24px;
  transform: rotate(7deg);
}

.upload-state,
.empty-state,
.preview-state {
  position: relative;
  z-index: 1;
  min-height: 202px;
}

.upload-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.frame-icon {
  position: relative;
  width: 78px;
  height: 94px;
  margin-bottom: 14px;
  border: 2px solid var(--color-ink);
  border-radius: 6px;
  transform: rotate(-3deg);
  box-shadow: 10px 10px 0 rgba(201, 71, 45, 0.12);
}

.frame-icon::before {
  content: "";
  position: absolute;
  inset: 12px;
  border: 1px solid rgba(34, 26, 20, 0.28);
}

.frame-icon span {
  position: absolute;
  inset: 34px 26px;
  border-radius: 50%;
  background: var(--color-vermilion);
}

.state-title {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 900;
  color: var(--color-ink);
}

.state-hint {
  max-width: 260px;
  margin-top: 8px;
  color: var(--color-ink-soft);
  font-size: 13px;
}

.state-limit {
  margin-top: 14px;
  color: var(--color-muted);
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.ink-loader {
  width: 74px;
  height: 74px;
  margin-bottom: 18px;
  border-radius: 50%;
  background:
    radial-gradient(circle at 48% 48%, var(--color-vermilion) 0 18%, transparent 19%),
    radial-gradient(circle at 50% 50%, rgba(201, 71, 45, 0.2) 0 42%, transparent 43%);
  animation: ink-pulse 0.9s ease-in-out infinite alternate;
}

.preview-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 18px;
}

.preview-card {
  position: relative;
  width: min(100%, 260px);
  margin: 0 auto;
  padding: 12px 12px 34px;
  background: var(--color-paper);
  border: 1px solid rgba(64, 43, 28, 0.18);
  box-shadow: 0 18px 34px rgba(66, 41, 20, 0.18);
  transform: rotate(-1.5deg);
}

.preview-card img {
  width: 100%;
  max-height: 150px;
  display: block;
  object-fit: contain;
  background: rgba(34, 26, 20, 0.04);
}

.preview-caption {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: var(--color-muted);
  font-size: 12px;
}

.preview-caption span {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.preview-caption strong {
  color: var(--color-vermilion-deep);
  font-weight: 700;
}

.file-input {
  display: none;
}

@media (max-width: 780px) {
  .uploader-frame {
    min-height: 260px;
    padding: 22px;
  }

  .upload-state,
  .empty-state,
  .preview-state {
    min-height: 210px;
  }
}
</style>
