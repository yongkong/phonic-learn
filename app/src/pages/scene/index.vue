<template>
  <view class="scene-page">
    <!-- Header -->
    <view class="scene-header">
      <text class="scene-title">{{ scene?.name || '场景单词' }}</text>
      <text class="scene-count">
        {{ loading ? '加载中…' : `${totals.total} 个单词 · 已学 ${totals.learned}` }}
      </text>
    </view>

    <!-- Loading -->
    <view v-if="loading" class="scene-status">
      <view class="loading-dots">
        <view class="dot dot-1"></view>
        <view class="dot dot-2"></view>
        <view class="dot dot-3"></view>
      </view>
    </view>

    <!-- Error -->
    <view v-else-if="loadError" class="scene-status">
      <text class="status-text">加载失败了，请检查网络</text>
      <button class="btn-retry" @click="loadAll">重试</button>
    </view>

    <!-- Sub-scene groups -->
    <view v-else class="sub-groups">
      <view v-for="group in groups" :key="group.id" class="sub-group">
        <view class="group-header">
          <text class="group-name">{{ group.name }}</text>
          <text class="group-progress">{{ group.learned }}/{{ group.words.length }}</text>
        </view>

        <view
          v-for="word in group.words"
          :key="word.id"
          class="word-card"
          @click="openWord(word, group)"
        >
          <view class="word-tile">
            <text class="tile-text">{{ word.spelling.slice(0, 1).toUpperCase() }}</text>
          </view>
          <view class="word-info">
            <view class="word-line">
              <text class="word-text">{{ word.spelling }}</text>
              <text v-if="word.phonetic_us" class="word-phonetic">{{ word.phonetic_us }}</text>
            </view>
            <text class="word-meaning">{{ primaryMeaning(word) }}</text>
          </view>
          <!-- 状态徽章：形状 + 文字（非仅颜色） -->
          <view class="status-chip" :class="statusClass(word)">
            <svg
              class="chip-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.4"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path v-for="(d, i) in statusIconPaths(word)" :key="i" :d="d" />
            </svg>
            <text class="chip-label">{{ statusMeta(word).label }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getScene, getSubSceneWords } from '@/api/scene'
import { getLearningStatusMeta } from '@/utils/learning-status'
import type { Scene, SubScene, WordListItem } from '@/types'

interface SubGroup {
  id: number
  name: string
  learned: number
  words: WordListItem[]
}

const scene = ref<Scene | null>(null)
const groups = ref<SubGroup[]>([])
const loading = ref(true)
const loadError = ref(false)

let sceneId = 0

onLoad((options) => {
  sceneId = Number(options?.id || 0)
  loadAll()
})

async function loadAll() {
  if (!sceneId) {
    loadError.value = true
    loading.value = false
    return
  }
  loading.value = true
  loadError.value = false
  try {
    scene.value = await getScene(sceneId)
    const subs: SubScene[] = scene.value.sub_scenes || []
    const wordLists = await Promise.all(subs.map((sub) => getSubSceneWords(sub.id)))
    groups.value = subs.map((sub, i) => ({
      id: sub.id,
      name: sub.name,
      learned: wordLists[i].filter((w) => w.learning_status !== 'new').length,
      words: wordLists[i],
    }))
  } catch {
    loadError.value = true
  } finally {
    loading.value = false
  }
}

const totals = computed(() => {
  let total = 0
  let learned = 0
  for (const g of groups.value) {
    total += g.words.length
    learned += g.learned
  }
  return { total, learned }
})

function primaryMeaning(word: WordListItem): string {
  const first = word.meanings?.[0]
  return first ? `${first.pos} ${first.cn}` : ''
}

function statusMeta(word: WordListItem) {
  return getLearningStatusMeta(word.learning_status)
}

function statusClass(word: WordListItem): string {
  return `is-${word.learning_status}`
}

// 形状互不相同的线性小图标：新学○ / 学习中◐(半环) / 熟悉☆ / 掌握★
function statusIconPaths(word: WordListItem): string[] {
  switch (statusMeta(word).shape) {
    case 'circle':
      return ['M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z']
    case 'half':
      return ['M12 22a10 10 0 1 1 0-20', 'M12 12h10', 'M12 2a10 10 0 0 1 10 10']
    case 'star-outline':
      return ['M12 3l1.9 5.8L20 10.6l-4.9 3.9 1.6 6-4.7-3.6-4.7 3.6 1.6-6L4 10.6l6.1-1.8z']
    case 'star':
      return ['M12 3l1.9 5.8L20 10.6l-4.9 3.9 1.6 6-4.7-3.6-4.7 3.6 1.6-6L4 10.6l6.1-1.8z']
    default:
      return []
  }
}

