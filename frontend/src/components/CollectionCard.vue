<template>
  <RouterLink
    :to="{ name: 'Collection', params: { id: collection.id } }"
    class="block group rounded-2xl border border-neutral-800 bg-neutral-900 hover:border-yellow-500/50 transition-all duration-200 overflow-hidden"
  >
    <div class="aspect-video bg-neutral-800 overflow-hidden relative">
      <img
        v-if="collection.cover_image_url"
        :src="collection.cover_image_url"
        :alt="collection.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-neutral-600">
        <span class="text-4xl">{{ typeEmoji }}</span>
      </div>
      <span class="absolute top-3 left-3 text-xs font-medium px-2 py-1 rounded-full bg-black/60 text-yellow-400 capitalize">
        {{ collection.collection_type }}
      </span>
    </div>

    <div class="p-4">
      <h3 class="font-semibold text-white truncate">{{ collection.name }}</h3>
      <p v-if="collection.description" class="text-sm text-neutral-400 mt-1 line-clamp-2">
        {{ collection.description }}
      </p>

      <div class="mt-4 flex items-center justify-between text-sm">
        <span class="text-neutral-500">{{ collection.item_count }} items</span>
        <span class="text-yellow-400 font-medium">
          ${{ Number(collection.total_value).toFixed(2) }}
        </span>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  collection: { type: Object, required: true }
})

const emojiMap = {
  figures: '🎭', cards: '🃏', comics: '📚', games: '🎮',
  toys: '🧸', coins: '🪙', stamps: '✉️', vinyl: '💿',
  books: '📖', other: '📦',
}

const typeEmoji = computed(() => emojiMap[props.collection.collection_type] || '📦')
</script>
