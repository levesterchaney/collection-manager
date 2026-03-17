<template>
  <div class="group rounded-xl border border-neutral-800 bg-neutral-900 overflow-hidden hover:border-neutral-600 transition-colors">
    <div class="aspect-square bg-neutral-800 overflow-hidden">
      <img
        v-if="item.image_url"
        :src="item.image_url"
        :alt="item.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-neutral-600 text-5xl">
        📦
      </div>
    </div>

    <div class="p-3">
      <div class="flex items-start justify-between gap-2">
        <div class="min-w-0">
          <p class="font-medium text-white text-sm truncate">{{ item.name }}</p>
          <p v-if="item.version" class="text-xs text-neutral-500 truncate">{{ item.version }}</p>
        </div>
        <span
          class="shrink-0 text-xs px-2 py-0.5 rounded-full font-medium"
          :class="statusClass"
        >
          {{ item.status.replace('_', ' ') }}
        </span>
      </div>

      <div class="mt-2 flex items-center justify-between text-xs text-neutral-500">
        <span class="truncate">{{ item.manufacturer || item.originating_property || '—' }}</span>
        <span v-if="item.current_value" class="text-yellow-400 font-medium shrink-0 ml-2">
          ${{ Number(item.current_value).toFixed(2) }}
        </span>
      </div>
    </div>

    <div class="px-3 pb-3 flex gap-2">
      <button
        @click="$emit('edit', item)"
        class="flex-1 text-xs py-1.5 rounded-lg border border-neutral-700 hover:border-neutral-500 text-neutral-400 hover:text-white transition-colors"
      >
        Edit
      </button>
      <button
        @click="$emit('delete', item)"
        class="flex-1 text-xs py-1.5 rounded-lg border border-neutral-700 hover:border-red-500/50 text-neutral-400 hover:text-red-400 transition-colors"
      >
        Delete
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  item: { type: Object, required: true }
})

defineEmits(['edit', 'delete'])

const statusClass = computed(() => ({
  'bg-emerald-500/20 text-emerald-400': props.item.status === 'mint',
  'bg-blue-500/20 text-blue-400': props.item.status === 'near_mint',
  'bg-yellow-500/20 text-yellow-400': ['excellent', 'good'].includes(props.item.status),
  'bg-orange-500/20 text-orange-400': props.item.status === 'fair',
  'bg-red-500/20 text-red-400': ['poor', 'damaged'].includes(props.item.status),
}))
</script>
