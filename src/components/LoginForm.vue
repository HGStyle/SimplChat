<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps({
  onLogin: Function,
})

const username = ref(null)
const usernameTyped = ref(false)
const password = ref(null)
const passwordTyped = ref(false)
const loginErrorMsg = ref(null)

watch(username, () => {
  usernameTyped.value = true
  loginErrorMsg.value = null
})

watch(password, () => {
  passwordTyped.value = true
  loginErrorMsg.value = null
})

async function onButtonClick() {
  if (username.value && password.value) {
    await props.onLogin(username.value, password.value, loginErrorMsg)
  }
}
</script>

<template>
  <section>
    <div class="inputs">
      <input type="text" v-model="username" placeholder="Your username" />
      <input type="password" v-model="password" placeholder="Your password" />
    </div>
    <br /><br />
    <span class="error" v-if="usernameTyped && !username">You must enter a username to login</span>
    <span class="error" v-if="passwordTyped && !password">You must enter a password to login</span>
    <span class="error" v-if="loginErrorMsg">{{ loginErrorMsg }}</span>
    <button v-if="username && password" @click="onButtonClick">Login as {{ username }}</button>
  </section>
</template>

<style>
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

.error {
  color: red;
}
</style>
