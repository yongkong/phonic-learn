<template>
  <view class="summary-page">
    <!-- Loading -->
    <view v-if="loading" class="page-status">
      <view class="loading-dots">
        <view class="dot dot-1"></view>
        <view class="dot dot-2"></view>
        <view class="dot dot-3"></view>
      </view>
    </view>

    <!-- 空态：没有学习记录（如直接进入本页） -->
    <view v-else-if="empty" class="page-status empty">
      <view class="trophy muted">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
          <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
          <path d="M4 22h16" />
          <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22" />
          <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22" />
          <path d="M18 2H6v7a6 6 0 0 0 12 0V2z" />
        </svg>
      </view>
      <text class="empty-title">还没有学习记录</text>
      <text class="empty-sub">去学习地图挑一个场景，开始你的第一课吧</text>
      <button class="btn-primary" @click="goHome">去学习地图</button>
    </view>

    <!-- Error -->
    <view v-else-if="loadError" class="page-status">
      <text class="empty-title">加载失败了</text>
      <text class="empty-sub">请检查网络后重试</text>
      <button class="btn-primary" @click="loadStats()">重试</button>
    </view>

    <!-- 正常小结 -->
    <template v-else>
      <view class="completion-header">
        <view class="trophy">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
            <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
            <path d="M4 22h16" />
            <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22" />
            <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22" />
            <path d="M18 2H6v7a6 6 0 0 0 12 0V2z" />
          </svg>
        </view>
        <text class="completion-title">学习完成！</text>
        <text class="completion-sub">今天也坚持了，真棒</text>
      </view>

      <!-- 本次统计（全部来自后端 /learning/stats） -->
      <view class="stats-section">
        <view class="stat-card">
          <text class="stat-value">{{ stats?.today_learned ?? 0 }}</text>
          <text class="stat-label">本次学词</text>
        </view>
        <view class="stat-card">
          <text class="stat-value">{{ dimensionPercent }}%</text>
          <text class="stat-label">五维完成度</text>
        </view>
        <view class="stat-card">
          <text class="stat-value">{{ stats?.learned_words ?? 0 }}</text>
          <text class="stat-label">已学会</text>
        </view>
      </view>

      <!-- 掌握情况 -->
      <view class="mastery-card">
        <text class="mastery-title">掌握情况</text>
        <view class="mastery-row">
          <view class="mastery-item">
            <text class="mastery-num">{{ stats?.learned_words ?? 0 }}</text>
            <text class="mastery-label">学习中</text>
          </view>
          <view class="mastery-item">
            <text class="mastery-num">{{ stats?.mastered_words ?? 0 }}</text>
            <text class="mastery-label">已掌握</text>
          </view>
          <view class="mastery-item">
            <text class="mastery-num">{{ stats?.pending_review ?? 0 }}</text>
            <text class="mastery-label">待复习</text>
          </view>
        </view>
      </view>

      <!-- 下次复习时间（简化 SM-2） -->
      <view class="review-card">
        <view class="review-head">
          <svg class="review-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10" />
            <path d="M12 6v6l4 2" />
          </svg>
          <text class="review-title">下次复习</text>
        </view>
        <text class="review-time">{{ nextReviewText }}</text>
        <text class="review-hint">按遗忘曲线安排，到时间记得回来复习哦</text>
      </view>

      <!-- Actions -->
      <view class="actions">
        <button class="btn-primary" @click="goHome">回到学习地图</button>
      </view>
    </template>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { getLearningStats } from '@/api/learning'
import type { LearningStats } from '@/types'

const stats = ref<LearningStats | null>(null)
const loading = ref(true)
const loadError = ref(false)

onLoad(() => {
  loadStats()
})

// 从学习页 redirectTo 过来时 stats 可能因时序拿到空，onShow 再刷新一次
onShow(() => {
  if (!loading.value) loadStats(true)
})

async function loadStats(silent = false) {
  if (!silent) loading.value = true
  loadError.value = false
  try {
    stats.value = await getLearningStats()
  } catch {
    loadError.value = true
  } finally {
    loading.value = false
  }
}

const empty = computed(() => !loadError.value && (stats.value?.total_words ?? 0) === 0)

