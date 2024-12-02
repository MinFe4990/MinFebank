<template>
  <nav class="navbar navbar-expand-lg sticky-top bg-body shadow-sm">
    <div class="container-fluid">
      <RouterLink class="navbar-brand logo" :to="{ name: 'home' }">MINFeBank</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-between" id="navbarSupportedContent">
        <ul class="navbar-nav nav-underline">
          <li class="nav-item">
            <RouterLink class="nav-link" active-class="active" :to="{ name: 'product-deposit'}">예적금 비교</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" active-class="active" :to="{ name: 'exchange' }">환율 계산기</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" active-class="active" :to="{ name: 'map' }">주변 은행</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" active-class="active" :to="{ name: 'free-article' }">커뮤니티</RouterLink>
          </li>
        </ul>
        <div class="navbar-nav" v-if="!userStore.isAuthenticated">
          <RouterLink class="nav-link" :to="{ name: 'login' }">로그인</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'signup' }">회원가입</RouterLink>
        </div>
        <div class="navbar-nav" v-else>
          <RouterLink class="nav-link" :to="{ name: 'my-profile' }">마이페이지</RouterLink>
          <span class="nav-link cursor" @click="logOut">로그아웃</span>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const logOut = () => {
  userStore.logOut()
}
</script>

<style scoped>

.cursor {
  cursor: pointer;
}
</style>