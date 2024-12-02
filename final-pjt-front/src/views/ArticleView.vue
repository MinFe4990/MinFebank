<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center">
      <!-- 게시판 탭 -->
      <ul class="nav nav-tabs mb-0">
        <li class="nav-item">
          <RouterLink 
            class="nav-link" :class="{active: isActive === 'announcement'}" 
            :to="{ name: 'announcement-article'}"
            @click="changeActive('announcement')"
          >
            공지사항
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink 
            class="nav-link" :class="{active: isActive === 'free'}" 
            :to="{ name: 'free-article'}"
            @click="changeActive('free')"
          >
            자유 게시판
          </RouterLink>
        </li>
      </ul>
      <!-- 원하는 게시판 추가 가능 but type을 만들어야함 -->

    </div>

    <!-- RouterView 컴포넌트 -->
    <RouterView />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterView, RouterLink, useRoute } from 'vue-router';

const route  = useRoute()

const isActive = ref(route.path.split('/')[2])

const changeActive = (category) => {
  isActive.value = category
}
</script>

<style scoped>
/* 추가적인 스타일이 필요하면 여기에 작성 */
</style>
