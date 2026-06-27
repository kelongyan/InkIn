<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getConfig, saveConfig } from '../utils/api.js'

const emit = defineEmits(['config-saved'])

const config = ref({
  api_key: '',
  base_url: 'https://api.openai.com/v1',
  model: 'gpt-4o',
})
const loading = ref(false)
const showKey = ref(false)

onMounted(async () => {
  try {
    const res = await getConfig()
    if (res.success && res.data) {
      config.value = { ...config.value, ...res.data }
    }
  } catch (err) {
    console.error('加载配置失败:', err)
  }
})

async function handleSave() {
  if (!config.value.api_key.trim()) {
    ElMessage.warning('请输入 API Key')
    return
  }
  if (!config.value.base_url.trim()) {
    ElMessage.warning('请输入 Base URL')
    return
  }
  if (!config.value.model.trim()) {
    ElMessage.warning('请输入 Model ID')
    return
  }

  loading.value = true
  try {
    const res = await saveConfig(config.value)
    if (res.success) {
      ElMessage.success('配置已保存')
      emit('config-saved', res.data)
    } else {
      ElMessage.error(res.error || '保存失败')
    }
  } catch (err) {
    ElMessage.error('保存失败: ' + (err.message || '网络错误'))
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="api-settings">
    <el-form label-position="top" size="default">
      <el-form-item label="API Key">
        <el-input
          v-model="config.api_key"
          :type="showKey ? 'text' : 'password'"
          placeholder="sk-..."
        >
          <template #append>
            <el-button @click="showKey = !showKey">
              {{ showKey ? '隐藏' : '显示' }}
            </el-button>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="Base URL">
        <el-input
          v-model="config.base_url"
          placeholder="https://api.openai.com/v1"
        />
      </el-form-item>

      <el-form-item label="Model ID">
        <el-input
          v-model="config.model"
          placeholder="gpt-4o"
        />
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          :loading="loading"
          @click="handleSave"
          style="width: 100%"
        >
          保存配置
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.api-settings {
  width: 100%;
}
</style>
