<template>
  <view class="scene-page">
    <!-- Header -->
    <view class="scene-header">
      <text class="scene-title">{{ scene?.name || '场景单词' }}</text>
      <text v-if="!loading && !loadError" class="scene-count">
        {{ totals.total }} 个单词 · 已学 {{ totals.learned }}
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
      <text class="status-text">{{ sceneId ? '加载失败了，请检查网络' : '缺少场景参数，请从学习地图进入' }}</text>
      <button class="btn-retry" @click="loadAll">{{ sceneId ? '重试' : '返回地图' }}</button>
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
          <!-- 状态徽章：形状（○/◐/☆/★）+ 文字（新学/学习中/熟悉/掌握），颜色仅辅助 -->
          <view class="status-chip" :class="`is-${word.learning_status}`">
            <svg
              class="chip-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.4"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                v-for="(seg, i) in metaOf(word).icon"
                :key="i"
                :d="seg.d"
                :fill="seg.filled ? 'currentColor' : 'none'"
              />
            </svg>
            <text class="chip-label">{{ metaOf(word).label }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { getScene, getSubSceneWords } from '@/api/scene'
import { getLearningStatusMeta, type LearningStatusMeta } from '@/utils/learning-status'
import type { Scene, WordListItem } from '@/types'

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
const sceneId = ref(0)

onLoad((options) => {
  sceneId.value = Number(options?.id || 0)
})

// onShow 刷新：从学习页返回时词表状态可见变化（如 学习中 → 熟悉）。
// 已知平台行为：uni H5 对同路由不同参数的 hash 直达会复用 keep-alive 实例，
// onLoad/onShow 均不触发（见验收记录）；真实路径（首页 navigateTo）不受影响。
onShow(() => {
  if (sceneId.value) loadAll()
})

async function loadAll() {
  if (!sceneId.value) {
    loadError.value = true
    loading.value = false
    return
  }
  loading.value = true
  loadError.value = false
  try {
    scene.value = await getScene(sceneId.value)
    const subs = scene.value.sub_scenes || []
    groups.value = await Promise.all(
      subs.map(async (sub) => {
        const words = await getSubSceneWords(sub.id)
        return {
          id: sub.id,
          name: sub.name,
          learned: words.filter((w) => w.learning_status !== 'new').length,
          words,
        }
      })
    )
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

function metaOf(word: WordListItem): LearningStatusMeta {
  return getLearningStatusMeta(word.learning_status)
}

function openWord(word: WordListItem, group: SubGroup) {
  uni.navigateTo({
    url: `/pages/learn/index?sceneId=${sceneId.value}&subSceneId=${group.id}&wordId=${word.id}`,
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

  // MASTER v2：按压下沉，不缩放
  &:active {
    transform: translateY(4rpx);
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
  min-width: 104rpx;
  box-sizing: border-box;

  .chip-icon {
    width: 32rpx;
    height: 32rpx;
  }

  .chip-label {
    font-size: 24rpx;
    font-weight: 800;
    line-height: 1.1;
  }

  // 颜色只是辅助：形状（○/◐/☆/★）+ 文字已区分状态；均用深色档保证白底对比度 ≥4.5:1
  &.is-new {
    color: $fg-secondary;
  }

  &.is-learning {
    color: $primary;
  }

  &.is-familiar {
    color: $accent-dark;
  }

  &.is-mastered {
    color: $success-dark;
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

/* ===== 桌面端（≥1024px）：子场景分组两列 ===== */
@media (min-width: 1024px) {
  .scene-page {
    max-width: 1080px;
    margin: 0 auto;
    padding-bottom: 48rpx;
  }

  .sub-groups {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
    align-items: start;
  }
}
</style>
