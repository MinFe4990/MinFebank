<template>
  <div class="container d-flex justify-content-center align-items-center">
    <form class="card p-3 mt-5 signup-form" @submit.prevent="signUp">
      <div class="form-list mb-5">
        <h5>기본 정보</h5>
        <div class="input-group">
          <span class="input-group-text"><i class="bi bi-person-add"></i></span>
          <input class="form-control shadow-none" type="text" placeholder="아이디" v-model="username">
        </div>
        <div class="input-group">
          <span class="input-group-text"><i class="bi bi-key"></i></span>
          <input class="form-control shadow-none" type="password" placeholder="비밀번호" v-model="password1">
        </div>
        <div class="input-group">
          <span class="input-group-text"><i class="bi bi-key"></i></span>
          <input class="form-control shadow-none" type="password" placeholder="비밀번호 확인" v-model="password2">
        </div>
      </div>
      <div class="form-list mb-5">
        <h5>상세 정보</h5>
        <div class="row">
          <span class="form-label">이름</span>
          <div class="col">
            <input class="form-control shadow-none" type="text" placeholder="성" v-model="lastName">
          </div>
          <div class="col">
            <input class="form-control shadow-none" type="text" placeholder="이름" v-model="firstName">
          </div>
        </div>
        <div class="row">
          <span class="form-label">이메일</span>
          <div class="input-group">
            <input class="form-control shadow-none" type="text" placeholder="이메일 아이디" v-model="emailId">
            <span class="input-group-text">@</span>
            <input class="form-control shadow-none" type="text" placeholder="이메일 주소" v-model="emailAddress">
          </div>
        </div>
        <div class="row mb-3">
          <span class="form-label">주소</span>
          <div class="col-4">
            <input 
              class="form-control shadow-none" type="text" placeholder="우편번호" 
              @focusin="findAddress" v-model="postcode"
            >
          </div>
          <div class="col-8">
            <input 
              class="form-control shadow-none" type="text" placeholder="주소"
              @focusin="findAddress" v-model="address"
            >
          </div>
          <div class="col-12 mt-2">
            <input 
              class="form-control shadow-none" type="text" placeholder="상세주소" 
              v-model="addressDetail" ref="addressDetailRef"
            >
          </div>
        </div>
      </div>
      <input type="submit" value="회원 가입" class="btn btn-primary">
    </form>
  </div>
</template>

<script setup>
import { ref, useTemplateRef } from 'vue'
import { useUserStore } from '@/stores/user'

const store = useUserStore()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const lastName = ref('')
const firstName = ref('')
const emailId = ref('')
const emailAddress = ref('')
const postcode = ref('')
const address = ref('')
const addressDetail = ref('')
const addressDetailRef = useTemplateRef('addressDetailRef')

const findAddress = () => {  // 다음 우편번호 찾기 API 활용
  new daum.Postcode({
    oncomplete: function(data) {
      postcode.value = data.zonecode
      address.value = data.address
      address.value += data.buildingName === '' ? '' : `(${data.buildingName})`
    }
  }).open()
  addressDetailRef.value.focus()
}

const signUp = () => {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    last_name: lastName.value,
    first_name: firstName.value,
    email: `${emailId.value}@${emailAddress.value}`,
    postcode: postcode.value,
    address: address.value,
    address_detail: addressDetail.value
  }
  store.signUp(payload)
}
</script>

<style scoped>
.form-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.signup-form {
  max-width: 800px;
  width: 80%;
}
</style>