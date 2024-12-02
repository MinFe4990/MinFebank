<template>
  <div class="container">
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <RouterLink class="nav-link" exact-active-class="active" :to="{ name: 'my-profile'}">내 정보</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink class="nav-link" active-class="active" :to="{ name: 'my-product' }">가입한 상품</RouterLink>
      </li>
    </ul>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>

<style scoped>

</style>