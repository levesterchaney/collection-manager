<template>
  <div class="max-w-2xl mx-auto">
    <div class="flex items-center gap-3 mb-8">
      <RouterLink
        :to="{ name: 'Collection', params: { id: collectionId } }"
        class="text-neutral-500 hover:text-white transition-colors"
      >
        ← Back
      </RouterLink>
      <h1 class="text-2xl font-bold text-white">{{ isEdit ? 'Edit Item' : 'New Item' }}</h1>
    </div>

    <div class="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 space-y-5">
      <div class="grid grid-cols-2 gap-4">
        <div class="col-span-2">
          <label class="block text-sm font-medium text-neutral-300 mb-1">Name *</label>
          <input v-model="form.name" type="text" class="input-field" placeholder="Item name" />
        </div>

        <div>
          <label class="block text-sm font-medium text-neutral-300 mb-1">Version</label>
          <input v-model="form.version" type="text" class="input-field" placeholder="v1, 2023 Ed." />
        </div>

        <div>
          <label class="block text-sm font-medium text-neutral-300 mb-1">Status</label>
          <select v-model="form.status" class="input-field">
            <option v-for="(label, val) in statusOptions" :key="val" :value="val">{{ label }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-neutral-300 mb-1">Manufacturer</label>
          <input v-model="form.manufacturer" type="text" class="input-field" placeholder="Hasbro, Bandai..." />
        </div>

        <div>
          <label class="block text-sm font-medium text-neutral-300 mb-1">Originating Property</label>
          <input v-model="form.originating_property" type="text" class="input-field" placeholder="Star Wars, Pokémon..." />
        </div>

        <div>
          <label class="block text-sm font-medium text-neutral-300 mb-1">Price Paid ($)</label>
          <input v-model="form.price_paid" type="number" step="0.01" min="0" class="input-field" placeholder="0.00" />
        </div>

        <div>
          <label class="block text-sm font-medium text-neutral-300 mb-1">Current Value ($)</label>
          <input v-model="form.current_value" type="number" step="0.01" min="0" class="input-field" placeholder="0.00" />
        </div>

        <div>
          <label class="block text-sm font-medium text-neutral-300 mb-1">Date Acquired</label>
          <input v-model="form.acquired_at" type="date" class="input-field" />
        </div>

        <div>
          <label class="block text-sm font-medium text-neutral-300 mb-1">Image</label>
          <input
            type="file"
            accept="image/*"
            @change="handleImage"
            class="w-full text-sm text-neutral-400 file:mr-3 file:py-2 file:px-3 file:rounded-lg file:border-0 file:bg-neutral-700 file:text-white file:cursor-pointer hover:file:bg-neutral-600"
          />
        </div>

        <div class="col-span-2">
          <label class="block text-sm font-medium text-neutral-300 mb-1">Description</label>
          <textarea v-model="form.description" rows="3" class="input-field resize-none" placeholder="Notes about this item..."></textarea>
        </div>
      </div>

      <div class="flex gap-3 pt-2">
        <RouterLink
          :to="{ name: 'Collection', params: { id: collectionId } }"
          class="flex-1 py-3 rounded-xl border border-neutral-700 text-neutral-400 hover:text-white transition-colors text-center"
        >
          Cancel
        </RouterLink>
        <button
          @click="submit"
          :disabled="!form.name || submitting"
          class="flex-1 py-3 rounded-xl bg-yellow-400 hover:bg-yellow-300 disabled:opacity-50 disabled:cursor-not-allowed text-black font-semibold transition-colors"
        >
          {{ submitting ? 'Saving...' : (isEdit ? 'Save Changes' : 'Add Item') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useCollectionsStore } from '@/stores/collections'
import { itemsApi } from '@/api/items'

const route = useRoute()
const router = useRouter()
const store = useCollectionsStore()

const collectionId = route.params.collectionId
const itemId = route.params.itemId
const isEdit = computed(() => !!itemId)
const submitting = ref(false)
const imageFile = ref(null)

const form = ref({
  name: '', version: '', description: '', price_paid: '',
  current_value: '', manufacturer: '', originating_property: '',
  status: 'good', acquired_at: '',
})

const statusOptions = {
  mint: 'Mint', near_mint: 'Near Mint', excellent: 'Excellent',
  good: 'Good', fair: 'Fair', poor: 'Poor', damaged: 'Damaged',
}

onMounted(async () => {
  if (isEdit.value) {
    const response = await itemsApi.get(collectionId, itemId)
    const item = response.data
    Object.keys(form.value).forEach(k => {
      if (item[k] !== undefined && item[k] !== null) form.value[k] = item[k]
    })
  }
})

function handleImage(e) {
  imageFile.value = e.target.files[0] || null
}

async function submit() {
  if (!form.value.name) return
  submitting.value = true

  try {
    const fd = new FormData()
    Object.entries(form.value).forEach(([k, v]) => {
      if (v !== '' && v !== null) fd.append(k, v)
    })
    if (imageFile.value) fd.append('image', imageFile.value)

    if (isEdit.value) {
      await store.updateItem(collectionId, itemId, fd)
    } else {
      await store.createItem(collectionId, fd)
    }

    router.push({ name: 'Collection', params: { id: collectionId } })
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.input-field {
  @apply w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-2.5 text-white placeholder-neutral-500 focus:outline-none focus:border-yellow-400 transition-colors;
}
</style>
