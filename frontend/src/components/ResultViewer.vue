<script setup>
import { ref } from 'vue'

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
    <div v-if="loading" class="loading-state">
      <el-icon class="is-loading" :size="48"><i class="el-icon-loading" /></el-icon>
      <p>正在生成漫画，请稍候...</p>
      <p class="tip">这可能需要 30-60 秒</p>
    </div>

    <div v-else-if="resultUrl" class="result-content">
      <div class="image-compare">
        <div class="image-box">
          <p class="label">原图</p>
          <img v-if="originalUrl" :src="originalUrl" alt="原图" />
        </div>
        <div class="image-box">
          <p class="label">漫画</p>
          <img :src="resultUrl" alt="漫画" />
        </div>
      </div>
      <el-button type="primary" @click="downloadImage" style="margin-top: 16px">
        下载漫画
      </el-button>
    </div>

    <div v-else class="empty-state">
      <p>上传图片并生成漫画后，结果将在这里显示</p>
    </div>
  </div>
</template>

<style scoped>
.result-viewer {
  width: 100%;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-state,
.empty-state {
  text-align: center;
  color: #909399;
  padding: 40px;
}

.loading-state .tip {
  font-size: 12px;
  color: #c0c4cc;
  margin-top: 8px;
}

.result-content {
  text-align: center;
}

.image-compare {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.image-box {
  flex: 1;
  min-width: 200px;
  max-width: 400px;
}

.image-box .label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.image-box img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
</style>
