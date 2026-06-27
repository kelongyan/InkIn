<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['upload-success'])

const isDragging = ref(false)
const previewUrl = ref('')
const uploading = ref(false)

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
const MAX_SIZE = 10 * 1024 * 1024 // 10MB

function validateFile(file) {
  if (!ALLOWED_TYPES.includes(file.type)) {
    ElMessage.error('仅支持 JPG/PNG/GIF/WebP 格式')
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

  // 预览
  const reader = new FileReader()
  reader.onload = (e) => {
    previewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)

  // 上传
  uploadFile(file)
}

async function uploadFile(file) {
  uploading.value = true
  try {
    const { uploadImage } = await import('../utils/api.js')
    const res = await uploadImage(file)
    if (res.success) {
      ElMessage.success('上传成功')
      emit('upload-success', res.data)
    } else {
      ElMessage.error(res.error || '上传失败')
    }
  } catch (err) {
    ElMessage.error('上传失败: ' + (err.message || '网络错误'))
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
      <div v-if="uploading" class="upload-loading">
        <el-icon class="is-loading" :size="40"><i class="el-icon-loading" /></el-icon>
        <p>上传中...</p>
      </div>
      <div v-else-if="previewUrl" class="preview">
        <img :src="previewUrl" alt="预览" />
        <p class="hint">点击重新选择</p>
      </div>
      <div v-else class="placeholder">
        <el-icon :size="48"><i class="el-icon-upload" /></el-icon>
        <p>拖拽图片到这里，或 <em>点击选择</em></p>
        <p class="tip">支持 JPG/PNG/GIF/WebP，最大 10MB</p>
      </div>
    </div>
    <input
      ref="fileInput"
      type="file"
      accept="image/jpeg,image/png,image/gif,image/webp"
      style="display: none"
      @change="onFileChange"
    />
  </div>
</template>

<style scoped>
.image-uploader {
  width: 100%;
}

.drop-zone {
  border: 2px dashed #dcdfe6;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #fafafa;
}

.drop-zone:hover,
.drop-zone.dragging {
  border-color: #409eff;
  background: #ecf5ff;
}

.drop-zone.has-image {
  padding: 20px;
}

.placeholder {
  color: #909399;
}

.placeholder em {
  color: #409eff;
  font-style: normal;
}

.placeholder .tip {
  font-size: 12px;
  color: #c0c4cc;
  margin-top: 8px;
}

.preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
}

.preview .hint {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.upload-loading {
  color: #409eff;
}
</style>
