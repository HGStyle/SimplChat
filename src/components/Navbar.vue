<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Cookies from 'js-cookie'

const props = defineProps({
  pageDetails: String,
})

const router = useRouter()

function logout() {
  Cookies.remove('username')
  Cookies.remove('token')
  router.push('/')
}

const rightSideRef = ref(null)
const navButtonCounts = ref(0)
</script>

<template>
  <nav>
    <h1>SimplChat</h1>
    <h2>{{ pageDetails }}</h2>
    <div class="rightside" v-if="Cookies.get('username')">
      <h2 @click="logout">Logout</h2>
    </div>
  </nav>
</template>

<style scoped>
nav {
  display: flex;
  border-bottom: 1px solid black;
  background-color: var(--secondary-color);
}

nav > * {
  border-right: 1px solid black;
  padding: 10px;
}

h1,
h2,
h3 {
  margin: 0;
  width: auto;
  height: auto;
}

nav .rightside * {
  cursor: pointer;
  -webkit-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

nav .rightside {
  margin-left: auto;
  border-right: 0;
  border-left: 1px solid black;
}
</style>
