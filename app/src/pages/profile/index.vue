<template>
  <view class="profile-page">
    <!-- User Info Card -->
    <view class="user-card">
      <view class="avatar">
        <text class="avatar-text">小</text>
      </view>
      <view class="user-info">
        <text class="nickname">小学者</text>
        <text class="grade">3年级</text>
      </view>
    </view>

    <!-- Stats Section -->
    <view class="stats-card">
      <view class="stat-item">
        <text class="stat-value">128</text>
        <text class="stat-label">已学单词</text>
      </view>
      <view class="stat-divider"></view>
      <view class="stat-item">
        <text class="stat-value">15</text>
        <text class="stat-label">学习天数</text>
      </view>
      <view class="stat-divider"></view>
      <view class="stat-item">
        <text class="stat-value">92%</text>
        <text class="stat-label">正确率</text>
      </view>
    </view>

    <!-- Settings List -->
    <view class="settings-list">
      <view class="setting-item" @click="handleSetting('badge')">
        <text class="setting-icon">🏅</text>
        <text class="setting-text">我的勋章</text>
        <text class="setting-arrow">></text>
      </view>
      <view class="setting-item" @click="handleSetting('record')">
        <text class="setting-icon">📊</text>
        <text class="setting-text">学习记录</text>
        <text class="setting-arrow">></text>
      </view>
      <view class="setting-item" @click="handleSetting('settings')">
        <text class="setting-icon">⚙️</text>
        <text class="setting-text">设置</text>
        <text class="setting-arrow">></text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  // TODO: 从 userStore 获取用户信息
  // TODO: 调用 getUserStats API 获取学习统计
})

const handleSetting = (type: string) => {
  console.log('Setting clicked:', type)
  // TODO: 根据 type 跳转到对应页面
}
</script>

<style lang="scss" scoped>
.profile-page {
  padding: $space-xl;
  background: $bg;
  min-height: 100vh;
  padding-bottom: calc(100rpx + env(safe-area-inset-bottom));
}

.user-card {
  background: linear-gradient(135deg, $primary 0%, $primary-light 100%);
  border-radius: $radius-lg;
  padding: $space-xl;
  display: flex;
  align-items: center;
  margin-bottom: $space-lg;
  box-shadow: $shadow-md;
}

.avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: $radius-circle;
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: $space-lg;
}

.avatar-text {
  font-size: 40rpx;
  color: $fg-inverse;
  font-weight: bold;
}

.user-info {
  flex: 1;
}

.nickname {
  font-size: 36rpx;
  font-weight: bold;
  color: $fg-inverse;
  display: block;
}

.grade {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.8);
  margin-top: $space-xs;
  display: block;
}

.stats-card {
  background: $surface;
  border-radius: $radius-lg;
  padding: $space-xl;
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin-bottom: $space-lg;
  box-shadow: $shadow-sm;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 40rpx;
  font-weight: bold;
  color: $primary;
  display: block;
}

.stat-label {
  font-size: 22rpx;
  color: $fg-secondary;
  margin-top: $space-xs;
  display: block;
}

.stat-divider {
  width: 2rpx;
  height: 60rpx;
  background: $border;
}

.settings-list {
  background: $surface;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  overflow: hidden;
}

.setting-item {
  display: flex;
  align-items: center;
  padding: $space-lg $space-xl;
  border-bottom: 1rpx solid $border-light;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background: $surface-hover;
  }
}

.setting-icon {
  font-size: 36rpx;
  margin-right: $space-md;
}

.setting-text {
  flex: 1;
  font-size: 30rpx;
  color: $fg;
}

.setting-arrow {
  font-size: 28rpx;
  color: $fg-tertiary;
}
</style>
