<template>
  <view class="splash-page">
    <view class="logo-container">
      <text class="logo-text">WordWorld</text>
      <text class="logo-subtitle">自然拼读学习</text>
    </view>
    <view class="loading-dots">
      <view class="dot dot-1"></view>
      <view class="dot dot-2"></view>
      <view class="dot dot-3"></view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onShow } from '@dcloudio/uni-app'

onShow(() => {
  // 3秒后根据用户状态跳转
  setTimeout(() => {
    // TODO: 接入 userStore 检查用户是否已注册
    const isRegistered = false // userStore.isLoggedIn
    if (isRegistered) {
      uni.switchTab({ url: '/pages/home/index' })
    } else {
      uni.navigateTo({ url: '/pages/onboarding/index' })
    }
  }, 3000)
})
</script>

<style lang="scss" scoped>
.splash-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, $primary 0%, $primary-light 100%);
}

.logo-container {
  text-align: center;
  margin-bottom: $space-4xl;
}

.logo-text {
  font-family: $font-display;
  font-size: 80rpx;
  font-weight: bold;
  color: $fg-inverse;
  display: block;
}

.logo-subtitle {
  font-size: 32rpx;
  color: rgba(255, 255, 255, 0.85);
  margin-top: $space-md;
  display: block;
}

.loading-dots {
  display: flex;
  gap: $space-sm;
}

.dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: $radius-circle;
  background: rgba(255, 255, 255, 0.6);
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot-1 { animation-delay: -0.32s; }
.dot-2 { animation-delay: -0.16s; }
.dot-3 { animation-delay: 0s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}
</style>
