<script setup>
import { ref } from 'vue'

const props = defineProps({
  onCreateChannel: Function,
})

const channelName = ref(null)

async function createChannel() {
  await props.onCreateChannel(channelName.value)
}
</script>

<template>
  <section>
    <h2>Create a new channel</h2>
    <div class="inputs">
      <input type="text" placeholder="Channel name" v-model="channelName" />
    </div>
    <br />
    <button @click="createChannel">Create channel</button>
  </section>
</template>

<style scoped>
section {
  margin-left: 25%;
  margin-top: 10%;
}

section * {
  max-width: 300px;
  max-height: 20px;
  display: block;
  font-size: 15px;
  text-align: center;
}

section input {
  width: 97%;
  height: 98%;
}

section button {
  padding-bottom: 18px;
}

.inputs,
section button {
  width: 300px;
  margin: 5px;
}

.inputs {
  text-align: unset;
}
</style>
