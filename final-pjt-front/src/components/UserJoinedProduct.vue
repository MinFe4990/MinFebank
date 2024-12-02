<template>
  <div class="d-flex flex-column justify-content-between join-product">
    <table class="table">
      <thead>
        <tr>
          <th class="fs-head">상품 종류</th>
          <th class="fs-head">상품명</th>
          <th class="fs-head">저축 기간</th>
          <th class="fs-head">저축 금리</th>
          <th class="fs-head">최대 우대 금리</th>
        </tr>
      </thead>
      <tbody>
        <template v-if="list.length > 0">
        <tr v-for="product in list" :key="`${product.product.code}-${product.option.save_term}`">
          <td class="fs-content">{{ product.category === 'deposit' ? '정기 예금' : '정기 적금' }}</td>
          <td class="fs-content">
            <RouterLink
              :to="{ name: 'product-detail', params: { category: product.category, code: product.product.code}}"
              class="underline-none"
            >
              {{ product.product.name }}
            </RouterLink>
          </td>
          <td class="fs-content">{{ product.option.save_term }}</td>
          <td class="fs-content">{{ product.option.intr_rate }}</td>
          <td class="fs-content">{{ product.option.intr_rate2 }}</td>
        </tr>
        </template>
      </tbody>
    </table>
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
const props = defineProps({
  joinedProducts: Object
})

const list = ref([]) //보여지는 리스트

const listCunt = ref(5) // 한 페이지에 노출될 게시글 개수

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
  if(props.joinedProducts?.length % listCunt.value === 0 ){
    totalPage.value = (props.joinedProducts?.length / listCunt.value) -1
  } else{
    totalPage.value =  Math.ceil(props.joinedProducts?.length / listCunt.value) -1
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
      if(props.joinedProducts?.length > listIdx) { //
        list.value.push(props.joinedProducts[listIdx])
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


getList()
</script>

<style scoped>
.join-product{
  min-height: 300px;
}
.fs-head {
  font-size: 1rem;
}
.fs-content {
  font-size: 0.9rem;
}
.underline-none {
  text-decoration: none;
}
</style>