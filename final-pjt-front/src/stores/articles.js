import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from './user'
import Swal from 'sweetalert2'


export const useArticleStore = defineStore('article', () => {
    const BASE_URL = 'http://127.0.0.1:8000/api/v1/articles'
    const router = useRouter()
    const userStore = useUserStore()
    // state
    const articleList = ref(null) // 게시글 전체 조회용
    const detailArticle = ref({}) // 게시글 상세 조회용
    const commits = ref([])
    const likeArticleUser = ref(null)
    const likeCommitUser = ref(null)
    // getters
    

    // actions

    const getArticleList = async function(articleType) {
        try {
          const response = await axios({
            method: 'get',
            url: `${BASE_URL}/`,
            params : {
                type: articleType,
            }
        });
          return response.data.article.sort((a, b) => b.id - a.id); // 최신 순으로 정렬 후 반환
        } catch (err) {
          console.error("Error fetching articles: ", err);
          throw err; // 오류가 발생하면 호출한 쪽에서 처리할 수 있도록 throw
        }
    }

    const createArticleList = (articleType,articleTitle,articleContent) => {  // 게시글 작성
        axios({
            method: 'post',
            url: `${BASE_URL}/`,
            data: {
                type : articleType, // 게시글 종류가 2개 이상일 경우 해당 명을 넣어준다. ex) 자유 게시판, 적금자랑 게시판
                title : articleTitle, // article 제목
                content : articleContent, // article 내용
            },
            headers: {
                Authorization: `Token ${userStore.token}`
            }
            }).then((res) => {
                router.push({name:`${articleType}-article`,params:{category : articleType}})
            }).catch((err) => {
                console.log(err)
        })
    }
    const getArticleDetail = async (article_pk) => {
        try {
            const response = await axios({
                method: 'get',
                url: `${BASE_URL}/detail/`,
                params: {
                    article_pk: article_pk, // article_pk를 쿼리 파라미터로 전달
                },
                // headers: {
                //     Authorization: `Token ${userStore.token}`, // 인증 토큰
                // },
            });
            detailArticle.value = response.data; // 성공 시 데이터 저장
            return response.data; // 데이터 반환 (필요 시 호출자에서 사용 가능)
        } catch (err) {
            console.error('Error fetching article details:', err);
            throw err; // 오류 발생 시 호출자에게 오류 전달
        }
    };
    

    const updateArticleDetail = (article_pk,title,content)=>{
        axios({
            method: 'put',
            url: `${BASE_URL}/detail/`,
            data:{
                article_pk : article_pk, // article id 도 같이 받아와서 이를 사보내주면된다.
                title : title,
                content : content
            },
            headers: {
                Authorization: `Token ${userStore.token}`,
                'Content-Type': 'application/json',
            }
            }).then((res) => { // 수정한 내용이 나와서 만일 사용하려면 사용할 수 있다.
                detailArticle.value = res.data
                router.push({
                    name:'article-detail',
                    params: {
                        id: res.data.id
                    }
                })
            }).catch((err) => {
                console.log(err)
        })
    }
    const deleteArticleDetail = (article_pk,category)=>{
        axios({
            method: 'delete',
            url: `${BASE_URL}/detail/`,
            data: {
                article_pk : article_pk, // article id 도 같이 받아와서 이를 사보내주면된다.
            },
            headers: {
                Authorization: `Token ${userStore.token}`
            }
            }).then((res) => {
                router.push({name : `${category}-article`})
            }).catch((err) => {
                console.log(err)
        })
    }
    const getCommit = async (article_pk)=>{
        try {
            const res = await axios({
                method: 'get',
                url: `${BASE_URL}/commit/`,
                params: {
                    article_pk : article_pk, // article 찾기용 id
                },
                })
                const temp=res.data.commit
                commits.value = temp// 작성한 댓글 내용이 나와서 만일 사용하려면 사용할 수 있다.
                return res.data
            } catch(err) {
                console.log(err)
                throw err
            }
    }
    const createCommit = async (article_pk,commitContent) => {  // 댓글 작성
        try {
            await axios({
                method: 'post',
                url: `${BASE_URL}/commit/`,
                data: {
                    article_pk : article_pk, // article 찾기용 id
                    content : commitContent, // 댓글 내용
                },
                headers: {
                    Authorization: `Token ${userStore.token}`
                }
                })
        } catch (err) {
            console.log(err)
        }
    }
    const updateCommit = async (commit_pk,commitContent) => {  // 댓글 작성
        try { 
            await axios({
            method: 'put',
            url: `${BASE_URL}/commit/`,
            data: {
                commit_pk : commit_pk, // commit 수정용 id
                content : commitContent, // 댓글 내용
            },
            headers: {
                Authorization: `Token ${userStore.token}`,
                'Content-Type': 'application/json',
            }
        })
        }catch (err) {
            console.log(err)
        }
    }
    const deleteCommit = async (commit_pk) => {  // 댓글 작성
        try {
            await axios({
            method: 'delete',
            url: `${BASE_URL}/commit/`,
            data: {
                commit_pk : commit_pk, // commit 수정용 id
            },
            headers: {
                Authorization: `Token ${userStore.token}`
            }
            })
        }catch (err) {
            console.log(err)
        }
    }
    
    const likeArticle = async (article_pk,articleType)=>{
            const res = await axios({
                method: 'post',
                url: `${BASE_URL}/detail/like/`,
                data: {
                    article_pk : article_pk, // 좋아요 보낼 id
                },
                headers: {
                    Authorization: `Token ${userStore.token}`
                }
            }).then((res)=>{
                getLikeArticle(article_pk)
                getArticleList(articleType)
            }).catch((err)=>{
            console.log(err)
        })
    }
    const getLikeArticle= async (article_pk)=>{
        try {
            const res = await axios({
                method: 'get',
                url: `${BASE_URL}/detail/like/`,
                params: {
                    article_pk : article_pk, // 좋아요 보낼 id
                },
            
                }) 
                const temp=res.data
                likeArticleUser.value = temp
                return res.data
            }
            catch(err) {
                console.log(err)
        }
    }

    return { 
        articleList,// 초기 화면에 입장할 때 받은 해당 게시물에 맞는 list [글 종류, 글 내용, 글 작성자, 글 좋아요 수 , 글의 댓글 수]
        detailArticle, // 상세 조회용 내용, 좋아요 수, 댓글, 작성자 를 받는다.
        commits,
        likeArticleUser,
        likeCommitUser,
        getArticleList, // 초기 화면에 입장할 때 input => (글 종류), 해당 게시물에 맞는 list를 return.
        createArticleList, // 게시물을 작성해 저장할 때 사용, input => (글 종류, 제목, 내용), 저장한 내용을 return.
        getArticleDetail, // 게시물을 상세 조회할 때 사용, input => (글 번호), 저장한 내용을 return.
        updateArticleDetail,  // 게시물을 업데이트 할 때 사용, input => (글 번호, 수정할 제목(빈칸 ok), 수정할 내용(빈칸 ok)), 수정한 내용을 return.
        deleteArticleDetail, // 게시물을 삭제할 때 사용, input => (글 번호), 삭제했다 메시지만 return
        getCommit,
        createCommit, // 댓글을 작성할 때 사용, input => ( 번호, 댓글 내용), 작성한 내용을 return
        updateCommit, // 댓글을 수정할 때 사용, input => (댓글 번호, 댓글 내용), 작성한 내용을 return 
        deleteCommit, // 댓글을 삭제할 때 사용, input => (댓글 번호), 작성한 내용을 return 
        likeArticle, // 게시글을 좋아요 할 때 사용, input => (글 번호), 상태에 따른 like의 값으로 true/false 그리고 메시지 return.
        getLikeArticle,
    }
}, { persist: {
    storage: sessionStorage,
    paths: ['article', ]
} })
