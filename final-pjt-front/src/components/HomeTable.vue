<template>
  <table class="table mb-5">
    <thead>
      <tr>
        <th class="d-flex justify-content-between p-2">
          <span>{{ category.name }}</span>
          <RouterLink
            :to="{ name: `${category.category}-article` }"
            class="underline-none"
          >
            +
          </RouterLink>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="article in articleList" :key="article.id">
        <td>
          <RouterLink
            :to="{name: 'article-detail', params: { category: category.category, id: article.id,}}"
            class="underline-none"
          >
            {{ article.title }}
          </RouterLink>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { ref, onMounted } from 'vue';

const articleStore = useArticleStore()

const props = defineProps({
  category: Object
})

const articleList = ref(null)

onMounted(async () => {
  try {
    const articles = await articleStore.getArticleList(props.category.category);
    articleList.value = articles.slice(0, 5); // 상위 5개 데이터만 저장
  } catch (err) {
    console.error("Error fetching articles: ", err);
  }
})
</script>

<style scoped>
.underline-none {
  text-decoration: none;
  color: black;
}
</style>