import { createRouter, createWebHistory } from 'vue-router'
import Swal from 'sweetalert2'

import HomeView from '@/views/HomeView.vue'
import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import UserProfileView from '@/views/UserProfileView.vue'
import { useUserStore } from '@/stores/user'
import { useArticleStore } from '@/stores/articles'
import UserUpdateView from '@/views/UserUpdateView.vue'
import UserProductView from '@/views/UserProductView.vue'
import ProductView from '@/views/ProductView.vue'
import ProductDepositView from '@/views/ProductDepositView.vue'
import ProductSavingView from '@/views/ProductSavingView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import MapView from '@/views/MapView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import ArticleView from '@/views/ArticleView.vue'
import FreeArticleView from '@/views/FreeArticleView.vue'
import ArticleSaveView from '@/views/ArticleSaveView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
import AnnouncementArticleView from '@/views/AnnouncementArticleView.vue'
import ProductUpdateView from '@/views/ProductUpdateView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
    {
      path: '/signup',
      name:  'signup',
      component: SignUpView
    },
    {
      path: '/map',
      name:  'map',
      component: MapView
    },
    {
      path: '/my-profile',
      component: UserProfileView,
      children: [
        {
          path: '',
          name: 'my-profile',
          component: UserUpdateView,
        },
        { 
          path: 'my-product',
          name: 'my-product',
          component: UserProductView
        }
      ]
    },
    {
      path: '/product',
      component: ProductView,
      children: [
        {
          path: 'deposit',
          name: 'product-deposit',
          component: ProductDepositView
        },
        {
          path: 'saving',
          name: 'product-saving',
          component: ProductSavingView
        },
        {
          path: ':category/detail/:code',
          name: 'product-detail',
          component: ProductDetailView
        },
        {
          path: ':category/detail/:code/update',
          name: 'product-update',
          component: ProductUpdateView,
          beforeEnter: (to, from) => {
            const userStore = useUserStore()
            if(userStore.isSuperUser === false) {
              Swal.fire({
                text: '관리자 계정이 아닙니다.',
                icon: 'warning',
                confirmButtonText: '확인',
                confirmButtonColor: '#dce9be'
              })
              return  { name: 'home' }
            }
          }
        }
      ]
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeView
    },
    {
      path: '/article',
      component: ArticleView,
      children :[
        {
          path: 'free',
          name: 'free-article',
          component: FreeArticleView,
        },// 새로운 게시글 목록의 이름은 category-article로 통일해야 작성 후 return 가능합니다.
        {
          path: 'announcement',
          name: 'announcement-article',
          component: AnnouncementArticleView,
        },
        {
          path: ':category/detail/:id',
          name: 'article-detail',
          component: ArticleDetailView,
        },
        {
          path: ':category/detail/:id/update',
          name: 'update-article',
          component: ArticleUpdateView,
        },
        {
          path: ':category/make',
          name: 'make-article',
          component: ArticleSaveView
        }
      ]
    }
  ],
})
router.beforeEach((to) => {
  const userStore = useUserStore()
  if ((to.name === 'login' || to.name === 'signup') && userStore.isAuthenticated === true) {
    Swal.fire({
      text: '로그인 하셨습니다.',
      icon: 'warning',
      confirmButtonText: '확인',
      confirmButtonColor: '#dce9be'
    })
    return { name : 'home' }
  }
  
})

export default router
