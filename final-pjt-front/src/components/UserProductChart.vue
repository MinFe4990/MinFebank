<template>
  <div>
    <Bar
      :key="chartData" 
      id="my-chart-id"
      :options="chartOptions"
      :data="chartData"
    />
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Colors } from 'chart.js'
import { ref } from 'vue'

defineProps({
  chartData: Object
})

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Colors)

const chartOptions = ref({
  responsive: true
})


</script>

<style scoped>

</style>