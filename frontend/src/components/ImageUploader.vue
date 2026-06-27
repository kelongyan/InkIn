<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, Loading } from '@element-plus/icons-vue'
import { uploadImage } from '../utils/api.js'

const emit = defineEmits(['upload-start', 'upload-success', 'upload-error'])

const isDragging = ref(false)
const previewUrl = ref('')
const uploading = ref(false)

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
const MAX_SIZE = 10 * 1024 * 1024 // 10MB

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
      :class="{ dragging: isDragging, 'has-image': previewUrl }"
      @drop="onDrop"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      @click="$refs.fileInput.click()"
    >
      <!-- 四角装饰 -->
      <span class="corner corner-tl"></span>
      <span class="corner corner-tr"></span>
      <span class="corner corner-bl"></span>
      <span class="corner corner-br"></span>

      <!-- 上传中 -->
      <div v-if="uploading" class="state uploading">
        <el-icon class="is-loading" :size="40"><Loading /></el-icon>
        <p>墨水渲染中...</p>
      </div>

      <!-- 已有预览 — 画卷卷轴样式 -->
      <div v-else-if="previewUrl" class="scroll-preview">
        <div class="scroll-rod scroll-rod-top"></div>
        <div class="scroll-body">
          <img :src="previewUrl" alt="预览" />
        </div>
        <div class="scroll-rod scroll-rod-bottom"></div>
        <p class="reselect-hint">点击重新选择</p>
      </div>

      <!-- 空状态 -->
      <div v-else class="state empty">
        <div class="brush-icon">
          <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M48 8L20 36l-4 16 16-4L60 20 48 8z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            <path d="M20 36l-4 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M8 56h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="52" cy="12" r="3" fill="currentColor" opacity="0.3"/>
          </svg>
        </div>
        <p class="empty-title">将照片放上画布</p>
        <p class="empty-sub">拖拽图片到这里，或 <em>点击选择</em></p>
        <p class="empty-tip">JPG / PNG / GIF / WebP &middot; 最大 10MB</p>
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
  border: 2px solid var(--color-border);
  border-radius: 12px;
  padding: 48px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s ease;
  background: var(--color-bg-warm);
  overflow: hidden;
}

.canvas-wrap:hover {
  border-color: var(--color-vermilion);
  background: var(--color-vermilion-light);
}

.canvas-wrap.dragging {
  border-color: var(--color-vermilion);
  border-width: 3px;
  background: var(--color-vermilion-light);
  animation: ink-spread 0.6s ease-out;
}

.canvas-wrap.has-image {
  padding: 24px;
  background: var(--color-surface);
}

/* ====== 四角装饰 ====== */
.corner {
  position: absolute;
  width: 20px;
  height: 20px;
  border-color: var(--color-ink);
  border-style: solid;
  opacity: 0.12;
  transition: opacity 0.3s ease;
}
.canvas-wrap:hover .corner {
  opacity: 0.3;
  border-color: var(--color-vermilion);
}
.corner-tl { top: 10px; left: 10px; border-width: 2px 0 0 2px; }
.corner-tr { top: 10px; right: 10px; border-width: 2px 2px 0 0; }
.corner-bl { bottom: 10px; left: 10px; border-width: 0 0 2px 2px; }
.corner-br { bottom: 10px; right: 10px; border-width: 0 2px 2px 0; }

/* ====== 通用状态 ====== */
.state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

/* ====== 空状态 ====== */
.brush-icon {
  width: 56px;
  height: 56px;
  color: var(--color-ink-faint);
  margin-bottom: 8px;
  transition: color 0.3s ease;
}
.canvas-wrap:hover .brush-icon {
  color: var(--color-vermilion);
}
.brush-icon svg {
  width: 100%;
  height: 100%;
}

.empty-title {
  font-family: var(--font-serif);
  font-size: 18px;
  color: var(--color-ink);
  font-weight: 600;
  letter-spacing: 2px;
}

.empty-sub {
  color: var(--color-ink-light);
  font-size: 14px;
}
.empty-sub em {
  color: var(--color-vermilion);
  font-style: normal;
  font-weight: 500;
  border-bottom: 1px dashed var(--color-vermilion);
  padding-bottom: 1px;
}

.empty-tip {
  font-size: 12px;
  color: var(--color-ink-faint);
  margin-top: 4px;
}

/* ====== 上传中 ====== */
.uploading {
  color: var(--color-vermilion);
  padding: 32px 0;
}
.uploading p {
  font-size: 14px;
  color: var(--color-ink-light);
}

/* ====== 卷轴预览 ====== */
.scroll-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}

.scroll-rod {
  width: calc(100% + 32px);
  height: 10px;
  background: linear-gradient(
    180deg,
    var(--color-border) 0%,
    var(--color-bg-warm) 40%,
    var(--color-border) 100%
  );
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  flex-shrink: 0;
}

.scroll-body {
  width: 100%;
  padding: 8px 0;
  display: flex;
  justify-content: center;
}

.scroll-body img {
  max-width: 100%;
  max-height: 360px;
  border-radius: 4px;
  box-shadow: 0 2px 16px rgba(44, 44, 44, 0.1);
}

.reselect-hint {
  font-size: 12px;
  color: var(--color-ink-faint);
  margin-top: 12px;
}

/* ====== 隐藏 input ====== */
.file-input {
  display: none;
}
</style>
