import { ref, computed,watchEffect } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Swal from 'sweetalert2'


export const useUserStore = defineStore('user', () => {
  const BASE_URL = 'http://127.0.0.1:8000/accounts'
  const router = useRouter()
  // state
  const token = ref(null)
  // getters
  const isAuthenticated = computed(() =>{
    return token.value !== null
  })
  const user = ref(null)

  const isSuperUser =  ref(null)

  const updateUser = async () => {
    if (isAuthenticated.value) {
      const userData = await getUserData();
      user.value = userData?.username || null;
      const superuser = await getSuperUser();
      isSuperUser.value = superuser?.is_superuser
    } else {
      user.value = null;
      isSuperUser.value = false
    }
  };
  
  // watchEffect로 `isAuthenticated` 변화 감지
  watchEffect(() => {
    updateUser();
  });

  // actions
  const signUp = (payload) => {  // 회원 가입
    const { username, password1, password2, last_name, first_name, email, postcode, address, address_detail } = payload
    axios({
      method: 'post',
      url: `${BASE_URL}/signup/`,
      data: {
        username, password1, password2, last_name, first_name, email, postcode, address, address_detail
      }
    }).then((res) => {
      Swal.fire({
        text: '회원가입 되었습니다.',
        icon: 'success',
        confirmButtonText : '확인',
        confirmButtonColor: '#dce9be',
      }).then(() => {
        const password = password1
        logIn({ username, password })
      })
    }).catch((err) => {
      Swal.fire({
        text: '다시 시도해주세요',
        icon: 'error',
        showConfirmButton: false,
        timer: 1500
      }).then(() => {
        console.log(err)
      })
    })
  }

  const logIn = (payload) => {  // 로그인
    const { username , password } = payload
    axios({
      method: 'post',
      url: `${BASE_URL}/login/`,
      data: { username, password }
    }).then((res) => {
      token.value = res.data.key
      Swal.fire({
        text: '로그인 되었습니다.',
        icon: 'success',
        confirmButtonText : '확인',
        confirmButtonColor: '#dce9be',
      }).then(() => {
        router.push({ name: 'home' })
      })
    }).catch((err) => {
      Swal.fire({
        text: '다시 시도해주세요',
        icon: 'error',
        showConfirmButton: false,
        timer: 1500
      })
    })
  }

  const logOut = () => {  // 로그아웃
    axios({
      method: 'post',
      url: `${BASE_URL}/logout/`,
    }).then((res) => {
      Swal.fire({
        text: '로그아웃 되었습니다.',
        icon: 'success',
        confirmButtonText: '확인',
        confirmButtonColor: '#dce9be',
      }).then(() => {
        token.value = null
        router.push({ name: 'login' })
      })
    }).catch((err) => {
      console.log(err)
    })
  }

  const getUserData = async () => { // 유저 정보 불러오기
    if (token.value === null) {
      Swal.fire({
        text: '로그인이 필요합니다.',
        icon: 'warning',
        confirmButtonText: '확인',
        confirmButtonColor: '#dce9be',
      })
      return null
    }
    try {
      const res = await axios({
        method: 'get',
        url: `${BASE_URL}/user/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      return res.data
    } catch (err) {
      console.log(err)
    }
  }

  const userUpdate = (payload) => {  // 회원 정보 수정
    const { username, password1, password2, last_name, first_name, email, postcode, address, address_detail } = payload
    axios({
      method: 'put',
      url: `${BASE_URL}/user/`,
      data: {
        username, password1, password2, last_name, first_name, email, postcode, address, address_detail
      },
      headers:{
        Authorization : `Token ${token.value}`
      }
    }).then((res) => {
      Swal.fire({
        text: '회원 정보가 변경되었습니다.',
        icon: 'success',
        confirmButtonText: '확인',
        confirmButtonColor: '#dce9be',
      })
    }).catch((err) => {
      Swal.fire({
        text: '다시 시도해주세요',
        icon: 'error',
        showConfirmButton: false,
        timer: 1500
      }).then(() => {
        console.log(err)
      })
    })
  }

  const userPasswordChange = async (payload) => {
    const { new_password1, new_password2, old_password } = payload
    try {
      const res = await axios({
        method: 'post',
        url: `${BASE_URL}/password/change/`,
        data: {
          new_password1, new_password2, old_password
        },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      Swal.fire({
        text: '비밀번호가 변경되었습니다.',
        icon: 'success',
        confirmButtonText: '확인',
        confirmButtonColor: '#dce9be',
        timer: 2000,
      })
      return res
    } catch (err) {
      Swal.fire({
        text: '다시 시도해주세요',
        icon: 'error',
        showConfirmButton: false,
        timer: 1500
      }).then(() => {
        console.log(err)
      })
    }
  }

  const userDelete = async (payload) => {  // 회원 탈퇴
    const { password } = payload
    try {
      const res = await axios({
          method : 'post',
          url : `${BASE_URL}/custom/signout/`,
          headers: {
            Authorization: `Token ${token.value}`
          },
          data :{
            password : password
          }  
      }).then((res)=>{
        Swal.fire({
          text: `${res.data.detail}`,
          icon: 'success',
          confirmButtonText: '확인',
          confirmButtonColor: '#dce9be',
        })
        token.value = null
        router.push({ name: 'login' })
        return res
      })
      
    }
    catch (err) {
      Swal.fire({
        text: `${err.response.data.detail}`,
        icon: 'error',
        timer: 1500
      }).then(() => {
        console.log(err)
      })
    }
  }

  const getSuperUser = async function() {
    try {
      const res = await axios({
          method : 'get',
          url : `${BASE_URL}/custom/superuser/`,
          headers: {
            Authorization: `Token ${token.value}`
          }
      })
        // if (res.data.is_superuser){
        //   Swal.fire({
        //     text: '관리자 계정으로 로그인하셨습니다.',
        //     icon: 'success',
        //     confirmButtonText: '확인',
        //     confirmButtonColor: '#dce9be',
        //   })
        // }
        isSuperUser.value = res.data
        return res.data
      
      }
      catch (err) {
        console.log(err)
        Swal.fire({
          text: `${err.response.data.detail}`,
          icon: 'error',
          timer: 1500
        }).then(() => {
          console.log(err)
        })
      
    }
    
    }
  
  return { 
    user,
    token,
    isAuthenticated,
    isSuperUser,
    signUp,
    logIn, 
    logOut,
    getUserData,
    userUpdate,
    userPasswordChange,
    userDelete,
  }
}, { persist: {
    storage: sessionStorage,
    pick: ['token', 'isSuperUser']
} })
