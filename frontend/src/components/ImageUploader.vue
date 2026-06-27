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
      class="drop-zone"
      :class="{ dragging: isDragging, 'has-image': previewUrl }"
      @drop="onDrop"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      @click="$refs.fileInput.click()"
    >
      <!-- 上传中 -->
      <div v-if="uploading" class="upload-loading">
        <el-icon class="is-loading" :size="40"><Loading /></el-icon>
        <p>上传中...</p>
      </div>

      <!-- 已有预览 -->
      <div v-else-if="previewUrl" class="preview">
        <img :src="previewUrl" alt="预览" />
        <p class="hint">点击重新选择</p>
      </div>

      <!-- 空状态占位 -->
      <div v-else class="placeholder">
        <div class="placeholder-icon">
          <el-icon :size="48"><Upload /></el-icon>
        </div>
        <p class="placeholder-text">拖拽图片到这里，或 <em>点击选择</em></p>
        <p class="placeholder-tip">支持 JPG / PNG / GIF / WebP，最大 10MB</p>
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

.drop-zone {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
  padding: 48px var(--space-5);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: var(--color-bg-warm);
}

.drop-zone:hover {
  border-color: var(--color-vermilion);
  background-color: var(--color-vermilion-light);
}

.drop-zone.dragging {
  border-color: var(--color-vermilion);
  border-style: solid;
  background-color: var(--color-vermilion-light);
  transform: scale(1.01);
}

.drop-zone.has-image {
  padding: var(--space-5);
}

/* 空状态 */
.placeholder-icon {
  color: var(--color-ink-faint);
  margin-bottom: var(--space-3);
  transition: color 0.3s ease;
}

.drop-zone:hover .placeholder-icon {
  color: var(--color-vermilion);
}

.placeholder-text {
  color: var(--color-ink-light);
  font-size: var(--text-base);
  margin-bottom: var(--space-2);
}

.placeholder-text em {
  color: var(--color-vermilion);
  font-style: normal;
  font-weight: 500;
}

.placeholder-tip {
  font-size: var(--text-xs);
  color: var(--color-ink-faint);
}

/* 预览图 */
.preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-card);
}

.preview .hint {
  font-size: var(--text-xs);
  color: var(--color-ink-faint);
  margin-top: var(--space-2);
}

/* 上传加载 */
.upload-loading {
  color: var(--color-vermilion);
}

.upload-loading p {
  margin-top: var(--space-2);
  font-size: var(--text-sm);
}

/* 隐藏文件 input */
.file-input {
  display: none;
}
</style>
