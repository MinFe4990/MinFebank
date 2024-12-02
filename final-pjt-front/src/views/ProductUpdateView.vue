<template>
  <div class="p-3">
    <h5 class="mb-3">{{ product?.bank.name }} - {{ product?.name }} 옵션 수정</h5>
    <table class="table">
      <thead>
        <tr class="text-center">
          <th>금리 유형</th>
          <th v-if="route.params.category === 'saving'">적립 방식</th>
          <th>저축 기간</th>
          <th>저축 금리</th>
          <th>최고 우대 금리</th>
          <td><button class="btn btn-sm" data-bs-toggle="modal" :data-bs-target="`#option-add-modal`">추가하기</button></td>
        </tr>
      </thead>
      <tbody>
        <template v-for="option in product?.options.sort((a, b) => a.save_term - b.save_term)" :key="`${route.params.code}-${option.save_term}`">
          <tr class="text-center">
            <td>{{ option.intr_type_name }}</td>
            <td v-if="route.params.category === 'saving'">{{ option?.rsrv_type_name }}</td>
            <td>{{ option.save_term }}</td>
            <td>{{ option.intr_rate }}</td>
            <td>{{ option.intr_rate2 }}</td>
            <td><button class="btn btn-sm" data-bs-toggle="modal" :data-bs-target="`#option-update-modal-${option.save_term}`">수정하기</button></td>
          </tr>
        </template>
      </tbody>
    </table>
    <div>
      <OptionUpdateFormModal
        v-for="option in product?.options.sort((a, b) => a.save_term - b.save_term)" 
        :key="`${route.params.code}-${option.save_term}`"
        :option="option"
        :category="route.params.category"
        :code="route.params.code"
      />
      <OptionAddFormModal 
        :category="route.params.category"
        :code="route.params.code"
      />
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed, onMounted, ref } from 'vue'
import { useProductStore } from '@/stores/product'
import { useUserStore } from '@/stores/user'
import OptionUpdateFormModal from '@/components/Modals/OptionUpdateFormModal.vue'
import OptionAddFormModal from '@/components/Modals/OptionAddFormModal.vue'


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