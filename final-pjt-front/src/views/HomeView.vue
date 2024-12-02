<template>
  <div>
    <div class="home-banner bg-thema position-relative d-none d-md-block">
      <div class="d-flex flex-column justify-content-center align-items-center h-100">
        <h1 class="banner-text mb-4">자산관리를 한번에!</h1>
        <h2 class="banner-text">상품 확인부터 가입까지 편하게 해보세요.</h2>
      </div>
      <div class="banner-link-container position-absolute top-100 start-50 translate-middle d-flex gap-3">
        <RouterLink
          :to="{name: 'product-deposit'}"
          class="fs-5 underline-none text-dark banner-link text-center"
        >
          <span>예적금 비교</span>
        </RouterLink>
        <RouterLink
          :to="{name: 'exchange'}"
          class="fs-5 underline-none text-dark banner-link text-center"
        >
          <span>환율 계산</span>
        </RouterLink>
        <RouterLink
          :to="{name: 'map'}"
          class="fs-5 underline-none text-dark banner-link text-center"
        >
          <span>주변 은행</span>
        </RouterLink>
      </div>
    </div>
    <div class="home-container">
      <HomeTable 
        v-for="category in categoryList"
        :key="category.id"
        :category="category"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import HomeTable from '@/components/HomeTable.vue'

const categoryList = ref([
  {id: 1, category: 'announcement', name: '공지사항'},
  {id: 2, category: 'free', name: '자유게시판' }
])
</script>

<style scoped>
.home-banner{
  width: 100%;
  height: 400px;
  margin-bottom: 180px;
}


.banner-link {
  width: 150px;
  height: 150px;
  line-height: 145px;
  margin: 30px;
  border: 1px solid #dce9be;
  border-radius: 30px;
  background-color: white;
}
@media (min-width: 998px) {
  .banner-link {
    width: 150px;
    height: 150px;
    line-height: 145px;
    margin: 80px;
    border: 1px solid #dce9be;
    border-radius: 30px;
    background-color: white;
  }
}
.underline-none {
  text-decoration: none;
}
.home-container {
  min-height: 80vh;
  margin: 30px 15%;
}
</style>