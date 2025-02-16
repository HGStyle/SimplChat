import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import ChannelView from '@/views/ChannelView.vue'
import MessageView from '@/views/MessageView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/channels',
      name: 'channels',
      component: ChannelView,
    },
    {
      path: '/messages/:channelid',
      name: 'messages',
      component: MessageView,
    },
  ],
})

export default router
