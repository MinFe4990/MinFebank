<template>
    <div >
        <div class="table-height">
            <table class="table">
                <thead>
                <tr >
                    <th class="fs-head col-2" scope="col">작성자</th>
                    <th class="fs-head col-6" scope="col">제목</th>
                    <th class="fs-head col-1" scope="col">추천</th>
                    <th class="fs-head col-1" scope="col">댓글</th>
                    <th class="fs-head col-2" scope="col">작성일</th>
                </tr>
                </thead>
                <tbody>
                <ArticleTableItem 
                    v-for="article in list"
                    :key="article.id"
                    :article="article"
                    :category="category"
                />
                </tbody>
            </table>
        </div>
        <ul class="pagination pagination-sm d-flex justify-content-center">
            <li class="page-item" :class="{'disabled' : isBtnPrev}">
                <a class="page-link shadow-none" href="#" @click.prevent="pageArrow('prev')">&laquo;</a>
            </li>
            <template v-for="item in pageList" :key="`list-${item+1}`">
                <li class="page-item" :class="{'active' : item == currentPage}">
                <a class="page-link shadow-none" href="#" @click.prevent="page(item)">{{item+1}}</a>
                </li>
            </template>
            <li class="page-item" :class="{'disabled' : isBtnNext}">
                <a class="page-link shadow-none" href="#" @click.prevent="pageArrow('next')">&raquo;</a>
            </li>
        </ul>
        <!-- {{ articleList[0] }} -->
    </div>
</template>

<script setup>
import { onBeforeRouteUpdate } from 'vue-router';
import ArticleTableItem from './ArticleTableItem.vue';

import { onMounted, ref, watch } from 'vue'

const props = defineProps({
    articleList: Array,
    category: String
})

// 페이지네이션 관련 기능
const list = ref([]) //보여지는 리스트

const listCunt = ref(15) // 한 페이지에 노출될 게시글 개수

let currentPage = ref(0) //현재 페이지
let pageNum = 10 //페이징 갯수
const pageList = ref([]) // 보여지는 페이지 리스트
let totalPage = ref(0); //페이지 숫자

let isBtnPrev = ref(true)
let isBtnNext = ref(true)

const currentPageListStart = () =>{
  return Math.floor(currentPage.value / pageNum) * pageNum
}
// 페이징 
const paging =() => {
  //보여지는 페이지 리셋
  pageList.value = [];

  //몇페이지 까지 있는지 확인
  if(props.articleList?.length % listCunt.value === 0 ){
    totalPage.value = (props.articleList?.length / listCunt.value) -1
  } else{
    totalPage.value =  Math.ceil(props.articleList?.length / listCunt.value) -1
  }

  //현재페이지 기준으로 페이징 숫자 넣기
  let pageListStart = currentPageListStart()
  for(let i= 0; i< pageNum; i++){   
    if(totalPage.value >= pageListStart){
      pageList.value.push(pageListStart)
      pageListStart++
    }
  }
}
const pageBtnCheck = () =>{
  isBtnPrev.value = currentPage.value == 0 ? true : false
  isBtnNext.value = currentPage.value == totalPage.value ? true : false
}

const getList = () =>{
    list.value = [] //보여지는 게시물 리셋
    
    let listIdx = (listCunt.value * (currentPage.value )); // 보여질 게시물 index
    for(let i= 0; i < listCunt.value; i++ ){       //게시글 수 만큼 루프
      if(props.articleList?.length > listIdx) { //
        list.value.push(props.articleList[listIdx])
        listIdx++
      }
    }
    paging()
    pageBtnCheck()
}
//페이지 번호 클릭시
const page = (e) =>{
  currentPage.value = e  
  getList()
}
//페이지 처음/끝/이전/다음 버튼 클릭시
const pageArrow = (e) => {
  let movePage = parseInt(currentPage.value)
 if(e == 'prev'){    //이전  
    movePage = currentPageListStart() - 1    
    movePage < 0 ? movePage = 0 : ''
  } else{//다음
    movePage = currentPageListStart() + 10
    movePage >= totalPage.value ? movePage = totalPage.value : ''
  }
  page(movePage)
}

// 라우트 변경 시 데이터 갱신
onBeforeRouteUpdate((to, from, next) => {
  if (to.params.category !== props.category) {
    currentPage.value = 0;
    getList();
  }
  next();
});

// Props 감지하여 리스트 갱신
watch(
  () => props.articleList,
  () => {
    currentPage.value = 0;
    getList();
  },
  { deep: true }
);


onMounted(() => {
  getList()
})
</script>

<style scoped>
.table-height {
    min-height: 70vh;
}
.fs-head {
    font-size: 1rem;
    text-align: center;
}
</style>