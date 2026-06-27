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

function isValidUrl(url) {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

async function handleSave() {
  if (!config.value.api_key.trim()) {
    ElMessage.warning('请输入 API Key')
    return
  }
  if (!config.value.base_url.trim()) {
    ElMessage.warning('请输入 Base URL')
    return
  }
  if (!isValidUrl(config.value.base_url)) {
    ElMessage.warning('请输入有效的 URL 格式')
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
      <el-form-item>
        <template #label>
          <span class="label-text">API Key</span>
        </template>
        <el-input
          v-model="config.api_key"
          :type="showKey ? 'text' : 'password'"
          placeholder="sk-..."
          class="settings-input"
        >
          <template #append>
            <el-button @click="showKey = !showKey">
              {{ showKey ? '隐藏' : '显示' }}
            </el-button>
          </template>
        </el-input>
        <p class="field-hint">在对应平台的控制台获取</p>
      </el-form-item>

      <el-form-item>
        <template #label>
          <span class="label-text">Base URL</span>
        </template>
        <el-input
          v-model="config.base_url"
          placeholder="https://api.openai.com/v1"
          class="settings-input"
        />
        <p class="field-hint">API 接口地址，需兼容 OpenAI 格式</p>
      </el-form-item>

      <el-form-item>
        <template #label>
          <span class="label-text">Model ID</span>
        </template>
        <el-input
          v-model="config.model"
          placeholder="gpt-4o"
          class="settings-input"
        />
        <p class="field-hint">模型名称，如 gpt-4o、qwen-vl-max</p>
      </el-form-item>

      <el-form-item class="save-item">
        <el-button
          type="primary"
          :loading="loading"
          class="save-btn"
          @click="handleSave"
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

.label-text {
  font-weight: 500;
  color: var(--color-ink);
  font-size: var(--text-sm);
}

.field-hint {
  font-size: var(--text-xs);
  color: var(--color-ink-faint);
  margin-top: var(--space-1);
  line-height: 1.4;
}

.settings-input :deep(.el-input__wrapper) {
  border-radius: var(--radius-sm);
}

.settings-input :deep(.el-input__wrapper:focus-within) {
  box-shadow: 0 0 0 1px var(--color-vermilion) inset;
}

.save-item {
  margin-bottom: 0;
}

.save-btn {
  width: 100%;
  height: 40px;
  font-size: var(--text-base);
  letter-spacing: 1px;
  border-radius: var(--radius-sm);
}
</style>
