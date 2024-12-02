<template>
  <div class="mb-3">
    <h5>환율 보기</h5>
    <ExchangeLastChart 
      v-if="exchangeStore.lastExchangeChartData.labels.length > 0"
      :key="JSON.stringify(exchangeStore.lastExchangeChartData)"
      :chartData="exchangeStore.lastExchangeChartData"
    />
    <!-- <table class="table">
      <thead>
        <tr>
          <th>날짜</th>
          <th>구매</th>
          <th>판매</th>
        </tr>
      </thead>
      <tbody class="table-group-divider">
        <tr v-for="exchage in exchangeList" :key="exchage.date.date">
          <th>{{ exchage.date.date }}</th>
          <td>{{ exchage.buy }}</td>
          <td>{{ exchage.sell }}</td>
        </tr>
      </tbody>
    </table> -->
  </div>
</template>

<script setup>
import { useExchangeStore } from '@/stores/exchange'
import ExchangeLastChart from './ExchangeLastChart.vue'

const exchangeStore =  useExchangeStore()

const props = defineProps({
  exchangeList: Array,
  country: String
})



</script>

<style scoped>

</style>