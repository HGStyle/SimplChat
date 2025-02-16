<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
import ChannelListing from '@/components/ChannelListing.vue'
import ChannelCreation from '@/components/ChannelCreation.vue'

import Cookies from 'js-cookie'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  endpoint: String,
})

const router = useRouter()
const userChannels = ref(null)

function viewChannel(channelId: string) {
  router.push('/messages/' + channelId)
}

async function createChannel(name: string) {
  const formdata = new FormData()
  formdata.append('username', Cookies.get('username'))
  formdata.append('token', Cookies.get('token'))
  formdata.append('name', name)

  const response = await (
    await fetch(props.endpoint + 'channels/new', {
      method: 'post',
      body: formdata,
    })
  ).json()

  if (response['status'] != 201) {
    Cookies.remove('username')
    Cookies.remove('token')
    router.push('/')
  }

  userChannels.value.push({
    id: response['data'],
    name: name,
  })
}

onMounted(async () => {
  if (!Cookies.get('username') || !Cookies.get('token')) {
    router.push('/')
  }

  const formdata = new FormData()
  formdata.append('username', Cookies.get('username'))
  formdata.append('token', Cookies.get('token'))

  const response = await (
    await fetch(props.endpoint + 'channels/list', {
      method: 'post',
      body: formdata,
    })
  ).json()

  if (response['status'] != 200) {
    Cookies.remove('username')
    Cookies.remove('token')
    router.push('/')
  }

  userChannels.value = response['data']
})
</script>

<template>
  <Navbar pageDetails="Available channels" />
  <ChannelListing :channels="userChannels" :onViewChannel="viewChannel" />
  <ChannelCreation :onCreateChannel="createChannel" />
</template>
