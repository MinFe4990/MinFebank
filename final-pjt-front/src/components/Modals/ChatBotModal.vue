<template>
    <div class="chatbot">
        <!-- 모달 -->
        <div v-if="isModalVisible" class="modal-overlay shadow d-flex flex-column justify-content-between" @click.self="closeModal">
            <div class="modal-header">
                <p>상품 추천 받기</p>
                <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-content flex-fill">
                <div class="chat-messages ">
                    <div
                    v-for="(message, index) in chatMessages"
                    :key="index"
                    class="chat-message"
                    :class="{ user: message.type === 'user', gpt: message.type === 'gpt' }"
                    >
                        <div class="d-flex align-items-end">
                            <img v-if="message.type === 'gpt'" src="@/assets/gpt-icon.png" alt="gpt-logo">
                        </div>
                        <div :class="{ 'user-message': message.type === 'user', 'gpt-message': message.type === 'gpt' }">
                            <p>{{ message.content }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-input d-flex">
                <input type="text" class="flex-fill" placeholder="요청사항을 적어주세요." v-model="userMessage">
                <button @click="chatSubmit" class="btn btn-sm btn-success fw-bold"><i class="bi bi-send"></i></button>
            </div>
        </div>
        <!-- GPT 버튼 -->
        <div v-if="userStore.isAuthenticated" class="bottom-area">
            <button
                class="gpt-button"
                @mouseover="showTooltip = true"
                @mouseleave="showTooltip = false"
                @click="toggleModal"
            >
                <img src="@/assets/gpt-icon.png" alt="GPT" />
                <div v-if="showTooltip" class="tooltip">상품을 추천해드릴까요?</div>
            </button>
        </div>
    </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { useProductStore } from '@/stores/product';
import { onMounted, ref } from 'vue';
import axios from 'axios';

const userStore = useUserStore();
const productStore = useProductStore();
const showTooltip = ref(false); // 툴팁 상태

const home = ref(null);
const deposits = ref(null);
const savings = ref(null);
const alreadyjoinedproduct = ref(null);
const chatMessages = ref([]); // 메시지 목록
const userMessage = ref('상품을 추천해줘')
const buttonShow = ref(true);
const isModalVisible = ref(false); // 모달 가시성 상태

// 모달 열기/닫기 함수
const toggleModal = () => {
    isModalVisible.value = !isModalVisible.value;
    // console.log("Modal Visibility:", isModalVisible.value); // 디버그용 로그 추가
};

const closeModal = () => {
    isModalVisible.value = false;
};

onMounted(async () => {
    try {
        const userdata = await userStore.getUserData();
        home.value = userdata.address;
        deposits.value = await productStore.getDepositList();
        savings.value = await productStore.getSavingList();
        alreadyjoinedproduct.value = await productStore.getJoinedProduct();
    }catch (error) {
        console.error('Error loading data:', error);
    }
});

const API_KEY = import.meta.env.VITE_GPT_KEY;

const chatSubmit = () => {
    buttonShow.value = false;
    addChatMessage(userMessage.value, "user"); // 유저 메시지 추가
    chatReceive();
    userMessage.value = ''
};

const chatReceive = async () => {
    const formattedDeposits = deposits.value
        ? deposits.value.map((item) =>
            `${item.bank?.name}에서 ${item.code}의 코드로 \n ${item.options?.map((option) =>
                `${option.save_term}개월  ${option.intr_rate}% 이자`
            ).join(',\n')}`).join(',\n')
        : '없음';

    const formattedSavings = savings.value
        ? savings.value.map((item) =>
            `${item.bank?.name}에서 ${item.code}의 코드로 \n ${item.options?.map((option) =>
                `${option.save_term}개월 ${option.intr_rate}% 이자`
            ).join(',\n')}`).join(',\n')
        : '없음';

    const formattedJoinedProducts = alreadyjoinedproduct.value
        ? alreadyjoinedproduct.value.map((item) =>
            `${item.product?.name} (${item.category}, 옵션: ${item.option?.save_term})기간 ${item.option?.intr_rate} 이자율)`).join(',\n')
        : '없음';

    const messages = [
        {
            role: "system",
            content: `너는 유능한 투자관리자야. 나는 현재 ${home.value}에 살고 있고, 
            내 주변에서 가입할 수 있는 적금상품과 예금상품은 아래와 같아
            예금 상품은 다음과 같아: ${formattedDeposits}.
            적금 상품은 다음과 같아: ${formattedSavings}.
            내가 이미 가입한 상품은 ${formattedJoinedProducts}란 것을 알고 있어.
            추천을 부탁해.
            답변으로는 
            
            제가 추천드릴 상품은 아래와 같습니다.

            1. WR0001F(우리은행) : 
              기한 3개월 3.%이자
            2. WR0001L(우리은행) : 
              기한 36개월 3.5%이자
            3. 01020400490002(카카오뱅크) : 
              기한 12개월 3.5%이자
            4. 01020400530001(BNK은행) : 
              기한 12개월 3.5%이자
            5. 01211210113(INK기업은행) : 
              기한 12개월 3.5%이자

            와 같은 5개의 상품을 추천드립니다.
            
            와 같이 5개의 상품, 1개의 개월, 그에 맞는 이자 로 2줄로구성해서 최대 13줄로 답변해줘
            `
        },
        { role: 'user', content: '상품 추천을 해줘.' },
    ];

    try {
        const response = await axios({
            method: 'post',
            url: 'https://api.openai.com/v1/chat/completions',
            headers: {
                Authorization: `Bearer ${API_KEY}`,
                'Content-Type': 'application/json',
            },
            data: {
                model: 'gpt-4o-mini',
                messages,
            },
        });
        const gptResponse = response.data.choices[0].message.content;
        addChatMessage(gptResponse, "gpt");
        buttonShow.value = true; // 버튼 다시 활성화
    } catch (error) {
        console.error("Error fetching GPT response:", error);
        addChatMessage("추천을 가져오는 데 실패했습니다.", "gpt");
        buttonShow.value = true; // 버튼 다시 활성화
    }
};

// 메시지 추가 함수
const addChatMessage = (content, type) => {
    chatMessages.value.push({ content, type });
};
</script>
<style scoped>
.chatbot {
    position: fixed;
    right: 30px; /* 화면 오른쪽에서 여유 공간 확보 */
    bottom: 30px; /* 화면 하단에서 여유 공간 확보 */
    z-index: 1000;;
}
/* 툴팁 스타일 */
.tooltip {
    position: absolute; /* 버튼 기준으로 위치 설정 */
    bottom: 110%; /* 버튼 위로 적절히 띄움 */
    left: 85%; /* 버튼 기준으로 7대 3 비율로 오른쪽으로 치우침 */
    transform: translateX(-85%); /* 왼쪽으로 살짝 당김 */
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 6px 12px; /* 텍스트 주변 여백 추가 */
    border-radius: 5px;
    font-size: 14px;
    white-space: nowrap;
    z-index: 2000;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    opacity: 1; /* 항상 보이도록 설정 */
    visibility: visible; /* 항상 보이도록 설정 */
}

/* 모달 스타일 */
.modal-overlay {
    box-sizing: border-box;
    margin: 20px 0;
    width: 350px;
    height: 500px;
    border: 1px solid lightgray;
    border-radius: 15px;
    background-color: white;
    animation: fadeIn 400ms;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.5);
  } to {
    opacity: 1;
    transform: scale(1);
  }
}
.chat-message p {
    white-space: pre-wrap; /* 줄바꿈과 공백을 유지 */
}
.modal-header {
    display: flex;
    justify-content: space-between;
    box-sizing: border-box;
    padding: 10px;
    align-items: center;
    border-radius: 15px 15px 0 0 ;
    border-bottom: 1px solid lightgray;
}
.modal-header > p {
    margin: 0;
    font-size: 20px;
    font-weight: bold;
}
.modal-content {
    box-sizing: border-box;
    overflow-y: scroll;
    padding: 10px;
    background-color: var(--maincolor);
}
.chat-message.user {
    display: flex;
    justify-content: end;
}
.chat-message.user > .user-message {
    border: 1px solid lightgrey;
    border-radius: 20px 20px 0 20px;
    padding: 10px;
    margin-bottom: 15px;
    background-color: white;
}
.chat-message.gpt {
    display: flex;
}
.chat-message.gpt img {
    width: 30px;
    height: 30px;
    margin-right: 5px;
    background-color: white;
    border-radius: 50%;
    border: 1px solid lightgrey;
}
.chat-message.gpt > .gpt-message {
    border: 1px solid lightgrey;
    border-radius: 20px 20px 20px 0;
    padding: 10px;
    margin-bottom: 15px;
    background-color: white;
}
    
.modal-input {
    width: 100%;
}
.modal-input > input {
    border: none;
    border-radius: 0 0 15px 15px;
    outline: none;
    padding: 10px;
}
.modal-input > button {
    width: 45px;
    height: 100%;
    border-radius: 0 0 15px 0;
    font-size: 25px;
}
/* 버튼 스타일 */
.bottom-area {
    display: flex;
    justify-content: end;

}

.gpt-button {
    position: relative; /* 툴팁 위치 조정을 위해 relative 사용 */
    border: none;
    background: white;
    cursor: pointer;
    width: 60px;
    height: 60px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    border-radius: 50%;
}

.gpt-button img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
}
</style>
