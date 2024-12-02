<template>
  <div class="modal fade" id="product-join-modal" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="staticBackdropLabel">상품 가입</h1>
          <button type="button" class="btn-close" ref="closeButtonRef" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class='form-check mb-3' v-for="option in options" :key="option.save_term">
            <input type="radio" class="form-check-input"
              :id="option.save_term" :value="option.save_term" name="option-select"
              v-model="selectOptions"
            >
            <label class="form-check-label" :for="option.save_term">
              {{ option.save_term }}개월 : 저축 금리 - {{ option.intr_rate }}% / 최대 우대 금리 - {{ option.intr_rate2 }}%
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
          <button type="button" class="btn btn-primary" @click="joinProduct">가입하기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProductStore } from '@/stores/product'
import { ref } from 'vue'

const productStore = useProductStore()

const props = defineProps({
  category: String,
  options: Array,
  productCode: String
})

const selectOptions = ref('')
const closeButtonRef = ref('')

const joinProduct = async () => {
  const payload = {
    products: props.category,
    prdt_cd: props.productCode,
    save_term: selectOptions.value
  }
  try {
    await  productStore.joinProduct(payload)
    if (closeButtonRef.value) {
        selectOptions.value = ''
        closeButtonRef.value.click()
      }
  } catch (err) {
    console.error('상품 가입 실패:', err)
  }
}
</script>

<style scoped>

</style>