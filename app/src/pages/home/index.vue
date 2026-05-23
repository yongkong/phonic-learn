<template>
  <view class="home-page">
    <!-- User Greeting -->
    <view class="greeting">
      <text class="greeting-text">你好, <text class="nickname">小学者</text></text>
      <text class="progress-text">今日进度: 0/10 单词</text>
    </view>

    <!-- Scene Map Placeholder -->
    <view class="scene-map">
      <view class="map-placeholder">
        <text class="map-title">场景地图</text>
        <text class="map-hint">加载中...</text>
      </view>
    </view>

    <!-- Progress Bar -->
    <view class="progress-section">
      <text class="section-title">学习进度</text>
      <view class="progress-bar">
        <view class="progress-fill" :style="{ width: progressPercent + '%' }"></view>
      </view>
      <text class="progress-label">{{ progressPercent }}%</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const progressPercent = ref(0)

onMounted(() => {
  // TODO: 从 userStore 获取用户信息
  // TODO: 调用 getScenes API 加载场景列表
  // TODO: 计算学习进度
})
</script>

<style lang="scss" scoped>
.home-page {
  padding: $space-xl;
  background: $bg;
  min-height: 100vh;
  padding-bottom: calc(100rpx + env(safe-area-inset-bottom));
}

.greeting {
  margin-bottom: $space-xl;
}

.greeting-text {
  font-size: 36rpx;
  font-weight: bold;
  color: $fg;
}

.nickname {
  color: $primary;
  font-family: $font-display;
}

.progress-text {
  font-size: 24rpx;
  color: $fg-secondary;
  margin-top: $space-xs;
  display: block;
}

.scene-map {
  background: $surface;
  border-radius: $radius-lg;
  padding: $space-xl;
  margin-bottom: $space-xl;
  box-shadow: $shadow-sm;
  min-height: 500rpx;
}

.map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 460rpx;
}

.map-title {
  font-size: 36rpx;
  font-weight: bold;
  color: $fg;
  margin-bottom: $space-md;
}

.map-hint {
  font-size: 28rpx;
  color: $fg-secondary;
}

.progress-section {
  background: $surface;
  border-radius: $radius-lg;
  padding: $space-xl;
  box-shadow: $shadow-sm;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: $fg;
  margin-bottom: $space-md;
  display: block;
}

.progress-bar {
  height: 20rpx;
  background: $border-light;
  border-radius: $radius-pill;
  overflow: hidden;
  margin-bottom: $space-sm;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, $primary, $primary-light);
  border-radius: $radius-pill;
  transition: width $transition-normal;
}

.progress-label {
  font-size: 24rpx;
  color: $fg-secondary;
  text-align: right;
  display: block;
}
</style>
