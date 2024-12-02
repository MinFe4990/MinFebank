import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './user'
import Swal from 'sweetalert2'

export const useLocStore = defineStore('location', () => {
    const BASE_URL = "https://dapi.kakao.com/v2/local/"
    const BASE_URL2 = "http://localhost:8000/api/v1/products/"
    const userStore =useUserStore()

    // states
    const RSKEY= import.meta.env.VITE_KAKAORS_KEY 
    const JSKEY=import.meta.env.VITE_KAKAOJS_KEY
    const map = ref(null);
    const markers = ref([]);
    const itemEls =ref([]);
    const infowindow = ref(null);
    const banklist = ref(null);
    const userHome = ref(null);
    // 지도와 관련된 상태

    // getters


    // actions

    // Kakao Maps SDK 동적 로드 함수
    function loadKakaoMaps() {
        return new Promise((resolve, reject) => {
            const script = document.createElement("script");
            script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${JSKEY}&libraries=services,clusterer&autoload=false`;
            script.async = true;
            script.onload = () => resolve();
            script.onerror = (error) => reject(error);
            document.head.appendChild(script);
        });
    }

    // 지도 초기화 함수
    async function initMap(centerPosition) {
        const container = document.getElementById("map");
    
        // Geolocation 지원 여부 확인
        if (!navigator.geolocation) {
            Swal.fire({
                text: "Geolocation을 지원하지 않는 브라우저입니다.",
                icon: 'warning',
                confirmButtonText : '확인',
                confirmButtonColor: '#dce9be'
            })
            return;
        }
        try {
            // 현재 위치를 Promise로 처리
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(
                    (pos) => resolve(pos),
                    (err) => reject(err)
                );
            });
            const { latitude, longitude } = position.coords;
            centerPosition = new kakao.maps.LatLng(latitude, longitude);
        } catch (error) {
            console.error("현재 위치를 가져오는 데 실패했습니다:", error);
        }
        const options = {
            center: centerPosition, // 중심 좌표
            level: 3, // 확대 레벨
        };

        map.value = new kakao.maps.Map(container, options);
        infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 });
        clearMarkers();
        // 현재 위치를 기준으로 은행 검색
        searchBanks(centerPosition, '은행');
    }
    
    // 마커 추가 함수
    function addMarker(position, title) {
        let isClicked = false
        const marker = new kakao.maps.Marker({
            position,
            map: map.value,
        });
        kakao.maps.event.addListener(marker, "click", () => {
            if (isClicked){
                infowindow.value.close()  
                isClicked = false  
            }else{
                infowindow.value.setContent(`<div style="padding:5px;">${title}</div>`);
                infowindow.value.open(map.value, marker);
                isClicked = true
            }
        });
        markers.value.push(marker);
    }

    // 기존 마커 삭제
    function clearMarkers() {
        markers.value.forEach((marker) => marker.setMap(null));
        markers.value = [];
    }

    // 은행 검색 함수
    function searchBanks(location, bank) {
        const places = new kakao.maps.services.Places();
        // "은행" 키워드로 장소 검색
        places.keywordSearch(bank, (data, status, pagination) => {
            if (status === kakao.maps.services.Status.OK) {
                banklist.value=data //은행을 가져올 때마다 .banklist 초기화
                data.forEach((place) => {
                    const position = new kakao.maps.LatLng(place.y, place.x);
                    addMarker(position, place.place_name); // 마커 추가
                });

                // 지도 범위 확장
                const bounds = new kakao.maps.LatLngBounds();
                data.forEach((place) => {
                    bounds.extend(new kakao.maps.LatLng(place.y, place.x));
                });
                map.value.setBounds(bounds);
                displayPlaces(banklist.value);
                displayPagination(pagination);
            } else {
                Swal.fire({
                    text: '주변 은행 정보를 찾을 수 없습니다.',
                    icon: 'question',
                    confirmButtonText : '확인',
                    confirmButtonColor: '#dce9be',
                })
            }},
            {
            location,
            radius: 2000, 
            });
        }
    // 현재 위치 기반 검색 함수
    function searchCurrentLocation(bank) {
        if (!navigator.geolocation) {
            Swal.fire({
                text: "Geolocation을 지원하지 않는 브라우저입니다.",
                icon: 'warning',
                confirmButtonText : '확인',
                confirmButtonColor: '#dce9be',
            })
            return;
        }   
        navigator.geolocation.getCurrentPosition((position) => {
            const { latitude, longitude } = position.coords;
            const currentPosition = new kakao.maps.LatLng(latitude, longitude);
    
            // 지도 중심 이동
            map.value.setCenter(currentPosition);
            // 기존 마커 제거
            clearMarkers();
            // 현재 위치를 기준으로 은행 검색
            searchBanks(currentPosition, bank);
            },
            (error) => {
                console.error("현재 위치를 가져올 수 없습니다:", error);
                Swal.fire({
                    text: "현재 위치를 가져올수 없습니다.",
                    icon: 'error',
                    confirmButtonText : '확인',
                    confirmButtonColor: '#dce9be',
                })
            }
        );
    }
    
    const getLagLat = async (searchtarget) => {
        return axios({
            method: 'get',
            url: `${BASE_URL}/search/address.json`,
            params: {
                analyze_type: 'exact',
                page: 1,
                query: searchtarget
            },
            headers: {
                Authorization: `KakaoAK ${RSKEY}`
            }
        })
        .then((res) => {
            const document = res.data.documents[0];
            if (document) {
                return {
                    latitude: document.y, // 위도
                    longitude: document.x // 경도
                };
            } else {
                console.error('주소 검색 결과가 없습니다.');
                return null;
            }
        })
        .catch((err) => {
            console.error('위도 경도 가져오기 실패:', err);
            return null;
        });
    };
    
    const searchDir = async function(searchTarget, bank) {
        const ps = new kakao.maps.services.Places();  
        if (!searchTarget.replace(/^\s+|\s+$/g, '')) {
            Swal.fire({
                text: "키워드를 입력해주세요.",
                icon: 'warning',
                showConfirmButton: false,
                timer: 1500
            })
            return false;
        }
        ps.keywordSearch(`${searchTarget} ${bank}`, placesSearchCB); 
    }

    function placesSearchCB(data, status, pagination) {
        if (status === kakao.maps.services.Status.OK) {
            banklist.value = data
            // 정상적으로 검색이 완료됐으면
            // 검색 목록과 마커를 표출합니다
            displayPlaces(banklist.value);
    
            // 페이지 번호를 표출합니다
            displayPagination(pagination);
    
        } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
    
            Swal.fire({
                text: "검색 결과가 존재하지 않습니다..",
                icon: 'question',
                showConfirmButton: false,
                timer: 1500
            })
            return;
    
        } else if (status === kakao.maps.services.Status.ERROR) {
    
            Swal.fire({
                text: "검색 중 오류가 발생했습니다.",
                icon: 'error',
                showConfirmButton: false,
                timer: 1500
            })
            return;
    
        }
    }

    function displayPlaces(places) {
        const listEl = document.getElementById('placesList'),
            menuEl = document.getElementById('menu_wrap'),
            fragment = document.createDocumentFragment(),
            bounds = new kakao.maps.LatLngBounds();
    
        // 검색 결과 목록 초기화
        removeAllChildNods(listEl);
    
        // 기존 마커 제거
        clearMarkers();
    
        // 검색된 장소들을 순회
        for (let i = 0; i < places.length; i++) {
            const placePosition = new kakao.maps.LatLng(places[i].y, places[i].x);
    
            // 마커 추가
            addMarker(placePosition, places[i].place_name);
    
            // 검색 결과 항목 생성
            const itemEl = getListItem(i, places[i], markers.value[i]);
    
            // LatLngBounds에 좌표 추가
            bounds.extend(placePosition);
    
            // 검색 결과 항목을 fragment에 추가
            fragment.appendChild(itemEl);
        }
    
        // 검색 결과 항목 추가
        listEl.appendChild(fragment);
        menuEl.scrollTop = 0;
    
        // 지도 범위 재설정
        map.value.setBounds(bounds);
    }
    
    // 검색결과 항목을 Element로 반환하는 함수입니다
    function getListItem(index, places, marker) {
        const el = document.createElement('li')
        
        let itemStr = '<div class="map-info">' + '<h6>' + places.place_name + '</h6>';

        if (places.road_address_name) {
            itemStr += '<span>' + places.road_address_name + '</span>'
        } else {
            itemStr += '<span>' +  places.address_name  + '</span>'; 
        }
                    
        itemStr += '<span class="tel">' + places.phone  + '</span>' +
            '</div> <hr>';   

        el.innerHTML = itemStr;
        el.className = 'map-item';
        
        // 검색 결과 항목 클릭 이벤트 추가
        el.onclick = function () {
            // 지도 중심을 해당 위치로 이동
            map.value.setCenter(marker.getPosition());
    
            // 해당 마커의 인포윈도우를 표시
            infowindow.value.setContent(
                `<div style="padding:5px;">${places.place_name}</div>`
            );
            infowindow.value.open(map.value, marker);
            
            scrollToMap();
        };

    
        return el;
    }
    
    function scrollToMap() {
        const mapContainer = document.getElementById("map"); // map 컨테이너의 ID 사용
        if (mapContainer) {
            mapContainer.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }


    // 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
    function displayPagination(pagination) {
        const paginationEl = document.getElementById('pagination');
        const fragment = document.createDocumentFragment();
    
        // 기존에 추가된 페이지 번호를 삭제합니다.
        while (paginationEl.hasChildNodes()) {
            paginationEl.removeChild(paginationEl.lastChild);
        }
    
        for (let i = 1; i <= pagination.last; i++) {
            // 페이지 번호 링크 생성

            const el = document.createElement('span');

            el.innerHTML = i;
            el.classList.add('page-item')
            if (i === pagination.current) {
                el.classList.add('on'); // 현재 페이지 표시
            } else {
                el.onclick = (function (i) {
                    return function () {
                        pagination.gotoPage(i);
                    };
                })(i);
            }
            // 페이지 나누기
            fragment.appendChild(el);
        }

    
        paginationEl.appendChild(fragment);
    }
    

    // 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
    // 인포윈도우에 장소명을 표시합니다
    function displayInfowindow(marker, title) {
        var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';
        infowindow.value.setContent(content);
        infowindow.value.open(map.value, marker);
    }
    
     // 검색결과 목록의 자식 Element를 제거하는 함수입니다
    function removeAllChildNods(el) {   
        while (el.hasChildNodes()) {
            el.removeChild (el.lastChild);
        }
    }


    const  searchHomeLocation = async function(bank) {
        const userdata = await userStore.getUserData()
        if (userdata){
            userHome.value =userdata.address // 유저 정보에서 유제 데이터 가져오기
            const Position=await getLagLat(userHome.value) // 데이터를 이용해 
            if (Position){
                const HomePosition = new kakao.maps.LatLng(Position.latitude, Position.longitude);
                // 지도 중심 이동
                map.value.setCenter(HomePosition);
                // 기존 마커 제거
                clearMarkers();
                // 현재 위치를 기준으로 은행 검색
                searchBanks(HomePosition, bank);
            }else{
                console.log('집의 위도 경도를 가져오는데 실패했습니다.')
            }
        }else{
            console.log('유저 데이터를 가져오지 못했습니다.')
        }
    }

    
    return {
        map,
        userHome,
        banklist,
        loadKakaoMaps,
        initMap,
        searchBanks,
        searchCurrentLocation,
        searchHomeLocation,
        searchDir,
    }
} ,{ persist :{
storage: sessionStorage,
paths: ['map', ]
} })