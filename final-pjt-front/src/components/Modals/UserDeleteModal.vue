<template>
<!-- Modal -->
<div class="modal fade" id="user-delete-modal" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="staticBackdropLabel">회원 탈퇴</h1>
        <button type="button" class="btn-close" ref="closeButtonRef" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p>회원 탈퇴를 원하시면 비밀번호를 입력하세요.</p>
        <input class="form-control mb-3" type="password" v-model="password" placeholder="회원 탈퇴를 원하시면 비밀번호를 입력하세요.">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
        <button type="button" class="btn btn-danger" @click="userDelete">회원 탈퇴</button>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const password = ref('')

const closeButtonRef = ref('')

const userDelete = async () => {
  const payload = {
    password: password.value,
  }
  try {
    await userStore.userDelete(payload) 
    if (closeButtonRef.value) {
      password.value = ''
      closeButtonRef.value.click()
    }
  } catch (err) {
    console.error( err)
  }
  }
</script>

<style scoped>

</style>