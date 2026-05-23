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
          <view class="slide-icon">📚</view>
          <text class="slide-title">趣味学单词</text>
          <text class="slide-desc">通过自然拼读法，轻松掌握英语发音规则</text>
        </view>
      </swiper-item>

      <!-- Slide 2 -->
      <swiper-item>
        <view class="slide">
          <view class="slide-icon">🎮</view>
          <text class="slide-title">互动练习</text>
          <text class="slide-desc">五维学习法：认形、发音、拼写、组词、运用</text>
        </view>
      </swiper-item>

      <!-- Slide 3 -->
      <swiper-item>
        <view class="slide">
          <view class="slide-icon">🏆</view>
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
  font-size: 160rpx;
  margin-bottom: $space-3xl;
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
}
</style>
