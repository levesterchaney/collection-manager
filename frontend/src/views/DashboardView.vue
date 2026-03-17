<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-white">My Collections</h1>
        <p class="text-neutral-400 mt-1">{{ collections.length }} collection{{ collections.length !== 1 ? 's' : '' }}</p>
      </div>
      <button
        @click="showCreateModal = true"
        class="px-5 py-2.5 bg-yellow-400 hover:bg-yellow-300 text-black font-semibold rounded-xl transition-colors"
      >
        + New Collection
      </button>
    </div>

    <div v-if="store.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      <div v-for="n in 4" :key="n" class="rounded-2xl border border-neutral-800 bg-neutral-900 animate-pulse aspect-[4/5]"></div>
    </div>

    <div v-else-if="collections.length === 0" class="text-center py-24">
      <p class="text-6xl mb-4">📦</p>
      <p class="text-xl font-medium text-white">No collections yet</p>
      <p class="text-neutral-500 mt-2">Create your first collection to get started.</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      <CollectionCard
        v-for="collection in collections"
        :key="collection.id"
        :collection="collection"
      />
    </div>

    <!-- Create Collection Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-neutral-900 border border-neutral-700 rounded-2xl w-full max-w-md p-6">
        <h2 class="text-xl font-bold text-white mb-5">New Collection</h2>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-neutral-300 mb-1">Name *</label>
            <input
              v-model="form.name"
              type="text"
              placeholder="My Funko Pop Collection"
              class="w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-2.5 text-white placeholder-neutral-500 focus:outline-none focus:border-yellow-400 transition-colors"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-neutral-300 mb-1">Type *</label>
            <select
              v-model="form.collection_type"
              class="w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-yellow-400 transition-colors"
            >
              <option v-for="(label, val) in collectionTypes" :key="val" :value="val">{{ label }}</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-neutral-300 mb-1">Description</label>
            <textarea
              v-model="form.description"
              rows="3"
              placeholder="What are you collecting?"
              class="w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-2.5 text-white placeholder-neutral-500 focus:outline-none focus:border-yellow-400 transition-colors resize-none"
            ></textarea>
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button
            @click="showCreateModal = false"
            class="flex-1 py-2.5 rounded-xl border border-neutral-700 text-neutral-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            @click="createCollection"
            :disabled="!form.name || creating"
            class="flex-1 py-2.5 rounded-xl bg-yellow-400 hover:bg-yellow-300 disabled:opacity-50 disabled:cursor-not-allowed text-black font-semibold transition-colors"
          >
            {{ creating ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import CollectionCard from '@/components/CollectionCard.vue'
import { useCollectionsStore } from '@/stores/collections'

const store = useCollectionsStore()
const collections = computed(() => store.collections)
const showCreateModal = ref(false)
const creating = ref(false)

const form = ref({ name: '', collection_type: 'other', description: '' })

const collectionTypes = {
  figures: 'Action Figures', cards: 'Trading Cards', comics: 'Comics',
  games: 'Games', toys: 'Toys', coins: 'Coins', stamps: 'Stamps',
  vinyl: 'Vinyl Records', books: 'Books', other: 'Other',
}

onMounted(() => store.fetchCollections())

async function createCollection() {
  if (!form.value.name) return
  creating.value = true
  try {
    const fd = new FormData()
    Object.entries(form.value).forEach(([k, v]) => fd.append(k, v))
    await store.createCollection(fd)
    showCreateModal.value = false
    form.value = { name: '', collection_type: 'other', description: '' }
  } finally {
    creating.value = false
  }
}
</script>
