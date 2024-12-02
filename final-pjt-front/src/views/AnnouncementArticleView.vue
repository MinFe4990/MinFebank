<template>
  <div class="container">
      <div class="d-flex justify-content-end w-100 mb-3">
          <RouterLink class="nav-link" :to="{ name: 'make-article', params : {category :category}}" v-if="userStore.isSuperUser">
              게시글 작성
          </RouterLink>
      </div>
      <ArticleTable 
      :articleList="articleList"
      :category="category"
      />
      <div class="d-grid">
          <RouterLink class="btn btn-thema" :to="{ name: 'make-article', params : {category :category}}" v-if="userStore.isSuperUser">
              게시글 작성
          </RouterLink>
      </div>
      <LoadingSpinner v-if="isLoading"/>
  </div>
</template>

<script setup>
import { useArticleStore } from '@/stores/articles';
import { useUserStore } from '@/stores/user';
import { onMounted, ref } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ArticleTable from '@/components/ArticleTable.vue';

const userStore = useUserStore()
const articleStore = useArticleStore()

const category = ref('announcement')
const articleList = ref([]); // 로컬 상태로 관리
const isLoading = ref(true); // 로딩 상태를 로컬로 관리

onMounted(async () => {
  isLoading.value = true;
  try {
    const articles = await articleStore.getArticleList(category.value);
    articleList.value = articles; // 받아온 데이터를 로컬 상태에 저장
  } catch (err) {
    console.error("Error fetching articles:", err);
  } finally {
    isLoading.value = false;
  }
});

</script>

<style scoped>

</style>