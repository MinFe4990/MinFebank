<template>
  <div class="container">
    <ul class="nav nav-tabs mb-3">
      <li class="nav-item">
        <RouterLink class="nav-link" :class="{ active: isActive === 'deposit' }" :to="{ name: 'product-deposit'}">예금</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink class="nav-link" :class="{ active: isActive === 'saving' }" :to="{ name: 'product-saving'}">적금</RouterLink>
      </li>
    </ul>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView, RouterLink, useRoute, onBeforeRouteUpdate } from 'vue-router'
import { ref } from 'vue'

const route = useRoute()

const isActive = ref(route.path.split('/')[2])

onBeforeRouteUpdate((to, from) => {
  isActive.value = to.path.split('/')[2]
})
</script>

<style scoped>

</style>