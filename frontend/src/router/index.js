import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/collections/:id',
    name: 'Collection',
    component: () => import('@/views/CollectionView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/collections/:collectionId/items/new',
    name: 'NewItem',
    component: () => import('@/views/ItemFormView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/collections/:collectionId/items/:itemId/edit',
    name: 'EditItem',
    component: () => import('@/views/ItemFormView.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'Login' })
  } else if (to.meta.requiresGuest && auth.isAuthenticated) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
