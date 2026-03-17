<template>
  <div class="min-h-screen bg-neutral-950">
    <NavBar v-if="auth.isAuthenticated" />
    <main class="container mx-auto px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>
