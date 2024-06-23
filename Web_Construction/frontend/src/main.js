import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'//引用组件库的样式
// import * as Icons from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 创建store对象
// .use(store)
// <h2>{{ $store.state.name }}</h2>
// import { createStore } from 'vuex'

const app = createApp(App)
app.use(router).use(ElementPlus).mount('#app')
app.config.globalProperties.$axios = axios
app.config.globalProperties.$echarts = echarts
// // 通过遍历的方式注册所有 svg组件，会牺牲一点点性能
// for (let i in Icons) {
//   app.component(i, Icons[i])
//   console.log(i, Icons[i])
// }


