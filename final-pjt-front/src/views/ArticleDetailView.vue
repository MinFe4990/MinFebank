<template>
    <div class="container p-3">
        <div class="d-flex justify-content-between">
            <div>
                <h4>{{ article.title }}</h4>
            </div>
            <div class="d-flex gap-4"  v-if="userStore.user === article.user">
                
                <RouterLink
                class="nav-link"
                :to="{ name: 'update-article', params: route.params, query: { ...article } }"
                >
                수정
            </RouterLink>
            <span class="cursor" @click="deleteArticleDetail">삭제</span>
        </div>
        
    </div>
    <div class="d-flex justify-content-between">
        <span>{{ article.user }}</span>
        <span>{{ formatDate(article.create_at) }}</span>
    </div>
    <hr>
    <div class="content">
        <p>{{ article.content }}</p>
    </div>
    <div class="text-center">
        <div class="heart btn btn-outline-thema" @click="likes" v-if="userStore.isAuthenticated">
            <img class="like" v-if="likeArticle" src="@/assets/icons8/icons8-처럼-96.png" alt="">
            <img class="like" v-else src="@/assets/icons8/icons8-heart-96.png" alt="">
            <span class="mx-1">{{ article.articlelike }}</span>
        </div>
    </div>
    <hr>
    <form class="input-group mb-3" @submit.prevent="createCommit">
        <input class="form-control shadow-none" type="text" name="commit" id="commit" v-model="newCommit">
        <button class="btn btn-sm btn-thema">댓글 작성</button>
    </form>
    <div v-if="list.length">
        <ArticleCommit
        v-for="commit in list || []"
        :key="commit.id"
        :commit="commit"
        @commit-update="commitUpdate"
        />
        <hr>
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
        <p v-else>댓글이 없습니다.</p>
    </div>
</template>

<script setup>

import { useRoute } from 'vue-router';
import { computed, onMounted, ref, watch } from 'vue';
import { useArticleStore } from '@/stores/articles';
import { useUserStore } from '@/stores/user';
import ArticleCommit from '@/components/ArticleCommit.vue';
import Swal from 'sweetalert2'


const route = useRoute();
const articleStore = useArticleStore();
const userStore = useUserStore();
// const likeArticle = ref(false)

const commitUpdate= async()=>{
    try {
        // 서버에서 최신 댓글 데이터 가져오기
        await articleStore.getCommit(route.params.id);
        // 최신 데이터로 리스트 갱신
        getList();
    } catch (error) {
        console.error('Error updating commit list:', error);
    }
}

const likes = async () => {
    try {
        // 서버 요청
        await articleStore.likeArticle(article.value.id,route.params.category);
        await fetchArticleData(route.params.id)
    } catch (error) {
        console.error("Error updating likes:", error);
    }
};

const likeArticle = computed (()=>{
    return articleStore.likeArticleUser?.likeuser.includes(userStore.user)? true :false
} )


const article = ref({});
const title = ref('');
const newCommit = ref('');

const createCommit = async () => {
    try {
        if(userStore.isAuthenticated){
            await articleStore.createCommit(route.params.id, newCommit.value); // 댓글 작성
            newCommit.value = ''; // 입력 필드 초기화
            await articleStore.getCommit(route.params.id).then(() => {
                getList()
            })
        }else{
            Swal.fire({
                text: '로그인이 필요합니다.',
                icon: 'warning',
                confirmButtonText: '확인',
                confirmButtonColor: '#dce9be',
            })
            newCommit.value=""
        }
        
    } catch (error) {
        console.error('Error creating commit:', error);
    }
};


const fetchArticleData = async (id) => {
    try {
        await articleStore.getArticleDetail(id);
        article.value = articleStore.detailArticle;
        title.value = article.value.title;
        await articleStore.getCommit(id).then(( ) =>{
            getList()
        })
    } catch (error) {
        console.error('Error fetching article data:', error);
    }
};

const deleteArticleDetail = function(){
    Swal.fire({
        text: '게시글을 삭제하시겠습니까?',
        icon: 'question',
        confirmButtonText: '확인',
        confirmButtonColor: '#dce9be',
        showCancelButton: true,
        cancelButtonText: '취소'
    }).then((res) => {
        if (res.isConfirmed) {
            articleStore.deleteArticleDetail(route.params.id, route.params.category)
        }
    })
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

// 라우트 변경 시 데이터 로드
watch(
    () => route.params.id,
    (newId) => {
        if (newId) {
            fetchArticleData(newId);
        }
    },
    { immediate: true } // 즉시 실행
);


// 초기 데이터 로드
onMounted(async () => {
    try {
        if (userStore.isAuthenticated && !userStore.user) {
            await userStore.getUserData(); // 유저 데이터 로드
        }

        await fetchArticleData(route.params.id); // 게시글 데이터 로드
        await articleStore.getLikeArticle(article.value.id); // 좋아요 정보 로드

    } catch (error) {
        console.error("Error during onMounted:", error);
    } 
});




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
    if(articleStore.commits?.length % listCunt.value === 0 ){
        totalPage.value = (articleStore.commits?.length / listCunt.value) -1
    } else{
        totalPage.value =  Math.ceil(articleStore.commits?.length / listCunt.value) -1
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
      if(articleStore.commits?.length > listIdx) { //
        list.value.push(articleStore.commits[listIdx])
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
    .heart {
        display: inline-block;
    }
    .cursor {
        cursor: pointer;
    }
    .content {
        min-height: 50vh;
    }
    .like {
        height: 25px;
    }
</style>