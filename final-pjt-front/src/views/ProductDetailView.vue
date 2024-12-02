<template>
  <div class="container">
    <div class="d-flex justify-content-between">
      <h4>{{ title }} 상세</h4>
      <div class='d-flex gap-3'>
        <RouterLink class="btn btn-primary"
          v-if="userStore.isSuperUser"
          :to="{ name: 'product-update', params: { category: route.params.category, code: route.params.code }}"
        >
          옵션 수정
        </RouterLink>
        <button class="btn btn-secondary" 
          v-if="userStore.isAuthenticated"
          data-bs-toggle="modal" data-bs-target="#product-join-modal"
        >
          가입하기
        </button>
      </div>
    </div>
    <div class="p-5">
      <div class="row mb-3">
        <div class="col-2">
          <p class="fw-bold">공시시작일</p>
        </div>
        <div class="col-10">
          <p>{{ product?.start_day }}</p>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-2">
          <p class="fw-bold">은행명</p>
        </div>
        <div class="col-10">
          <p>{{ product?.bank.name }}</p>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-2">
          <p class="fw-bold">상품명</p>
        </div>
        <div class="col-10">
          <p>{{ product?.name }}</p>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-2">
          <p class="fw-bold">가입제한</p>
        </div>
        <div class="col-10">
          <p>{{ product?.join_deny.join_deny }}</p>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-2">
          <p class="fw-bold">우대조건</p>
        </div>
        <div class="col-10">
          <p>{{ product?.special_cnd }}</p>
        </div>
      </div>
    </div>
    <ProductJoinModal 
      :category="route.params.category"
      :options="product?.options"
      :productCode="route.params.code"
    />
  </div>
</template>

<script setup>
import { useRoute, RouterLink } from 'vue-router'
import { computed, onMounted, ref } from 'vue'
import { useProductStore } from '@/stores/product'
import { useUserStore } from '@/stores/user'
import ProductJoinModal from '@/components/Modals/ProductJoinModal.vue'

const route = useRoute()

const productStore = useProductStore()
const userStore = useUserStore()

const title = ref(null)
onMounted(() => {
  if ( route.params.category === 'deposit' && productStore.depositList === null ) {
    productStore.getDepositList()
  }
  if ( route.params.category === 'saving' && productStore.savingList === null ) {
    productStore.getSavingList()
  }
  title.value = route.params.category === 'deposit' ? '예금' : '적금'
})
const product = computed(() => {
  if (route.params.category === 'deposit') {
    return productStore.depositList?.find(v => v.code === route.params.code)
  } else {
    return productStore.savingList?.find(v => v.code === route.params.code)
  }
})
</script>

<style scoped>

</style>