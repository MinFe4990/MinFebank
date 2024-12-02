<template>
  <table class="table">
    <thead>
      <tr>
        <th class="fs-head" scope="col">공시 시작일</th>
        <th class="fs-head" scope="col">금융 회사명</th>
        <th class="fs-head" scope="col">금융 상품명</th>
        <th class="fs-head" scope="col">6개월</th>
        <th class="fs-head" scope="col">12개월</th>
        <th class="fs-head" scope="col">24개월</th>
        <th class="fs-head" scope="col">36개월</th>
      </tr>
    </thead>
    <tbody>
      <ProductTableItem 
        v-for="product in filteredProductList"
        :key="product.code"
        :product="product"
        :category="category"
      />
    </tbody>
  </table>
</template>

<script setup>
import ProductTableItem from '@/components/ProductTableItem.vue'
import { computed } from 'vue'

const props = defineProps({
  productList: Array,
  selectFilter: String,
  category: String
})

const filteredProductList = computed(() => {
  return props.selectFilter === '전체 은행' ?
    props.productList :
    props.productList.filter(v => v.bank.name === props.selectFilter)
})
</script>

<style scoped>
.fs-head {
  font-size: 1rem;
}
</style>