<template>
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M11 5L6 9H2v6h4l5 4z" :fill="filled ? 'currentColor' : 'none'" />
    <path v-if="wave === 1 || wave === 2" d="M15.54 8.46a5 5 0 0 1 0 7.07" />
    <path v-if="wave === 2" d="M19.07 4.93a10 10 0 0 1 0 14.14" />
  </svg>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ filled?: boolean; wave?: 0 | 1 | 2 }>(), {
  filled: false,
  wave: 1,
})
</script>
