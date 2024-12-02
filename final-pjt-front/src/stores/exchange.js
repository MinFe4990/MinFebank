import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import Swal from 'sweetalert2'

export const useExchangeStore = defineStore('exchange', () => {
  const BASE_URL = 'http://127.0.0.1:8000/api/v1/exchanges'
  // states
  const exchanges = ref([])
  const currentExchage = ref(null)
  const lastExchanges = ref(null)
  const lastExchangeChartData = ref({
    labels: [],
    datasets: [
      {
        label: '구매가',
        data: []
      },
      {
        label: '판매가',
        data: []
      },
    ]
  })
  const countrys = ref(null)
  // getters

  // actions
  const getExchange = (country) => {
    axios({
      method: 'get',
      url: `${BASE_URL}/`,
      params: {
        range: 8
      }
    }).then((res) => {
      exchanges.value = res.data.data
      if(res.data.message) {
        Swal.fire({
          text: res.data.message,
          icon: 'warning',
          confirmButtonText: '확인'
        })
      }
    }).then((res) => {
      filteredExchanges(country)
      if(res.data.message) {
        Swal.fire({
          text: res.data.message,
          icon: 'warning',
          confirmButtonText: '확인'
        })
      }
    }).catch((err) => {
      console.log(err)
    })
  }

  const filteredExchanges = (country) => {
    const filteredExchange  = exchanges.value
      .filter(v => v.country.name === country)
      .sort((a, b) => new Date(b.date.date) - new Date(a.date.date))
    currentExchage.value = filteredExchange[0]
    lastExchanges.value = filteredExchange
    const tempLabels = []
    const tempBuyData = []
    const tempSellData = []
    filteredExchange.forEach((v) => {
      tempLabels.unshift(v.date.date)
      tempBuyData.unshift(v.buy)
      tempSellData.unshift(v.sell)
    })
    lastExchangeChartData.value = {
      labels: tempLabels,
      datasets: [
        { label: '구매가', data: tempSellData },
        { label: '판매가', data: tempBuyData }
      ]
    }
  }

  const getCountry = () => {
    axios({
      method: 'get',
      url: `${BASE_URL}/country/`
    }).then((res) => {
      countrys.value = res.data
    }).catch((err) => {
      console.log(err)
    })
  }
  return {
    exchanges,
    currentExchage,
    lastExchanges,
    lastExchangeChartData,
    countrys,
    getExchange,
    filteredExchanges,
    getCountry
  }
})
