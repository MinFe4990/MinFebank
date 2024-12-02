<template>
  <div class="d-flex justify-content-center align-items-center mb-5">
    <form class="card p-3 mt-5 signup-form" @submit.prevent="userUpdate">
      <div class="form-list mb-3">
        <h5>기본 정보</h5>
        <div class="input-group">
          <span class="input-group-text"><i class="bi bi-person-add"></i></span>
          <input class="form-control shadow-none" disabled type="text" placeholder="아이디" v-model="username">
        </div>
        <div class="input-group">
          <span class="input-group-text"><i class="bi bi-key"></i></span>
          <input class="form-control shadow-none" disabled type="password" placeholder="비밀번호">
        </div>
        <div class="input-group">
          <span class="input-group-text"><i class="bi bi-key"></i></span>
          <input class="form-control shadow-none" disabled type="password" placeholder="비밀번호 확인">
        </div>
      </div>
      <button class="btn btn-secondary mb-3" type="button" data-bs-toggle="modal" data-bs-target="#user-password-change-modal">
        비밀번호 변경
      </button>
      <div class="form-list mb-3">
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
      <input type="submit" value="회원 정보 수정" class="btn btn-primary mb-2">
      <button class="btn btn-danger" type="button" data-bs-toggle="modal" data-bs-target="#user-delete-modal">
        회원 탈퇴
      </button>
    </form>
    <UserPasswordChangeModal />
    <UserDeleteModal />
  </div>
</template>

<script setup>
import { onMounted, ref, useTemplateRef } from 'vue'
import { useUserStore } from '@/stores/user'
import UserDeleteModal from '@/components/Modals/UserDeleteModal.vue'
import UserPasswordChangeModal from '@/components/Modals/UserPasswordChangeModal.vue'

const store = useUserStore()

const username = ref('')
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

const userUpdate = () => {
  const payload = {
    username: username.value,
    last_name: lastName.value,
    first_name: firstName.value,
    email: `${emailId.value}@${emailAddress.value}`,
    postcode: postcode.value,
    address: address.value,
    address_detail: addressDetail.value
  }
  store.userUpdate(payload)
}

onMounted(async () => {
  const userData = await store.getUserData()
    if (userData) {
      username.value = userData.username
      lastName.value = userData.last_name
      firstName.value = userData.first_name
      emailId.value = userData.email.split('@')[0]
      emailAddress.value = userData.email.split('@')[1]
      address.value = userData.address
      addressDetail.value = userData.address_detail
      postcode.value = userData.postcode
      
    } else {
      console.log('유저 데이터를 가져오지 못했습니다.')
    }
})
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