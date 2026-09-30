<template>
  <view class="onboarding-page">
    <swiper
      class="swiper"
      :indicator-dots="true"
      indicator-color="rgba(255,255,255,0.4)"
      indicator-active-color="#FFFFFF"
      :autoplay="false"
      @change="onSwiperChange"
    >
      <!-- Slide 1 -->
      <swiper-item>
        <view class="slide">
          <view class="slide-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
          </view>
          <text class="slide-title">趣味学单词</text>
          <text class="slide-desc">通过自然拼读法，轻松掌握英语发音规则</text>
        </view>
      </swiper-item>

      <!-- Slide 2 -->
      <swiper-item>
        <view class="slide">
          <view class="slide-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" x2="10" y1="11" y2="11"/><line x1="8" x2="8" y1="9" y2="13"/><line x1="15" x2="15.01" y1="12" y2="12"/><line x1="18" x2="18.01" y1="10" y2="10"/><path d="M17.32 5H6.68a4 4 0 0 0-3.978 3.59c-.006.052-.01.101-.017.152C2.604 9.416 2 14.456 2 16a3 3 0 0 0 3 3c1 0 1.5-.5 2-1l1.414-1.414A2 2 0 0 1 9.828 16h4.344a2 2 0 0 1 1.414.586L17 18c.5.5 1 1 2 1a3 3 0 0 0 3-3c0-1.545-.604-6.584-.685-7.258-.007-.05-.011-.1-.017-.151A4 4 0 0 0 17.32 5z"/></svg>
          </view>
          <text class="slide-title">互动练习</text>
          <text class="slide-desc">五维学习法：认形、识义、拼读、巧记、运用</text>
        </view>
      </swiper-item>

      <!-- Slide 3 -->
      <swiper-item>
        <view class="slide">
          <view class="slide-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"/></svg>
          </view>
          <text class="slide-title">场景学习</text>
          <text class="slide-desc">丰富场景单词，学以致用更有趣</text>
          <button class="btn-start" @click="goRegister">开始学习</button>
        </view>
      </swiper-item>
    </swiper>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const currentSlide = ref(0)

const onSwiperChange = (e: any) => {
  currentSlide.value = e.detail.current
}

const goRegister = () => {
  uni.navigateTo({ url: '/pages/register/index' })
}
</script>

<style lang="scss" scoped>
.onboarding-page {
  min-height: 100vh;
  background: linear-gradient(135deg, $primary-dark 0%, $primary 50%, $primary-light 100%);
}

.swiper {
  width: 100%;
  height: 100vh;
}

.slide {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $space-4xl;
  height: 100%;
}

.slide-icon {
  width: 200rpx;
  height: 200rpx;
  border-radius: $radius-xl;
  background: rgba(255, 255, 255, 0.14);
  border: 2rpx solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $space-3xl;

  svg {
    width: 104rpx;
    height: 104rpx;
    color: $fg-inverse;
  }
}

.slide-title {
  font-family: $font-display;
  font-size: 48rpx;
  font-weight: bold;
  color: $fg-inverse;
  margin-bottom: $space-lg;
}

.slide-desc {
  font-size: 32rpx;
  color: rgba(255, 255, 255, 0.8);
  text-align: center;
  line-height: 1.6;
  margin-bottom: $space-5xl;
}

.btn-start {
  background: $secondary;
  color: $fg-inverse;
  border-radius: $radius-pill;
  padding: $space-lg $space-4xl;
  font-size: 32rpx;
  font-weight: bold;
  border: none;
  margin-top: $space-3xl;
  min-height: 88rpx;
  min-width: 320rpx;
  box-shadow: $edge-accent;
  transition: transform $transition-normal, box-shadow $transition-normal;

  &::after {
    border: none;
  }

  &:active {
    transform: translateY(4rpx);
    box-shadow: $edge-accent-sm;
  }
}
</style>
