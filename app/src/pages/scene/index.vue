<template>
  <view class="scene-page">
    <view class="scene-header">
      <text class="scene-title">场景单词</text>
      <text class="scene-count">加载中...</text>
    </view>

    <!-- Word List Placeholder -->
    <view class="word-list">
      <view v-for="i in 5" :key="i" class="word-card placeholder">
        <view class="word-icon"></view>
        <view class="word-info">
          <text class="word-text">单词 {{ i }}</text>
          <text class="word-meaning">释义加载中...</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
// TODO: 接收 sceneId 参数
// TODO: 调用 getSceneWords API 加载单词列表
</script>

<style lang="scss" scoped>
.scene-page {
  padding: $space-xl;
  background: $bg;
  min-height: 100vh;
}

.scene-header {
  margin-bottom: $space-xl;
}

.scene-title {
  font-size: 40rpx;
  font-weight: bold;
  color: $fg;
  display: block;
}

.scene-count {
  font-size: 24rpx;
  color: $fg-secondary;
  margin-top: $space-xs;
  display: block;
}

.word-list {
  display: flex;
  flex-direction: column;
  gap: $space-md;
}

.word-card {
  background: $surface;
  border-radius: $radius-md;
  padding: $space-lg;
  display: flex;
  align-items: center;
  box-shadow: $shadow-sm;

  &.placeholder {
    opacity: 0.6;
  }
}

.word-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: $radius-md;
  background: $border-light;
  margin-right: $space-md;
}

.word-info {
  flex: 1;
}

.word-text {
  font-size: 32rpx;
  font-weight: bold;
  color: $fg;
  display: block;
}

.word-meaning {
  font-size: 24rpx;
  color: $fg-secondary;
  margin-top: $space-xs;
  display: block;
}
</style>
