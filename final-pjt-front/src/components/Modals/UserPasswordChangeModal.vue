<template>
  <!-- Modal -->
  <div class="modal fade" id="user-password-change-modal" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="staticBackdropLabel">비밀번호 변경</h1>
          <button type="button" class="btn-close" ref="closeButtonRef" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="old-password" class="form-label">현재 비밀번호</label>
            <input class="form-control" type="password" id="old-password" v-model="oldPassword">
          </div>
          <div class="mb-3">
            <label for="password1" class="form-label">새 비밀번호</label>
            <input class="form-control" type="password" id="password1" v-model="password1">
          </div>
          <div class="mb-3">
            <label for="password2" class="form-label">새 비밀번호 확인</label>
            <input class="form-control" type="password" id="password2" v-model="password2">
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
          <button type="button" class="btn btn-primary" @click="passwordChange">비밀번호 변경</button>
        </div>
      </div>
    </div>
  </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useUserStore } from '@/stores/user'

  const userStore = useUserStore()

  const password1 = ref('')
  const password2 = ref('')
  const oldPassword = ref('')

  const closeButtonRef = ref('')

  const passwordChange = async () => {
    const payload = {
      new_password1: password1.value,
      new_password2: password2.value,
      old_password: oldPassword.value
    }
    try {
    await userStore.userPasswordChange(payload) 
    if (closeButtonRef.value) {
      password1.value = ''
      password2.value = ''
      oldPassword.value = ''
      closeButtonRef.value.click()
    }
  } catch (err) {
    console.error('비밀번호 변경 실패:', err)
  }
  }
  
  </script>
  
  <style scoped>
  
  </style>