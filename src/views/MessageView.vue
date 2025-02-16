<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
import Message from '@/components/Message.vue'
import MessageInput from '@/components/MessageInput.vue'

import Cookies from 'js-cookie'
import { onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { io } from 'socket.io-client'

const props = defineProps({
  endpoint: String,
})

const router = useRouter()
const channelId = useRoute().params.channelid

const messages = ref([])
const socket = io(new URL(props.endpoint as string).host, {
  query: {
    username: Cookies.get('username'),
    token: Cookies.get('token'),
  },
})
let listenSocket = false

async function sendMessage(content: string) {
  const formdata = new FormData()
  formdata.append('username', Cookies.get('username') as string)
  formdata.append('token', Cookies.get('token') as string)
  formdata.append('content', content)
  formdata.append('channel', channelId.toString())

  const response = await (
    await fetch(props.endpoint + 'channels/post', {
      method: 'post',
      body: formdata,
    })
  ).json()

  if (response['status'] != 201) {
    Cookies.remove('username')
    Cookies.remove('token')
    router.push('/')
  }
}

onMounted(async () => {
  const formdata = new FormData()
  formdata.append('username', Cookies.get('username') as string)
  formdata.append('token', Cookies.get('token') as string)
  formdata.append('channel', channelId as string)

  const response = await (
    await fetch(props.endpoint + 'channels/load', {
      method: 'post',
      body: formdata,
    })
  ).json()

  if (response['status'] != 200) {
    Cookies.remove('username')
    Cookies.remove('token')
    router.push('/')
  }

  messages.value = response['data'].reverse()
  listenSocket = true
})

socket.on('message', async (message) => {
  if (listenSocket) {
    if (message['channel'] == channelId) {
      messages.value = [
        {
          id: message['id'],
          content: message['content'],
          author: message['author'],
        },
      ].concat(messages.value)
    }
  }
})
</script>

<template>
  <Navbar pageDetails="Messages inside channel" />
  <ul class="messages">
    <li v-for="message in messages" :key="message.id" class="message">
      <Message :author="message.author" :content="message.content" />
    </li>
  </ul>
  <MessageInput :onSendMessage="sendMessage" />
</template>

<style scoped>
.message {
  display: block;
  margin: 5px;
}

.messages {
  margin-left: 18%;
  margin-top: 10%;
  max-height: 65vh;
  overflow-y: scroll;
  display: flex;
  flex-direction: column-reverse;
}

.message * {
  display: inline-block;
}
</style>
