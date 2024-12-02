<template>
    <tr>
        <td class = "text-truncate title-cell text-center">
            {{ article.user }}
        </td>
        <td class="text-truncate title-cell fw-bold px-3">
            <RouterLink
                :to="{ name: 'article-detail', params: { category: category, id: article.id}}"
                class="underline-none a-black"
                :key = "article.id"
                @click.native="handleRouteChange"
            >
                {{ article.title }}
            </RouterLink>
        </td>
        <td class = "text-truncate title-cell text-center">{{ article.articlelike }}</td>
        <td class = "text-truncate title-cell text-center">{{ article.commitcount }}</td>
        <td class = "text-truncate title-cell text-center">{{ formatDate(article.create_at) }}</td>
    </tr>
</template>

<script setup>
    import { ref } from 'vue'
    import { RouterLink, useRouter } from 'vue-router'

    const router = useRouter()

    const props = defineProps({
        article: Object,
        category: String
    })
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        const year = date.getFullYear().toString().slice(-2); // yy 형식
        const month = String(date.getMonth() + 1).padStart(2, '0'); // mm 형식
        const day = String(date.getDate()).padStart(2, '0'); // dd 형식
        const hours = String(date.getHours()).padStart(2, '0'); // hh 형식
        const minutes = String(date.getMinutes()).padStart(2, '0'); // mm 형식
        return `${year}.${month}.${day} ${hours}:${minutes}`;
    };
    const handleRouteChange = () => {
        router.push({
            name: 'article-detail',
            params: { category: props.category, id: props.article.id },
        }).catch((err) => {
            if (err.name !== 'NavigationDuplicated') {
            console.error(err);
        }
    });}
</script>

<style scoped>
    .title-cell, .content-cell {
        max-width: 150px; /* 원하는 최대 너비를 지정 */
        white-space: nowrap; /* 텍스트를 한 줄로 유지 */
        overflow: hidden; /* 넘치는 내용을 숨김 */
        text-overflow: ellipsis; /* 넘친 내용 대신 ... 표시 */
    }
    .underline-none {
        text-decoration: none;
        color: black;
    }
    td {
        vertical-align: middle; /* 내용 가운데 정렬 */
    }
</style>