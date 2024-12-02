<template>
  <div class="container d-flex flex-column align-itmes-center">
    <select class="form-select shadow-none mb-3" v-model="selectFilter">
      <option value="전체 은행">전체 은행</option>
      <option :value="bank.name" v-for="bank in productStore.bankList" :key="bank.code">
        {{ bank.name }}
      </option>
    </select>
    <ProductTable 
      :productList="productStore.depositList"
      :selectFilter="selectFilter"
      :category="category"
    />
    <LoadingSpinner v-if="isLoading"/>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useProductStore } from '@/stores/product'
import ProductTable from '@/components/ProductTable.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'


const productStore = useProductStore()

const selectFilter = ref('전체 은행')
const category = ref('deposit')

const isLoading = computed(() => {
  return productStore.depositList === null
})

onMounted(() => {
  productStore.getDepositList()
  productStore.getBankList()
})
</script>

<style scoped>

</style>