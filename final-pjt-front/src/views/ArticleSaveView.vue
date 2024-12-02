<template>
    <div class="mb-5">
        <form class="p-3" @submit.prevent="createArticleList">
            <input type="text" class="form-control mb-3" placeholder="제목" v-model="title">
            <!-- <input type="file" accept="image/*" multiple class="form-control mb-3" disabled> -->
            <textarea class="form-control mb-3 content" placeholder="원하는 내용을 마음껏 작성하세요" v-model="content"></textarea>
            <div class="d-grid">
                <button  class="btn btn-thema mb-3" type="submit" >
                    게시글 작성
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
    import { useRoute } from 'vue-router'
    import { computed, onMounted, ref } from 'vue'
    import { useArticleStore } from '@/stores/articles'
    import { useUserStore } from '@/stores/user'
    const content = ref("")
    const title = ref("")

    const route = useRoute()

    const articleStore = useArticleStore()
    const userStore = useUserStore()
    const createArticleList = function(){
        articleStore.createArticleList(route.params.category,title.value,content.value)
    }
</script>

<style scoped>
.content {
    min-height: 65vh;
}
</style>