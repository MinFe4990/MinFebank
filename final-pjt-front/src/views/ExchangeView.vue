<template>
  <div class="container my-5">
    <div class="mb-5">
      <h5 class="mb-3">환율 계산기</h5>
      <div class="row mb-3 gy-3">
        <div class="col-4">
          <select class="form-select shadow-none" v-model="country" @change="filteredExchanges">
            <option 
              :value="country.name" 
              v-for="country in exchangeStore.countrys" 
              :key="country.id"
            >
              {{ country.name }} - {{ country.currency }}
            </option>
          </select>
        </div>
        <div class="col-8">
          <input type="number" class="form-control shadow-none" v-model="selectMoney" @input="selectMoneyToWon(exchangeStore.currentExchage?.buy)">
        </div>
        <div class="col-12">
          <div class="input-group">
            <span class="input-group-text">￦</span>
            <input type="number" class="form-control shadow-none" v-model="won" @input="wonToSelectMoney(exchangeStore.currentExchage?.sell)">
          </div>
        </div>
      </div>
      <div>
        <p>[{{ exchangeStore.currentExchage?.date.date }}] {{ exchangeStore.currentExchage?.country.name }} - {{ exchangeStore.currentExchage?.country.currency }} 환율</p>
        <p class="d-flex gap-3">
          <span>판매가 :  {{ exchangeStore.currentExchage?.buy }}</span>
          <span>구매가 : {{ exchangeStore.currentExchage?.sell }} 입니다.</span>
        </p>
        <p class="fs-sm">주의사항: 일본 엔화와 인도네시아 루피아는 100단위입니다.</p>
      </div>
    </div>
    <ExchangeLast 
      :exchangeList="exchangeStore.lastExchanges"
      :chartData="exchangeStore.lastExchangeChartData"
      :country="country"
    />
  </div>
</template>

<script setup>
import { useExchangeStore } from '@/stores/exchange'
import { onMounted, ref } from 'vue'
import ExchangeLast from '@/components/ExchangeLast.vue'

const exchangeStore = useExchangeStore()

const country = ref('미국')

const won = ref(0)
const selectMoney = ref(0)

const selectMoneyToWon = (rate) => {
  won.value = (selectMoney.value * rate).toFixed(2)
  if (country.value === '일본' || country.value === '인도네시아') {
    won.value /= 100
  }
}

const wonToSelectMoney = (rate) => {
  selectMoney.value = (won.value / rate).toFixed(2)
  if (country.value === '일본' || country.value === '인도네시아') {
    selectMoney.value *= 100
  }
}

const filteredExchanges = () => {
  won.value = 0
  selectMoney.value = 0
  exchangeStore.filteredExchanges(country.value)
}

onMounted(() => {
  exchangeStore.getExchange(country.value)
  exchangeStore.getCountry()
})
</script>

<style scoped>
.fs-sm {
  font-size: 0.9rem;
}
</style>