// 五维完成度：已完成维度 / （已学词数 × 5），无学习记录时为 0
const dimensionPercent = computed(() => {
  const s = stats.value
  if (!s || s.learned_words === 0) return 0
  return Math.min(100, Math.round((s.dimensions_completed / (s.learned_words * 5)) * 100))
})

const nextReviewText = computed(() => {
  const raw = stats.value?.next_review_at
  if (!raw) return '暂无复习安排'
  const d = new Date(raw)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getMonth() + 1}月${d.getDate()}日 ${pad(d.getHours())}:${pad(d.getMinutes())}`
})

function goHome() {
  uni.switchTab({ url: '/pages/home/index' })
}
</script>

<style lang="scss" scoped>
.summary-page {
  padding: $space-xl;
  background: $bg;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-status {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: $space-md;
  min-height: 500rpx;
}

.completion-header {
  text-align: center;
  margin: $space-3xl 0 $space-2xl;
}

.trophy {
  width: 160rpx;
  height: 160rpx;
  border-radius: $radius-xl;
  background: $accent-soft;
  color: $accent-dark;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto $space-lg;

  svg {
    width: 84rpx;
    height: 84rpx;
  }

  &.muted {
    background: $surface;
    color: $fg-tertiary;
  }
}

.completion-title {
  font-family: $font-display;
  font-size: 48rpx;
  font-weight: 800;
  color: $fg;
  display: block;
}

.completion-sub {
  font-size: 28rpx;
  font-weight: 600;
  color: $fg-secondary;
  margin-top: $space-sm;
  display: block;
}

.empty-title {
  font-size: 32rpx;
  font-weight: 800;
  color: $fg;
}

.empty-sub {
  font-size: 26rpx;
  font-weight: 600;
  color: $fg-secondary;
  text-align: center;
  line-height: 1.6;
}

.stats-section {
  display: flex;
  gap: $space-md;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: $space-lg;
}

.stat-card {
  flex: 1;
  background: $surface;
  border: 2rpx solid $border;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  padding: $space-lg $space-md;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $space-xs;
}

.stat-value {
  font-family: $font-display;
  font-size: 52rpx;
  font-weight: 800;
  color: $primary;
  line-height: 1.1;
}

.stat-label {
  font-size: 24rpx;
  font-weight: 700;
  color: $fg-secondary;
}

.mastery-card {
  width: 100%;
  box-sizing: border-box;
  background: $surface;
  border: 2rpx solid $border;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  padding: $space-lg $space-xl;
  margin-bottom: $space-lg;
}

.mastery-title {
  font-size: 28rpx;
  font-weight: 800;
  color: $fg;
  display: block;
  margin-bottom: $space-md;
}

.mastery-row {
  display: flex;
}

.mastery-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
}

.mastery-num {
  font-family: $font-display;
  font-size: 40rpx;
  font-weight: 800;
  color: $fg;
  line-height: 1.1;
}

.mastery-label {
  font-size: 24rpx;
  font-weight: 700;
  color: $fg-secondary;
}

.review-card {
  width: 100%;
  box-sizing: border-box;
  background: $primary-soft;
  border: 2rpx solid $border;
  border-radius: $radius-lg;
  padding: $space-lg $space-xl;
  margin-bottom: $space-2xl;
}

.review-head {
  display: flex;
  align-items: center;
  gap: $space-sm;
}

.review-icon {
  width: 34rpx;
  height: 34rpx;
  color: $primary;
}

.review-title {
  font-size: 26rpx;
  font-weight: 800;
  color: $primary-dark;
}

.review-time {
  font-family: $font-display;
  font-size: 44rpx;
  font-weight: 800;
  color: $fg;
  margin-top: $space-sm;
  display: block;
}

.review-hint {
  font-size: 24rpx;
  font-weight: 600;
  color: $fg-secondary;
  margin-top: $space-xs;
  display: block;
  line-height: 1.5;
}

.actions {
  width: 100%;
  box-sizing: border-box;
  display: flex;
  gap: $space-md;
}

.btn-primary {
  flex: 1;
  background: $primary;
  color: $fg-inverse;
  border-radius: $radius-pill;
  border: none;
  min-height: 96rpx;
  line-height: 96rpx;
  font-size: 30rpx;
  font-weight: 800;
  @include press-feedback;
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
