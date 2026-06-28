<script setup>
import { onMounted, ref } from 'vue'
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
      ElMessage.success('器材箱已保存')
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
    <section class="settings-intro">
      <p>Provider Setup</p>
      <h2>接上你的画笔</h2>
      <span>支持 OpenAI 兼容接口，配置只保存在本地后端。</span>
    </section>

    <el-form label-position="top" size="large" class="settings-form">
      <el-form-item>
        <template #label>
          <span class="label-text">API Key</span>
        </template>
        <el-input
          v-model="config.api_key"
          :type="showKey ? 'text' : 'password'"
          placeholder="sk-..."
          autocomplete="off"
        >
          <template #append>
            <el-button @click="showKey = !showKey">
              {{ showKey ? '隐藏' : '显示' }}
            </el-button>
          </template>
        </el-input>
        <p class="field-hint">从模型服务商控制台复制密钥。</p>
      </el-form-item>

      <el-form-item>
        <template #label>
          <span class="label-text">Base URL</span>
        </template>
        <el-input
          v-model="config.base_url"
          placeholder="https://api.openai.com/v1"
        />
        <p class="field-hint">需要兼容 OpenAI Chat Completions 或 Images 接口。</p>
      </el-form-item>

      <el-form-item>
        <template #label>
          <span class="label-text">Model ID</span>
        </template>
        <el-input
          v-model="config.model"
          placeholder="gpt-4o"
        />
        <p class="field-hint">例如 gpt-4o、gpt-image-1、qwen-vl-max。</p>
      </el-form-item>

      <el-form-item class="save-item">
        <el-button
          type="primary"
          :loading="loading"
          class="save-btn"
          @click="handleSave"
        >
          保存器材箱
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.api-settings {
  width: 100%;
}

.settings-intro {
  margin-bottom: 26px;
  padding: 18px;
  border: 1px solid rgba(64, 43, 28, 0.14);
  border-radius: 18px;
  background: rgba(255, 250, 240, 0.58);
}

.settings-intro p {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.18em;
  color: var(--color-muted);
  text-transform: uppercase;
}

.settings-intro h2 {
  margin-top: 6px;
  font-family: var(--font-display);
  font-size: 30px;
  line-height: 1;
  color: var(--color-ink);
}

.settings-intro span {
  display: block;
  margin-top: 10px;
  color: var(--color-ink-soft);
  font-size: 13px;
}

.settings-form {
  display: grid;
  gap: 8px;
}

.label-text {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: var(--color-ink-soft);
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.field-hint {
  margin-top: 6px;
  color: var(--color-muted);
  font-size: 12px;
  line-height: 1.5;
}

.save-item {
  margin-top: 6px;
  margin-bottom: 0;
}

.save-btn {
  width: 100%;
  height: 46px;
  border-radius: 999px;
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 900;
  letter-spacing: 0.08em;
}

:deep(.el-input__wrapper),
:deep(.el-input-group__append) {
  border-radius: 14px;
  background: rgba(255, 250, 240, 0.78);
  box-shadow: 0 0 0 1px rgba(64, 43, 28, 0.16) inset;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--color-vermilion) inset;
}

:deep(.el-input__inner) {
  color: var(--color-ink);
}
</style>
