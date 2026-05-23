<template>
  <view class="practice-page">
    <view class="coming-soon">
      <text class="icon">🎮</text>
      <text class="title">练习</text>
      <text class="desc">Coming Soon</text>
      <text class="hint">更多练习功能即将上线</text>
    </view>
  </view>
</template>

<script setup lang="ts">
// TabBar 页面 - 练习
// TODO: 实现练习功能
</script>

<style lang="scss" scoped>
.practice-page {
  min-height: 100vh;
  background: $bg;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-bottom: calc(100rpx + env(safe-area-inset-bottom));
}

.coming-soon {
  text-align: center;
}

.icon {
  font-size: 120rpx;
  display: block;
  margin-bottom: $space-xl;
}

.title {
  font-family: $font-display;
  font-size: 48rpx;
  font-weight: bold;
  color: $fg;
  display: block;
}

.desc {
  font-size: 32rpx;
  color: $primary;
  font-weight: bold;
  margin-top: $space-md;
  display: block;
}

.hint {
  font-size: 26rpx;
  color: $fg-secondary;
  margin-top: $space-sm;
  display: block;
}
</style>
