<template>
  <nav class="border-b border-neutral-800 bg-neutral-900/80 backdrop-blur-sm sticky top-0 z-50">
    <div class="container mx-auto px-4 flex items-center justify-between h-16">
      <RouterLink to="/" class="text-xl font-bold tracking-tight text-white">
        Manifest
      </RouterLink>
      <div class="flex items-center gap-4">
        <span class="text-sm text-neutral-400">{{ auth.user?.username }}</span>
        <button
          @click="handleLogout"
          class="text-sm text-neutral-400 hover:text-white transition-colors"
        >
          Sign out
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await auth.logout()
  router.push({ name: 'Login' })
}
</script>
