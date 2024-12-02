<template>
  <div class="container">
    <div class="p-3">
      <h5 v-if="productStore.userJoinedProduct?.length > 0">내가 가입한 상품</h5>
      <h5 v-else>아직 가입한 상품이 없습니다.</h5>
      <UserJoinedProduct 
        v-if="productStore.userJoinedProduct?.length > 0"
        :joinedProducts="productStore.userJoinedProduct"
      />
    </div>
    <div class="p-3">
      <h5 v-if="productStore.chartData.labels.length > 0">가입한 상품 금리</h5>
      <UserProductChart
        v-if="productStore.chartData.labels.length > 0"
        :chartData="productStore.chartData"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useProductStore } from '@/stores/product'
import UserJoinedProduct from '@/components/UserJoinedProduct.vue'
import UserProductChart from '@/components/UserProductChart.vue'
const productStore = useProductStore()
onMounted(() => {
  productStore.getJoinedProduct()
  
})

</script>

<style scoped>

</style>