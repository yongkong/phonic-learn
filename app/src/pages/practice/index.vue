<template>
  <view class="practice-page">
    <SiteHeader active="/pages/practice/index" />

    <view class="coming-soon">
      <text class="icon">🎮</text>
      <text class="title">练习</text>
      <text class="desc">Coming Soon</text>
      <text class="hint">更多练习功能即将上线</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import SiteHeader from '@/components/SiteHeader.vue'
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

/* 桌面端顶栏对齐所需的水平内边距 */
@media (min-width: 1024px) {
  .practice-page,
  .essay-page,
  .profile-page {
    padding-left: $space-xl;
    padding-right: $space-xl;
  }
}
</style>
