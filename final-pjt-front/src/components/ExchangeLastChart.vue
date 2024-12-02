<template>
  <div>
    <Line
      :options="chartOptions"
      :data="chartData"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, PointElement, LineElement, CategoryScale, LinearScale, Colors } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, PointElement, LineElement, CategoryScale , LinearScale, Colors)

const props = defineProps({
  chartData: Object
})

const chartOptions = ref({
  responsive: true,
  // maintainAspectRatio: false
})

watch(
  () => props.chartData,
  (newData) => {
    if (chartInstance) {
      chartInstance.data = newData;
      chartInstance.update();
    }
  }
)
</script>

<style scoped>

</style>