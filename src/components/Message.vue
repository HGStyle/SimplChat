<script setup>
const props = defineProps({
  content: String,
  author: String,
})
</script>

<template>
  <span class="message-author">{{ author }}</span>
  <p class="message-content">{{ content }}</p>
</template>

<style scoped>
.message-author {
  width: 120px;
}

.message-content {
  margin: 0;
}
</style>
