<script setup lang="ts">
import LoginView from '@/views/LoginView.vue'
import ChannelView from '@/views/ChannelView.vue'
import MessageView from '@/views/MessageView.vue'

import { useRoute, useRouter } from 'vue-router'
import { onMounted } from 'vue'
import Cookies from 'js-cookie'

const route = useRoute()
const router = useRouter()
const endpoint = 'http://localhost:5000/'

async function checkLogin(username, token) {
  const formdata = new FormData()
  formdata.append('username', username)
  formdata.append('token', token)

  const response = await (
    await fetch(endpoint + 'check', {
      method: 'post',
      body: formdata,
    })
  ).json()

  if (response['status'] != 200) {
    logoutUser()
  }
}

function logoutUser() {
  Cookies.remove('username')
  Cookies.remove('token')
  router.push('/')
}

onMounted(() => {
  if (route.name == 'login') {
    return
  }

  if (Cookies.get('username') || Cookies.get('token')) {
    checkLogin(Cookies.get('username'), Cookies.get('token'))
  } else {
    router.push('/')
  }
})
</script>

<template>
  <LoginView :endpoint="endpoint" v-if="route.name == 'login'" />
  <ChannelView :endpoint="endpoint" v-else-if="route.name == 'channels'" />
  <MessageView :endpoint="endpoint" v-else-if="route.name == 'messages'" />
  <h1 v-else>Page not found</h1>
</template>
