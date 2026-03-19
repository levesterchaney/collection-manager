import { defineStore } from 'pinia'
import { ref } from 'vue'
import { collectionsApi } from '@/api/collections'
import { itemsApi } from '@/api/items'

export const useCollectionsStore = defineStore('collections', () => {
  const collections = ref([])
  const currentCollection = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchCollections(params = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await collectionsApi.list(params)
      collections.value = response.data.results ?? response.data
    } catch (e) {
      error.value = e.response?.data || 'Failed to fetch collections'
    } finally {
      loading.value = false
    }
  }

  async function fetchCollection(id) {
    loading.value = true
    error.value = null
    try {
      const response = await collectionsApi.get(id)
      currentCollection.value = response.data
    } catch (e) {
      error.value = e.response?.data || 'Failed to fetch collection'
    } finally {
      loading.value = false
    }
  }

  async function createCollection(data) {
    const response = await collectionsApi.create(data)
    collections.value.unshift(response.data)
    return response.data
  }

  async function updateCollection(id, data) {
    const response = await collectionsApi.update(id, data)
    const idx = collections.value.findIndex(c => c.id === id)
    if (idx !== -1) collections.value[idx] = response.data
    if (currentCollection.value?.id === id) currentCollection.value = response.data
    return response.data
  }

  async function deleteCollection(id) {
    await collectionsApi.delete(id)
    collections.value = collections.value.filter(c => c.id !== id)
    if (currentCollection.value?.id === id) currentCollection.value = null
  }

  async function createItem(collectionId, data) {
    data.append("collection", collectionId)
    const response = await itemsApi.create(collectionId, data)
    if (currentCollection.value?.id === collectionId) {
      currentCollection.value.items = [response.data, ...(currentCollection.value.items || [])]
    }
    return response.data
  }

  async function updateItem(collectionId, itemId, data) {
    const response = await itemsApi.update(collectionId, itemId, data)
    if (currentCollection.value?.items) {
      const idx = currentCollection.value.items.findIndex(i => i.id === itemId)
      if (idx !== -1) currentCollection.value.items[idx] = response.data
    }
    return response.data
  }

  async function deleteItem(collectionId, itemId) {
    await itemsApi.delete(collectionId, itemId)
    if (currentCollection.value?.items) {
      currentCollection.value.items = currentCollection.value.items.filter(i => i.id !== itemId)
    }
  }

  return {
    collections, currentCollection, loading, error,
    fetchCollections, fetchCollection,
    createCollection, updateCollection, deleteCollection,
    createItem, updateItem, deleteItem,
  }
})
