<template>
  <AppNavbar />
  <RouterView />
  <ChatBotModal v-if="userStore.isAuthenticated && !userStore.isSuperUser"/>
  <AppFooter />
</template>

<script setup>
import { RouterView } from 'vue-router'
import AppNavbar from '@/components/AppNavbar.vue'
import AppFooter from '@/components/AppFooter.vue'
import ChatBotModal from '@/components/Modals/ChatBotModal.vue';
import { useUserStore } from './stores/user';
const userStore = useUserStore()
</script>

<style scoped>
.container {
    min-height: 80vh;
    margin-top: 20px;
  }
</style>
