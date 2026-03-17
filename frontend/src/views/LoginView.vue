<template>
  <div class="min-h-screen flex items-center justify-center bg-neutral-950">
    <div class="w-full max-w-md px-6">
      <div class="text-center mb-10">
        <h1 class="text-4xl font-bold text-white tracking-tight">Manifest</h1>
        <p class="text-neutral-400 mt-2">Your collections, catalogued.</p>
      </div>

      <div class="bg-neutral-900 border border-neutral-800 rounded-2xl p-8">
        <!-- Tab toggle -->
        <div class="flex rounded-xl bg-neutral-800 p-1 mb-6">
          <button
            @click="mode = 'login'"
            class="flex-1 py-2 text-sm font-medium rounded-lg transition-colors"
            :class="mode === 'login'
              ? 'bg-neutral-700 text-white'
              : 'text-neutral-400 hover:text-white'"
          >
            Sign in
          </button>
          <button
            @click="mode = 'register'"
            class="flex-1 py-2 text-sm font-medium rounded-lg transition-colors"
            :class="mode === 'register'
              ? 'bg-neutral-700 text-white'
              : 'text-neutral-400 hover:text-white'"
          >
            Create account
          </button>
        </div>

        <form @submit.prevent="submit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-neutral-300 mb-1">Username</label>
            <input
              v-model="form.username"
              type="text"
              required
              autocomplete="username"
              class="w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-2.5 text-white placeholder-neutral-500 focus:outline-none focus:border-yellow-400 transition-colors"
              placeholder="your_username"
            />
          </div>

          <div v-if="mode === 'register'">
            <label class="block text-sm font-medium text-neutral-300 mb-1">Email</label>
            <input
              v-model="form.email"
              type="email"
              autocomplete="email"
              class="w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-2.5 text-white placeholder-neutral-500 focus:outline-none focus:border-yellow-400 transition-colors"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-neutral-300 mb-1">Password</label>
            <input
              v-model="form.password"
              type="password"
              required
              autocomplete="current-password"
              class="w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-2.5 text-white placeholder-neutral-500 focus:outline-none focus:border-yellow-400 transition-colors"
              placeholder="••••••••"
            />
          </div>

          <div v-if="mode === 'register'">
            <label class="block text-sm font-medium text-neutral-300 mb-1">Confirm Password</label>
            <input
              v-model="form.passwordConfirm"
              type="password"
              autocomplete="new-password"
              class="w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-2.5 text-white placeholder-neutral-500 focus:outline-none focus:border-yellow-400 transition-colors"
              placeholder="••••••••"
            />
          </div>

          <p v-if="error" class="text-red-400 text-sm">{{ error }}</p>

          <button
            type="submit"
            :disabled="submitting"
            class="w-full py-3 rounded-xl bg-yellow-400 hover:bg-yellow-300 disabled:opacity-50 disabled:cursor-not-allowed text-black font-semibold transition-colors mt-2"
          >
            {{ submitting ? 'Please wait...' : (mode === 'login' ? 'Sign in' : 'Create account') }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const mode = ref('login')
const submitting = ref(false)
const error = ref(null)

const form = ref({ username: '', email: '', password: '', passwordConfirm: '' })

watch(mode, () => {
  error.value = null
  form.value = { username: '', email: '', password: '', passwordConfirm: '' }
})

async function submit() {
  error.value = null
  submitting.value = true
  try {
    if (mode.value === 'login') {
      await auth.login(form.value.username, form.value.password)
    } else {
      await auth.register(
        form.value.username,
        form.value.email,
        form.value.password,
        form.value.passwordConfirm
      )
    }
    router.push({ name: 'Dashboard' })
  } catch (e) {
    const data = e.response?.data
    if (typeof data === 'object') {
      error.value = Object.values(data).flat().join(' ')
    } else {
      error.value = 'Something went wrong. Please try again.'
    }
  } finally {
    submitting.value = false
  }
}
</script>
