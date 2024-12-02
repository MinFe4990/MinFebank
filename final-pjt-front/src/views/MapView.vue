<template>
    <div class="container">
    <!-- 버튼으로 위치 검색 -->
        <div class="my-3 row">
            <div class="col-12 mb-3">
                <div class="row">
                    <div class="col-6 col-md-8">
                        <form @submit.prevent="searchDir" class="input-group ">
                            <input type="text" id="keyword" class="form-control shadow-none" v-model="searchTarget" placeholder="검색을 원하는 지역이 어디인가요?"> 
                            <button type="submit" class="btn btn-outline-success" :class="{ 'btn-active': mapState === 'search' }"><i class="bi bi-search"></i></button> 
                        </form>
                    </div>
                    <div class="col-6 col-md-4 d-flex justify-content-end gap-3">
                        <button @click="searchCurrentLocation" class="btn btn-outline-secondary d-none  d-lg-block" :class="{ 'btn-active': mapState === 'current' }" >현재 위치로 검색</button>
                        <button @click="searchHomeLocation" class="btn btn-outline-secondary d-none d-lg-block" :class="{ 'btn-active': mapState === 'home' }">내 주소로 검색</button>
                        <button @click="searchCurrentLocation" class="btn btn-outline-secondary btn-sm d-lg-none" :class="{ 'btn-active': mapState === 'current' }">현재 위치</button>
                        <button @click="searchHomeLocation" class="btn btn-outline-secondary btn-sm d-lg-none" :class="{ 'btn-active': mapState === 'home' }" >내 주소</button>
                    </div>
                </div>
            </div>
            <div class="col-12">
                <select class="form-select shadow-none" v-model="selectbank">
                    <option value="은행">전체 은행</option>
                    <option v-for="bank in banklist" :value="bank.name" :key="bank.id">{{ bank.name }}</option>
                </select>
            </div>
        </div>
        <hr>
        <div class="map_wrap">
            <div id="map" style="width:100%;height:100%;position:relative;overflow:hidden;"></div>
            <div id="menu_wrap" class="bg_white">
                <ul id="placesList"></ul>
                <div id="pagination" class="d-flex justify-content-center gap-3"></div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted,watch } from "vue"
import { useLocStore } from '@/stores/location'
import { useProductStore } from "@/stores/product"
import { useUserStore } from "@/stores/user";
import Swal from 'sweetalert2'

const userStore = useUserStore()
const store = useLocStore()
const productStore = useProductStore()

const searchTarget = ref("")
const banklist = ref([])
const selectbank = ref("은행")
const mapState = ref('current')

const searchCurrentLocation = () => {
    store.searchCurrentLocation(selectbank.value)
    mapState.value = 'current'
}
const searchHomeLocation = () => {
    if (userStore.isAuthenticated === true) {
        store.searchHomeLocation(selectbank.value)
        mapState.value = 'home'
    } else {
        Swal.fire({
            text: '로그인이 필요합니다.',
            icon: 'warning',
            confirmButtonText : '확인',
            confirmButtonColor: '#dce9be',
        })
    }
}

const searchDir = function(){
    store.searchDir(searchTarget.value, selectbank.value)
    mapState.value = 'search'
} 

watch(selectbank, (newVal) => {
    if (newVal && userStore.isAuthenticated) {
        switch (mapState.value) {
            case 'current':
                store.searchCurrentLocation(newVal)
                break;
            case 'home':
                store.searchHomeLocation(newVal)
                break;
            case 'search':
                store.searchDir(searchTarget.value, newVal)
                break;
        }
        // store.searchDir(newVal); // 은행 검색 함수 호출
    }
    else if(newVal){
        switch (mapState.value) {
            case 'current':
                store.searchCurrentLocation(newVal);
                break;
            case 'home':
                store.searchCurrentLocation(newVal)
                break;
            case 'search':
                store.searchDir(searchTarget.value, newVal);
                break;
            }
        }
    
});


// 컴포넌트 마운트 시 Kakao Maps SDK 로드 및 지도 초기화
onMounted(async () => {
    try {
        // console.log("호출 시작")
        await productStore.getBankList();
        // console.log("호출 끝")
        const temp = productStore.bankList
        banklist.value = temp
        // console.log('업데이트 완료',banklist.value)
        await store.loadKakaoMaps();
        kakao.maps.load(() => {
            const defaultPosition = new kakao.maps.LatLng(37.5665, 126.9780);
            store.initMap(defaultPosition);
        });
    } catch (error) {
        console.error("Kakao Maps SDK 로드 실패:", error);
    }
});


</script>

<style scoped>
    .btn-active {
        background-color: #6c757d; /* 활성화된 버튼의 배경색 */
        color: #fff; /* 글자색 */
        border-color: #6c757d; /* 테두리색 */
    }
</style>

