<template>
  <div class="container d-flex justify-content-center align-items-center">
    <form class="card mt-5 login-form" @submit.prevent="logIn">
      <div class="card-header p-3">
        <h4 class="card-title text-center m-0">서비스명</h4>
      </div>
      <div class="px-4 py-5">
        <div class="input-group mb-3">
          <span class="input-group-text"><i class="bi bi-person-add"></i></span>
          <input class="form-control shadow-none" type="text" placeholder="아이디" v-model="username">
        </div>
        <div class="input-group mb-3">
          <span class="input-group-text"><i class="bi bi-key"></i></span>
          <input class="form-control shadow-none" type="password" placeholder="비밀번호" v-model="password">
        </div>
        <div class="row mb-3 text-secondary login-addtional">
          
          <div class="col text-center">
            <span class='cursor' @click="signUp">회원 가입</span>
          </div>
        </div>
        <div class="d-grid">
          <input type="submit" value="로그인" class="btn btn-primary">
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
const router = useRouter()
const store = useUserStore()

const username = ref('')
const password = ref('')

const signUp = ()=>{
  router.push({name:'signup'})
}

const logIn  = () => {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style scoped>
.form-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.login-form {
  max-width: 500px;
  width: 70%;
}
.cursor {
  cursor: pointer;
}
.login-addtional {
  font-size: 13px;
}
</style>