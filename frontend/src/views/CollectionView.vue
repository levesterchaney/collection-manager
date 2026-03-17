<template>
  <div v-if="store.loading" class="animate-pulse">
    <div class="h-8 bg-neutral-800 rounded w-48 mb-4"></div>
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      <div v-for="n in 10" :key="n" class="bg-neutral-900 rounded-xl aspect-square"></div>
    </div>
  </div>

  <div v-else-if="collection">
    <!-- Header -->
    <div class="flex items-start justify-between mb-8 gap-4">
      <div>
        <div class="flex items-center gap-3 mb-1">
          <RouterLink to="/" class="text-neutral-500 hover:text-white text-sm transition-colors">
            Collections
          </RouterLink>
          <span class="text-neutral-600">/</span>
          <span class="text-white text-sm">{{ collection.name }}</span>
        </div>
        <h1 class="text-3xl font-bold text-white">{{ collection.name }}</h1>
        <p v-if="collection.description" class="text-neutral-400 mt-1">{{ collection.description }}</p>

        <div class="flex items-center gap-6 mt-4 text-sm">
          <div>
            <span class="text-neutral-500">Items</span>
            <span class="ml-2 text-white font-semibold">{{ collection.item_count }}</span>
          </div>
          <div>
            <span class="text-neutral-500">Paid</span>
            <span class="ml-2 text-white font-semibold">${{ Number(collection.total_paid).toFixed(2) }}</span>
          </div>
          <div>
            <span class="text-neutral-500">Value</span>
            <span class="ml-2 text-yellow-400 font-semibold">${{ Number(collection.total_value).toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <RouterLink
        :to="{ name: 'NewItem', params: { collectionId: collection.id } }"
        class="shrink-0 px-5 py-2.5 bg-yellow-400 hover:bg-yellow-300 text-black font-semibold rounded-xl transition-colors"
      >
        + Add Item
      </RouterLink>
    </div>

    <!-- Items Grid -->
    <div v-if="collection.items?.length === 0" class="text-center py-24">
      <p class="text-5xl mb-4">🗂️</p>
      <p class="text-xl font-medium text-white">No items yet</p>
      <p class="text-neutral-500 mt-2">Start adding items to your collection.</p>
    </div>

    <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      <ItemCard
        v-for="item in collection.items"
        :key="item.id"
        :item="item"
        @edit="goToEdit(item)"
        @delete="confirmDelete(item)"
      />
    </div>

    <!-- Delete Confirm Modal -->
    <div v-if="itemToDelete" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-neutral-900 border border-neutral-700 rounded-2xl w-full max-w-sm p-6 text-center">
        <p class="text-white font-semibold text-lg mb-2">Delete "{{ itemToDelete.name }}"?</p>
        <p class="text-neutral-400 text-sm mb-6">This action cannot be undone.</p>
        <div class="flex gap-3">
          <button
            @click="itemToDelete = null"
            class="flex-1 py-2.5 rounded-xl border border-neutral-700 text-neutral-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            @click="deleteItem"
            class="flex-1 py-2.5 rounded-xl bg-red-500 hover:bg-red-400 text-white font-semibold transition-colors"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import ItemCard from '@/components/ItemCard.vue'
import { useCollectionsStore } from '@/stores/collections'

const route = useRoute()
const router = useRouter()
const store = useCollectionsStore()
const collection = computed(() => store.currentCollection)
const itemToDelete = ref(null)

onMounted(() => store.fetchCollection(route.params.id))

function goToEdit(item) {
  router.push({ name: 'EditItem', params: { collectionId: collection.value.id, itemId: item.id } })
}

function confirmDelete(item) {
  itemToDelete.value = item
}

async function deleteItem() {
  await store.deleteItem(collection.value.id, itemToDelete.value.id)
  itemToDelete.value = null
}
</script>
