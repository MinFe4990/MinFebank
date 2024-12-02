<template>
  <div class="mb-3">
      <hr>
      <div class="d-flex justify-content-between px-2">
          <p class="fw-bold">{{ commit.user }}</p>
          <div class="d-flex gap-4" v-if="commit.user===userStore.user">
              <span class="cursor" @click = "UserUpdate" >수정</span>
              <span class="cursor" @click = "UserDelete">삭제</span>
          </div>
      </div>
      <div class="px-2">
          <input v-if="clicked" class="form-control form-control-sm shadow-none" type="text" v-model="content">
          <p v-else>{{ commit.content }}</p>
      </div>
      <div class="px-2 fs-sm">
          <p>{{ formatDate(commit.create_at) }}</p>
      </div>
  </div>   
</template>

<script setup>
import { ref,computed, onMounted, defineEmits  } from 'vue';
import { useUserStore } from '@/stores/user';
import { useArticleStore } from '@/stores/articles';
const userStore = useUserStore()
const articleStore = useArticleStore()

const props = defineProps({
  commit : Object,
})
const emit = defineEmits([
  'commit-update'
])

const content = ref("")
content.value = props.commit.content
const clicked = ref(false)

const UserUpdate = async () => {
  if (clicked.value){
      clicked.value = !clicked.value
      await articleStore.updateCommit(props.commit.id, content.value)
      emit('commit-update');
  }else{
      clicked.value = !clicked.value
  }
}

const UserDelete= async ()=>{
  
  await articleStore.deleteCommit(props.commit.id)
  emit('commit-update');
  
  
}

const formatDate = (dateString) => {
      const date = new Date(dateString);
      const year = date.getFullYear().toString().slice(-2); // yy 형식
      const month = String(date.getMonth() + 1).padStart(2, '0'); // mm 형식
      const day = String(date.getDate()).padStart(2, '0'); // dd 형식
      const hours = String(date.getHours()).padStart(2, '0'); // hh 형식
      const minutes = String(date.getMinutes()).padStart(2, '0'); // mm 형식
      return `${year}.${month}.${day} ${hours}:${minutes}`;
  };
</script>

<style scoped>
  .fs-sm {
    font-size: 0.8rem;
  }
  .like {
    height: 25px;
  }
  .heart {
    display: inline-block;
  }
  .cursor {
    cursor: pointer;
  }
</style>