<script setup>
import { ref } from 'vue'

const props = defineProps({
  onSendMessage: Function,
})

const message = ref(null)

async function sendMessage() {
  if (document.getElementById('messageInput').value) {
    document.getElementById('messageInput').value = ''
    props.onSendMessage(message.value)
  }
}
</script>

<template>
  <section>
    <div class="inputs">
      <input type="text" id="messageInput" v-model="message" placeholder="Enter your message" />
    </div>
    <button @click="sendMessage">Send</button>
  </section>
</template>

<style scoped>
section {
  margin-left: 25%;
  margin-top: 0 !important;
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
