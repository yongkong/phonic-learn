<template>
  <view class="register-page">
    <view class="header">
      <text class="title">欢迎来到 WordWorld</text>
      <text class="subtitle">创建你的学习账号</text>
    </view>

    <view class="form">
      <!-- Nickname Input -->
      <view class="form-item">
        <text class="label">你的昵称</text>
        <input
          class="input"
          v-model="nickname"
          placeholder="请输入昵称"
          maxlength="20"
        />
      </view>

      <!-- Grade Selection -->
      <view class="form-item">
        <text class="label">选择年级</text>
        <view class="grade-grid">
          <view
            v-for="grade in 6"
            :key="grade"
            class="grade-item"
            :class="{ active: selectedGrade === grade }"
            @click="selectedGrade = grade"
          >
            <text class="grade-text">{{ grade }}年级</text>
          </view>
        </view>
      </view>

      <!-- Register Button -->
      <button
        class="btn-register"
        :disabled="!canRegister"
        :class="{ disabled: !canRegister }"
        @click="handleRegister"
      >
        开始学习之旅
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const nickname = ref('')
const selectedGrade = ref(0)

const canRegister = computed(() => {
  return nickname.value.trim().length > 0 && selectedGrade.value > 0
})

const handleRegister = async () => {
  if (!canRegister.value) return

  // TODO: 调用 registerUser API
  // const res = await registerUser({ nickname: nickname.value, grade: selectedGrade.value })

  // TODO: 保存到 userStore
  // userStore.setUser(res.data)

  // 跳转到主页
  uni.switchTab({ url: '/pages/home/index' })
}
</script>

<style lang="scss" scoped>
.register-page {
  min-height: 100vh;
  background: $bg;
  padding: $space-4xl $space-xl;
}

.header {
  text-align: center;
  margin-bottom: $space-4xl;
}

.title {
  font-family: $font-display;
  font-size: 48rpx;
  font-weight: bold;
  color: $fg;
  display: block;
}

.subtitle {
  font-size: 28rpx;
  color: $fg-secondary;
  margin-top: $space-sm;
  display: block;
}

.form {
  background: $surface;
  border-radius: $radius-lg;
  padding: $space-xl;
  box-shadow: $shadow-sm;
}

.form-item {
  margin-bottom: $space-xl;
}

.label {
  font-size: 28rpx;
  font-weight: bold;
  color: $fg;
  margin-bottom: $space-sm;
  display: block;
}

.input {
  background: $bg;
  border-radius: $radius-md;
  padding: $space-md;
  font-size: 30rpx;
  border: 2rpx solid $border;
}

.grade-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $space-md;
}

.grade-item {
  background: $bg;
  border: 2rpx solid $border;
  border-radius: $radius-md;
  padding: $space-lg;
  text-align: center;
  transition: all $transition-fast;

  &.active {
    background: $primary;
    border-color: $primary;
  }
}

.grade-text {
  font-size: 28rpx;
  color: $fg-secondary;

  .grade-item.active & {
    color: $fg-inverse;
    font-weight: bold;
  }
}

.btn-register {
  background: $primary;
  color: $fg-inverse;
  border-radius: $radius-pill;
  padding: $space-lg $space-2xl;
  font-size: 32rpx;
  font-weight: bold;
  border: none;
  margin-top: $space-xl;

  &.disabled {
    background: $fg-tertiary;
    opacity: 0.6;
  }
}
</style>
