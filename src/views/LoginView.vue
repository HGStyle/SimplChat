<script setup lang="ts">
// @ts-ignore
import Navbar from '@/components/Navbar.vue'
import LoginForm from '@/components/LoginForm.vue'

import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import Cookies from 'js-cookie'

const props = defineProps({
  endpoint: String,
})

const router = useRouter()

async function loginHandler(username: string, password: string, loginErrorMsg: ref) {
  const formdata = new FormData()
  formdata.append('username', username)
  formdata.append('password', password)

  const response = await (
    await fetch(props.endpoint + 'login', {
      method: 'post',
      body: formdata,
    })
  ).json()

  if (response['status'] == 201) {
    Cookies.set('username', username)
    Cookies.set('token', response['data'])
    router.push('/channels')
  } else {
    loginErrorMsg.value = response['message']
  }
}

onMounted(() => {
  if (Cookies.get('username')) {
    router.push('/channels')
  }
})
</script>

<template>
  <Navbar pageDetails="Login to chat" />
  <LoginForm :onLogin="loginHandler" />
</template>