function openWord(word: WordListItem, group: SubGroup) {
  uni.navigateTo({
    url: `/pages/learn/index?sceneId=${sceneId}&subSceneId=${group.id}&wordId=${word.id}`,
  })
}
</script>

<style lang="scss" scoped>
.scene-page {
  padding: $space-xl;
  background: $bg;
  min-height: 100vh;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
}

.scene-header {
  margin-bottom: $space-xl;
}

.scene-title {
  font-family: $font-display;
  font-size: 44rpx;
  font-weight: 800;
  color: $fg;
  display: block;
}

.scene-count {
  font-size: 24rpx;
  font-weight: 600;
  color: $fg-secondary;
  margin-top: $space-xs;
  display: block;
}

.scene-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400rpx;
  gap: $space-lg;
}

.status-text {
  font-size: 28rpx;
  font-weight: 600;
  color: $fg-secondary;
}

.btn-retry {
  background: $primary;
  color: $fg-inverse;
  font-size: 28rpx;
  font-weight: 800;
  border-radius: $radius-pill;
  border: none;
  min-height: 88rpx;
  min-width: 240rpx;
  line-height: 88rpx;
  @include press-feedback($edge-primary-sm, none);
}

.sub-groups {
  display: flex;
  flex-direction: column;
  gap: $space-xl;
}

.sub-group {
  background: $surface;
  border: 2rpx solid $border;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  padding: $space-lg;
}

.group-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: $space-md;
}

.group-name {
  font-size: 30rpx;
  font-weight: 800;
  color: $fg;
}

.group-progress {
  font-family: $font-display;
  font-size: 24rpx;
  font-weight: 800;
  color: $fg-secondary;
}

.word-card {
  display: flex;
  align-items: center;
  gap: $space-md;
  background: $bg;
  border: 2rpx solid $border-light;
  border-radius: $radius-md;
  padding: $space-md $space-lg;
  min-height: 120rpx;
  margin-bottom: $space-sm;
  transition: transform $transition-fast;

  &:last-child {
    margin-bottom: 0;
  }

  &:active {
    transform: scale(0.98);
  }
}

.word-tile {
  width: 80rpx;
  height: 80rpx;
  border-radius: $radius-md;
  background: $primary-soft;
  border: 2rpx solid $border;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tile-text {
  font-family: $font-display;
  font-size: 40rpx;
  font-weight: 800;
  color: $primary;
  line-height: 1;
}

.word-info {
  flex: 1;
  min-width: 0;
}

.word-line {
  display: flex;
  align-items: baseline;
  gap: $space-sm;
}

.word-text {
  font-family: $font-display;
  font-size: 32rpx;
  font-weight: 800;
  color: $fg;
}

.word-phonetic {
  font-size: 22rpx;
  font-weight: 600;
  color: $fg-tertiary;
  flex-shrink: 0;
}

.word-meaning {
  font-size: 24rpx;
  font-weight: 600;
  color: $fg-secondary;
  margin-top: 4rpx;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
  padding: $space-xs $space-sm;
  border-radius: $radius-pill;
  background: $surface;
  border: 2rpx solid $border;
  flex-shrink: 0;
  min-width: 88rpx;
  box-sizing: border-box;

  .chip-icon {
    width: 30rpx;
    height: 30rpx;
  }

  .chip-label {
    font-size: 20rpx;
    font-weight: 800;
    line-height: 1.1;
  }

  // 颜色只是辅助，形状 + 文字已经区分状态
  &.is-new {
    color: $fg-tertiary;
  }

  &.is-learning {
    color: $primary;
  }

  &.is-familiar {
    color: $accent-dark;
  }

  &.is-mastered {
    color: $success;
  }
}

.loading-dots {
  display: flex;
  gap: $space-sm;
}

.dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: $radius-circle;
  background: $primary-light;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot-1 { animation-delay: -0.32s; }
.dot-2 { animation-delay: -0.16s; }
.dot-3 { animation-delay: 0s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .dot {
    animation: none;
    opacity: 0.8;
  }
}
</style>
