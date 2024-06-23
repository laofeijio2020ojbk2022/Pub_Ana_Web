import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// import AboutView from "@/views/AboutView.vue";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/test',
    name: 'test',
    component: () => import('../views/TestView.vue')
  },
  {
    path: '/active-user',
    name: 'active-user',
    component: () => import('../views/protrait/ActiveUserView.vue')
  },
  {
    path: '/active-blogger',
    name: 'active-blogger',
    component: () => import('../views/protrait/NewActiveBloggerView.vue')
  },
  {
    path: '/protrait',
    name: 'protrait',
    component: () => import('../views/protrait/ProtraitPaintingView.vue')
  },
  {
    path: '/emotion',
    name: 'emotion',
    component: () => import('@/views/search/EmotionAnalysisView.vue')
  },
  {
    path: '/participle',
    name: 'participle',
    component: () => import('@/views/search/ParticipleAnalysisView.vue')
  },
  {
    path: '/personal',
    name: 'personal',
    component: () => import('@/views/admin/PersonalView.vue')
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('@/views/admin/AdminView.vue')
  },
  {
    path: '/cookies',
    name: 'cookies',
    component: () => import('@/views/crawler/CookiesView.vue')
  },
  {
    path: '/crawler',
    name: 'crawler',
    component: () => import('@/views/crawler/CrawlerView.vue')
  },
  {
    path: '/save',
    name: 'save',
    component: () => import('@/views/crawler/SaveView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
