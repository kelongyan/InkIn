<script setup>
import { reactive, watch } from 'vue'
import { MagicStick } from '@element-plus/icons-vue'

const props = defineProps({
  styles: { type: Array, default: () => [] },
  modelValue: { type: String, default: 'comic' },
})

const emit = defineEmits(['update:modelValue'])

const paramValues = reactive({})

// 监听风格变化：为新风格初始化参数默认值
watch(
  () => props.modelValue,
  (id) => {
    const style = props.styles.find((s) => s.id === id)
    if (!style) return
    for (const p of style.params || []) {
      if (paramValues[p.key] === undefined) {
        paramValues[p.key] = p.default ?? ''
      }
    }
  },
  { immediate: true }
)

function selectStyle(id) {
  emit('update:modelValue', id)
}

function getStyleParams(styleId) {
  const style = props.styles.find((s) => s.id === styleId)
  return (style && style.params) || []
}

// 供父组件收集参数（排除空字符串）
function collectParams() {
  const out = {}
  for (const [key, value] of Object.entries(paramValues)) {
    if (value !== '' && value !== undefined && value !== null) {
      out[key] = value
    }
  }
  return out
}

defineExpose({ collectParams })
</script>

<template>
  <div class="style-picker">
    <div class="style-picker-head">
      <span class="pick-label">Pick a Style · 选一种画法</span>
    </div>

    <div class="style-grid">
      <button
        v-for="style in styles"
        :key="style.id"
        type="button"
        class="style-card"
        :class="[
          `family-${style.family || 'classic'}`,
          { active: modelValue === style.id },
        ]"
        @click="selectStyle(style.id)"
      >
        <span class="style-card-mark" aria-hidden="true">
          <el-icon v-if="style.family === 'classic'"><MagicStick /></el-icon>
          <span v-else class="seal-char">拾</span>
        </span>
        <span class="style-card-body">
          <strong>{{ style.name }}</strong>
          <em>{{ style.tagline }}</em>
          <small>{{ style.description }}</small>
        </span>
      </button>
    </div>

    <div v-if="getStyleParams(modelValue).length" class="params-panel">
      <p class="params-title">风格参数</p>
      <el-form label-position="top" size="default" class="params-form">
        <el-form-item v-for="p in getStyleParams(modelValue)" :key="p.key">
          <template #label>
            <span class="param-label">{{ p.label }}</span>
          </template>

          <el-select
            v-if="p.type === 'select'"
            v-model="paramValues[p.key]"
            placeholder="请选择"
            class="param-control"
          >
            <el-option
              v-for="opt in p.options"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>

          <el-input
            v-else-if="p.type === 'text'"
            v-model="paramValues[p.key]"
            :placeholder="p.hint || '选填'"
            clearable
            class="param-control"
          />

          <el-switch
            v-else-if="p.type === 'switch'"
            v-model="paramValues[p.key]"
            class="param-control"
          />

          <p v-if="p.hint" class="param-hint">{{ p.hint }}</p>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.style-picker {
  width: 100%;
}

.style-picker-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.pick-label {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-muted);
}

.style-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.style-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px;
  text-align: left;
  color: var(--color-ink);
  background: rgba(255, 250, 240, 0.62);
  border: 1px solid var(--color-line);
  border-radius: 16px;
  cursor: pointer;
  transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease,
    background 0.22s ease;
}

.style-card:hover {
  transform: translateY(-2px);
  border-color: rgba(201, 71, 45, 0.5);
  box-shadow: var(--shadow-float);
}

.style-card.active {
  background: rgba(255, 250, 240, 0.95);
  border-color: var(--color-vermilion);
  box-shadow: 0 0 0 1px var(--color-vermilion) inset, var(--shadow-float);
}

.style-card-mark {
  flex: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  color: var(--color-paper);
  background: var(--color-ink);
  font-size: 16px;
}

.style-card.family-shijing .style-card-mark {
  background: var(--color-vermilion);
}

.seal-char {
  font-family: var(--font-display);
  font-weight: 900;
}

.style-card-body {
  display: grid;
  gap: 3px;
  min-width: 0;
}

.style-card-body strong {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 900;
  line-height: 1.25;
}

.style-card-body em {
  font-style: normal;
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.1em;
  color: var(--color-vermilion-deep);
}

.style-card-body small {
  margin-top: 3px;
  color: var(--color-ink-soft);
  font-size: 12px;
  line-height: 1.55;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.params-panel {
  margin-top: 12px;
  padding: 14px 16px 6px;
  border: 1px dashed rgba(64, 43, 28, 0.3);
  border-radius: 16px;
  background: rgba(255, 250, 240, 0.5);
}

.params-title {
  margin-bottom: 8px;
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-muted);
}

.params-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0 14px;
}

.param-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-ink-soft);
}

.param-control {
  width: 100%;
}

.param-hint {
  margin-top: 4px;
  color: var(--color-muted);
  font-size: 11px;
  line-height: 1.5;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  background: rgba(255, 250, 240, 0.85);
  box-shadow: 0 0 0 1px rgba(64, 43, 28, 0.16) inset;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--color-vermilion) inset;
}

:deep(.el-select__wrapper) {
  border-radius: 10px;
  background: rgba(255, 250, 240, 0.85);
  box-shadow: 0 0 0 1px rgba(64, 43, 28, 0.16) inset;
}

@media (max-width: 780px) {
  .style-grid {
    grid-template-columns: 1fr 1fr;
  }

  .params-form {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .style-grid {
    grid-template-columns: 1fr;
  }
}
</style>