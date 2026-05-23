<template>
  <view class="summary-page">
    <!-- Completion Header -->
    <view class="completion-header">
      <text class="completion-icon">🎉</text>
      <text class="completion-title">学习完成！</text>
      <text class="completion-sub">太棒了，继续加油！</text>
    </view>

    <!-- Stats -->
    <view class="stats-section">
      <view class="stat-card">
        <text class="stat-value">10</text>
        <text class="stat-label">学习单词</text>
      </view>
      <view class="stat-card">
        <text class="stat-value">5</text>
        <text class="stat-label">完成维度</text>
      </view>
      <view class="stat-card">
        <text class="stat-value">90%</text>
        <text class="stat-label">正确率</text>
      </view>
    </view>

    <!-- Actions -->
    <view class="actions">
      <button class="btn-review" @click="goReview">复习单词</button>
      <button class="btn-home" @click="goHome">返回主页</button>
    </view>
  </view>
</template>

<script setup lang="ts">
const goReview = () => {
  // TODO: 跳转到复习/练习页
  uni.navigateBack()
}

const goHome = () => {
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

.completion-header {
  text-align: center;
  margin-bottom: $space-4xl;
  margin-top: $space-3xl;
}

.completion-icon {
  font-size: 120rpx;
  display: block;
  margin-bottom: $space-lg;
}

.completion-title {
  font-family: $font-display;
  font-size: 48rpx;
  font-weight: bold;
  color: $fg;
  display: block;
}

.completion-sub {
  font-size: 28rpx;
  color: $fg-secondary;
  margin-top: $space-sm;
  display: block;
}

.stats-section {
  display: flex;
  gap: $space-md;
  width: 100%;
  margin-bottom: $space-4xl;
}

.stat-card {
  flex: 1;
  background: $surface;
  border-radius: $radius-md;
  padding: $space-xl;
  text-align: center;
  box-shadow: $shadow-sm;
}

.stat-value {
  font-size: 44rpx;
  font-weight: bold;
  color: $primary;
  display: block;
}

.stat-label {
  font-size: 24rpx;
  color: $fg-secondary;
  margin-top: $space-xs;
  display: block;
}

.actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: $space-md;
}

.btn-review {
  background: $primary;
  color: $fg-inverse;
  border-radius: $radius-pill;
  padding: $space-lg 0;
  font-size: 32rpx;
  font-weight: bold;
  border: none;
}

.btn-home {
  background: $surface;
  color: $primary;
  border-radius: $radius-pill;
  padding: $space-lg 0;
  font-size: 32rpx;
  font-weight: bold;
  border: 2rpx solid $primary;
}
</style>
