import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './user'
import Swal from 'sweetalert2'

export const useProductStore = defineStore('product', () => {
  const BASE_URL = 'http://127.0.0.1:8000/api/v1/products'
  const userStore = useUserStore()
  // states
  const depositList = ref(null)
  const savingList = ref(null)
  const bankList = ref(null)
  const product = ref(null)
  const userJoinedProduct = ref(null)
  const chartData = ref({
    labels: [],
    datasets: [
      {
        label: '저축 금리',
        data: [],
      },
      {
        label: '최대 우대 금리',
        data: []
      }
    ]
  })
  // getters

  // actions
  const getDepositList = async () => {
    try {
      const response = await axios({
        method: 'get',
        url: `${BASE_URL}/deposit/`
      });
      depositList.value = response.data; // 응답 데이터를 설정
      return response.data; // 필요시 데이터를 반환
    } catch (error) {
      console.error("Error fetching deposit list:", error);
      throw error; // 필요시 에러를 다시 던짐
    }
  };
  const getSavingList = async () => {
    try {
      const response = await axios({
        method: 'get',
        url: `${BASE_URL}/saving/`
      });
      savingList.value = response.data; // 응답 데이터를 설정
      return response.data; // 필요시 데이터를 반환
    } catch (error) {
      console.error("Error fetching saving list:", error);
      throw error; // 필요시 에러를 다시 던짐
    }
  };
  const getBankList = async () => {
    try {
      const res = await axios({
        method: 'get',
        url: `${BASE_URL}/banks/`,
      });
      bankList.value = res.data; // 데이터를 가져와 bankList에 저장
    } catch (err) {
      console.error("은행 리스트 가져오기 실패:", err);
    }
  };
  const joinProduct = async (payload) => {
    const { products, prdt_cd, save_term } = payload
    try {
      const res = await axios({
        method: 'post',
        url: `${BASE_URL}/sign/`,
        data: { products, prdt_cd, save_term},
        headers: {
          Authorization: `Token ${userStore.token}`
        }
      })
      return res.data
    } catch (err) {
      if( err.response.data.error === 'Deposit product already Signed' || err.response.data.error === 'Saving product already Signed') {
        Swal.fire({
          text: '이미 가입한 상품 입니다.',
          icon: 'error',
          confirmButtonText: '확인',
          confirmButtonColor: '##dce9be'
        })
      }
      console.log(err.response.data.error)
      console.log(err)
    }
  }

  const getJoinedProduct = async () => {
    try {
      const response = await axios({
        method: 'get',
        url: `${BASE_URL}/sign/`,
        headers: {
          Authorization: `Token ${userStore.token}`
        }
      });
  
      // 데이터 재가공
      const tempData = [];
      const labels = [];
      const intrRateData = [];
      const intrRate2Data = [];
  
      // 예금 데이터 처리
      response.data.signed_deposit.forEach((v) => {
        tempData.push({ category: 'deposit', product: v.deposit, option: v.options[0].deposit_option });
        labels.push(v.deposit.name);
        intrRateData.push(v.options[0].deposit_option.intr_rate);
        intrRate2Data.push(v.options[0].deposit_option.intr_rate2);
      });
  
      // 적금 데이터 처리
      response.data.signed_saving.forEach((v) => {
        tempData.push({ category: 'saving', product: v.saving, option: v.options[0].saving_option });
        labels.push(v.saving.name);
        intrRateData.push(v.options[0].saving_option.intr_rate);
        intrRate2Data.push(v.options[0].saving_option.intr_rate2);
      });
  
      // 가공된 데이터 할당
      userJoinedProduct.value = tempData;
      chartData.value.labels = labels;
      chartData.value.datasets[0].data = intrRateData;
      chartData.value.datasets[1].data = intrRate2Data;
  
      return tempData; // 필요시 데이터 반환
    } catch (error) {
      console.error("Error fetching joined products:", error);
      throw error; // 필요시 에러를 다시 던짐
    }
  };

  const optionUpdate = async (payload) => {
    const { products, code, save_term, intr_type, intr_type_name, rsrv_type, rsrv_type_name, intr_rate, intr_rate2 } = payload
    if ( products === 'deposit' ) {
      await axios({
        method: 'post',
        url: `${BASE_URL}/change/option/`,
        data: { products, code, save_term, intr_type, intr_type_name, intr_rate, intr_rate2 }
      }).then((res) => {
        getDepositList()
      }).catch((err) => {
        console.log(err)
      })
    } else {
      await axios({
        method: 'post',
        url: `${BASE_URL}/change/option/`,
        data: { products, code, save_term, intr_type, intr_type_name, rsrv_type, rsrv_type_name, intr_rate, intr_rate2 }
      }).then((res) => {
        getSavingList()
      }).catch((err) => {
        console.log(err)
      })
    }
  }

  
  return {
    depositList,
    savingList,
    bankList,
    product,
    userJoinedProduct,
    chartData,
    getDepositList,
    getSavingList,
    getBankList,
    joinProduct,
    getJoinedProduct,
    optionUpdate,
  }
})