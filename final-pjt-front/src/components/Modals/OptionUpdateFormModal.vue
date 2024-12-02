<template>
  <div class="modal fade" :id="`option-update-modal-${option.save_term}`" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="staticBackdropLabel">옵션 수정</h1>
          <button type="button" class="btn-close" ref="closeButtonRef" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label :for="`intr_type-${option.save_term}`">저축 금리 유형</label>
            <select class="form-select shadow-none" :id="`intr_type-${option.save_term}`" v-model="intr_type">
              <option value="S">단리</option>
              <option value="M">복리</option>
            </select>
          </div>
          <div class="mb-3">
            <label :for="`save_term-${option.save_term}`">저축 기간</label>
            <select class="form-select shadow-none" :id="`save_term-${option.save_term}`" v-model="save_term" disabled>
              <option value="1">1개월</option>
              <option value="3">3개월</option>
              <option value="6">6개월</option>
              <option value="12">12개월</option>
              <option value="24">24개월</option>
              <option value="36">36개월</option>
            </select>
          </div>
          <div class="mb-3" v-if="category === 'saving'">
            <label :for="`rsrv_type-${option.save_term}`">적립 방식</label>
            <select  class="form-select shadow-none" :id="`rsrv_type-${option.save_term}`" v-model="rsrv_type">
              <option value="S">정액적립식</option>
              <option value="F">자유적립식</option>
            </select>
          </div>
          <div class="mb-3">
            <label :for="`intr_rate-${option.save_term}`">저축 금리</label>
            <input type="number" class="form-control shadow-none" :id="`intr_rate-${option.save_term}`" v-model="intr_rate">
          </div>
          <div class="mb-3">
            <label :for="`intr_rate2-${option.save_term}`">최고 우대 금리</label>
            <input type="number" class="form-control shadow-none" :id="`intr_rate2-${option.save_term}`" v-model="intr_rate2">
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
          <button type="button" class="btn btn-primary" @click="optionUpdate">수정 하기</button>
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
  option: Object,
  category: String,
  code: String
})

const closeButtonRef = ref('')

const intr_type = ref(props.option?.intr_type)
const intr_type_name = computed(() => {
  return  intr_type.value === 'S' ? '단리' : '복리'
})
const save_term = ref(props.option?.save_term)
const intr_rate = ref(props.option?.intr_rate)
const intr_rate2 = ref(props.option?.intr_rate2)
const rsrv_type = ref(props.option?.rsrv_type)
const rsrv_type_name = computed(() => {
  return rsrv_type.value === 'S' ? '정액적립식' : '자유적립식'
})

const optionUpdate = async () => {
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