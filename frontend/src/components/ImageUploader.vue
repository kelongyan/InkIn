<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadImage } from '../utils/api.js'

const emit = defineEmits(['upload-start', 'upload-success', 'upload-error'])

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
      ElMessage.success('上传成功')
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
}
</script>

<template>
  <div class="image-uploader">
    <div
      class="canvas-wrap"
      :class="{ dragging: isDragging, 'has-image': previewUrl, 'is-uploading': uploading }"
      @drop="onDrop"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      @click="$refs.fileInput.click()"
    >
      <!-- 上传中：halftone 网点 -->
      <div v-if="uploading" class="state uploading-state">
        <div class="halftone-spinner"></div>
        <p class="state-label">渲染中...</p>
      </div>

      <!-- 已有预览 -->
      <div v-else-if="previewUrl" class="preview-wrap">
        <div class="preview-frame img-panel">
          <img :src="previewUrl" alt="预览" />
        </div>
        <p class="reselect-hint">点击重新选择</p>
      </div>

      <!-- 空状态 -->
      <div v-else class="state empty-state">
        <div class="upload-icon">
          <svg viewBox="0 0 40 40" fill="none">
            <rect x="4" y="4" width="32" height="32" rx="4" stroke="currentColor" stroke-width="1.5"/>
            <path d="M20 12v16M12 20h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </div>
        <p class="state-title">拖入照片，或点击选择</p>
        <p class="state-hint">JPG / PNG / GIF / WebP &middot; 最大 10MB</p>
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

/* ====== 画布外壳 ====== */
.canvas-wrap {
  position: relative;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  padding: 48px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: var(--color-canvas);
  overflow: hidden;
}

.canvas-wrap:hover {
  border-color: var(--color-pop);
  border-style: solid;
  background: var(--color-pop-light);
}

.canvas-wrap.dragging {
  border-color: var(--color-pop);
  border-style: solid;
  border-width: 3px;
  background: var(--color-pop-light);
  transform: scale(1.01);
}

.canvas-wrap.has-image {
  border-style: solid;
  border-color: var(--color-border);
  padding: 20px;
  background: var(--color-panel);
}

.canvas-wrap.has-image:hover {
  border-color: var(--color-pop);
}

.canvas-wrap.is-uploading {
  border-style: solid;
  border-color: var(--color-pop);
  background: var(--color-pop-light);
}

/* ====== 通用状态 ====== */
.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

/* ====== 空状态 ====== */
.upload-icon {
  width: 48px;
  height: 48px;
  color: var(--color-halftone);
  margin-bottom: 8px;
  transition: color 0.3s ease;
}
.canvas-wrap:hover .upload-icon {
  color: var(--color-pop);
}
.upload-icon svg {
  width: 100%;
  height: 100%;
}

.state-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--color-ink);
  letter-spacing: 0.5px;
}

.state-hint {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-muted);
  letter-spacing: 0.5px;
}

/* ====== 上传中 ====== */
.uploading-state {
  padding: 24px 0;
}

.halftone-spinner {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-image: radial-gradient(circle, var(--color-pop) 1.5px, transparent 1.5px);
  background-size: 6px 6px;
  animation: halftone-reveal 1.5s ease-in-out infinite alternate;
  opacity: 0.6;
}

.state-label {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--color-muted);
  margin-top: 4px;
}

/* ====== 预览 ====== */
.preview-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.preview-frame {
  max-width: 100%;
  border-radius: var(--radius-sm);
}
.preview-frame img {
  max-height: 340px;
  object-fit: contain;
  border-radius: var(--radius-sm);
}

.reselect-hint {
  font-size: var(--text-xs);
  color: var(--color-muted);
}

/* ====== 隐藏 input ====== */
.file-input {
  display: none;
}
</style>
