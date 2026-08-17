import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import 'element-plus/dist/index.css'
import './style.css'
import App from './App.vue'

const app = createApp(App)

// 全局错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err)
  console.error('Error Info:', info)

  // 可以在这里添加错误上报逻辑
  // 例如：sendErrorToServer(err, info)

  // 显示用户友好的错误提示
  import('element-plus').then(({ ElMessage }) => {
    ElMessage.error('应用出现错误，请刷新页面重试')
  })
}

// 全局警告处理（开发环境）
if (import.meta.env.DEV) {
  app.config.warnHandler = (msg, instance, trace) => {
    console.warn('Vue Warning:', msg)
    console.warn('Trace:', trace)
  }
}

app.use(ElementPlus, { locale: zhCn })
app.mount('#app')
