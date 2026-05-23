<template>
  <view class="learn-page">
    <!-- Dimension Progress -->
    <view class="dimension-header">
      <view class="dimension-info">
        <text class="dimension-title">五维学习</text>
        <text class="dimension-current">维度 {{ currentDimension }}/5</text>
      </view>
      <view class="dimension-steps">
        <view
          v-for="i in 5"
          :key="i"
          class="step-dot"
          :class="{
            active: i === currentDimension,
            completed: i < currentDimension
          }"
        >
          <text class="step-label">{{ stepNames[i - 1] }}</text>
        </view>
      </view>
    </view>

    <!-- Dimension Content Placeholder -->
    <view class="dimension-content">
      <view class="content-placeholder">
        <text class="placeholder-icon">{{ currentDimensionIcon }}</text>
        <text class="placeholder-title">{{ currentDimensionName }}</text>
        <text class="placeholder-desc">学习内容加载中...</text>
      </view>
    </view>

    <!-- Navigation -->
    <view class="dimension-nav">
      <button class="btn-prev" @click="prevDimension" :disabled="currentDimension <= 1">
        上一维度
      </button>
      <button class="btn-next" @click="nextDimension">
        {{ currentDimension < 5 ? '下一维度' : '完成学习' }}
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const currentDimension = ref(1)

const stepNames = ['认形', '发音', '拼写', '组词', '运用']

const currentDimensionName = computed(() => {
  return stepNames[currentDimension.value - 1] || ''
})

const currentDimensionIcon = computed(() => {
  const icons = ['👁️', '🔊', '✍️', '🧩', '🎯']
  return icons[currentDimension.value - 1] || '📖'
})

const prevDimension = () => {
  if (currentDimension.value > 1) {
    currentDimension.value--
  }
}

const nextDimension = () => {
  if (currentDimension.value < 5) {
    currentDimension.value++
  } else {
    // TODO: 完成学习，跳转到 summary 页
    uni.navigateTo({ url: '/pages/summary/index' })
  }
}
</script>

<style lang="scss" scoped>
.learn-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: $bg;
  padding: $space-xl;
  padding-bottom: calc(100rpx + env(safe-area-inset-bottom));
}

.dimension-header {
  margin-bottom: $space-xl;
}

.dimension-info {
  text-align: center;
  margin-bottom: $space-md;
}

.dimension-title {
  font-size: 36rpx;
  font-weight: bold;
  color: $fg;
  display: block;
}

.dimension-current {
  font-size: 28rpx;
  color: $primary;
  font-weight: bold;
  display: block;
  margin-top: $space-xs;
}

.dimension-steps {
  display: flex;
  justify-content: space-between;
  padding: $space-sm 0;
}

.step-dot {
  flex: 1;
  text-align: center;
  position: relative;

  &.active .step-label {
    color: $primary;
    font-weight: bold;
  }

  &.completed .step-label {
    color: $success;
  }
}

.step-label {
  font-size: 22rpx;
  color: $fg-tertiary;
}

.dimension-content {
  flex: 1;
  margin-bottom: $space-xl;
}

.content-placeholder {
  background: $surface;
  border-radius: $radius-lg;
  padding: $space-3xl;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 600rpx;
  box-shadow: $shadow-sm;
}

.placeholder-icon {
  font-size: 120rpx;
  margin-bottom: $space-xl;
}

.placeholder-title {
  font-size: 40rpx;
  font-weight: bold;
  color: $fg;
  margin-bottom: $space-md;
}

.placeholder-desc {
  font-size: 28rpx;
  color: $fg-secondary;
}

.dimension-nav {
  display: flex;
  gap: $space-md;
}

.btn-prev {
  flex: 1;
  background: $border;
  color: $fg-secondary;
  border-radius: $radius-pill;
  padding: $space-lg 0;
  font-size: 30rpx;
  border: none;

  &[disabled] {
    opacity: 0.4;
  }
}

.btn-next {
  flex: 1;
  background: $primary;
  color: $fg-inverse;
  border-radius: $radius-pill;
  padding: $space-lg 0;
  font-size: 30rpx;
  font-weight: bold;
  border: none;
}
</style>
