<template>
  <div class="modal fade" id="option-add-modal" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="staticBackdropLabel">옵션 수정</h1>
          <button type="button" class="btn-close" ref="closeButtonRef" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="add-intr_type">저축 금리 유형</label>
            <select class="form-select shadow-none" id="add-intr_type" v-model="intr_type">
              <option value="S">단리</option>
              <option value="M">복리</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="add-save_term">저축 기간</label>
            <select class="form-select shadow-none" id="add-save_term" v-model="save_term">
              <option value="1">1개월</option>
              <option value="3">3개월</option>
              <option value="6">6개월</option>
              <option value="12">12개월</option>
              <option value="24">24개월</option>
              <option value="36">36개월</option>
            </select>
          </div>
          <div class="mb-3" v-if="category === 'saving'">
            <label for="add-rsrv_type">적립 방식</label>
            <select  class="form-select shadow-none" id="add-rsrv_type`" v-model="rsrv_type">
              <option value="S">정액적립식</option>
              <option value="F">자유적립식</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="add-intr_rate">저축 금리</label>
            <input type="number" class="form-control shadow-none" id="add-intr_rate" v-model="intr_rate">
          </div>
          <div class="mb-3">
            <label for="add-intr_rate2">최고 우대 금리</label>
            <input type="number" class="form-control shadow-none" id="add-intr_rate2" v-model="intr_rate2">
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
          <button type="button" class="btn btn-primary" @click="optionAdd">추가 하기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useProductStore } from '@/stores/product'

const productStore = useProductStore()

const props = defineProps({
  category: String,
  code: String
})

const closeButtonRef = ref('')

const intr_type = ref('S')
const intr_type_name = computed(() => {
  return  intr_type.value === 'S' ? '단리' : '복리'
})
const save_term = ref('1')
const intr_rate = ref(0)
const intr_rate2 = ref(0)
const rsrv_type = ref('S')
const rsrv_type_name = computed(() => {
  return rsrv_type.value === 'S' ? '정액적립식' : '자유적립식'
})
const optionAdd = async () => {
  const payload = {
    products: props.category,
    code: props.code,
    save_term: save_term.value,
    intr_type: intr_type.value,
    intr_type_name: intr_type_name.value,
    rsrv_type: rsrv_type.value,
    rsrv_type_name: rsrv_type_name.value,
    intr_rate: intr_rate.value,
    intr_rate2: intr_rate2.value
  }
  await productStore.optionUpdate(payload)
  closeButtonRef.value.click()
}
</script>

<style scoped>

</style>