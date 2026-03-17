import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const isAuthenticated = computed(() => !!user.value)

  function setUser(userData) {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }

  async function register(username, email, password, passwordConfirm) {
    const response = await api.post('/auth/register/', {
      username,
      email,
      password,
      password_confirm: passwordConfirm,
    })
    setUser(response.data)
  }

  async function login(username, password) {
    const response = await api.post('/auth/login/', { username, password })
    setUser(response.data)
  }

  async function logout() {
    await api.post('/auth/logout/')
    user.value = null
    localStorage.removeItem('user')
  }

  async function fetchUser() {
    const response = await api.get('/auth/me/')
    setUser(response.data)
  }

  return { user, isAuthenticated, register, login, logout, fetchUser }
})
