<script setup>
import { ref } from 'vue'

const props = defineProps({
  channels: ref,
  onViewChannel: Function,
})
</script>

<template>
  <ul>
    <li v-for="channel in props.channels" :key="channel.id">
      <button @click="onViewChannel(channel.id)">{{ channel.name }}</button>
    </li>
  </ul>
</template>

<style>
li {
  list-style-type: none;
  display: inline-flex;
}

li button {
  background-color: transparent;
  border: 1px solid black;
  border-radius: 5px;
  font-size: 20px;
  margin: 5px;
  display: inline;
}
</style>
