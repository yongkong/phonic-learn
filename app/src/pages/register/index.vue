<template>
  <view class="register-page">
    <view class="reg-body">
      <view class="header">
        <text class="title">你好，准备好开始<text class="hl">单词冒险</text>了吗？</text>
        <text class="subtitle">先给自己起个名字吧</text>
      </view>

      <view class="form">
        <!-- Nickname Input -->
        <view class="form-item">
          <text class="label">你的昵称</text>
          <view class="input-wrap">
            <input
              class="input"
              v-model="nickname"
              placeholder="请输入昵称"
              placeholder-class="input-placeholder"
              maxlength="20"
            />
            <text class="count">{{ nickname.length }}/20</text>
          </view>
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
              <text class="grade-num">{{ grade }}</text>
              <text class="grade-text">年级</text>
              <view v-if="selectedGrade === grade" class="check">
                <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- Bottom CTA -->
    <view class="cta-bar">
      <button
        class="btn-register"
        :class="{ disabled: !canRegister }"
        :disabled="!canRegister"
        @click="handleRegister"
      >
        {{ submitting ? '正在创建账号…' : '开始学习之旅' }}
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { registerUser } from '@/api/user'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const nickname = ref('')
const selectedGrade = ref(0)
const submitting = ref(false)

const canRegister = computed(() => {
  return nickname.value.trim().length > 0 && selectedGrade.value > 0 && !submitting.value
})

const handleRegister = async () => {
  if (!canRegister.value) return
  submitting.value = true
  try {
    const user = await registerUser({
      nickname: nickname.value.trim(),
      grade: selectedGrade.value,
    })
    userStore.setUser(user)
    uni.switchTab({ url: '/pages/home/index' })
  } catch {
    // 请求层已统一 toast 具体错误（如昵称重复 409），这里不再重复提示
  } finally {
    submitting.value = false
  }
}
</script>

<style lang="scss" scoped>
.register-page {
  min-height: 100vh;
  background: $bg;
  display: flex;
  flex-direction: column;
}

.reg-body {
  flex: 1;
  padding: $space-2xl $space-xl 0;
}

.header {
  margin-bottom: $space-3xl;
}

.title {
  font-family: $font-display;
  font-size: 52rpx;
  font-weight: 800;
  line-height: 1.3;
  color: $fg;
  display: block;
}

.hl {
  color: $primary;
}

.subtitle {
  font-size: 28rpx;
  font-weight: 600;
  color: $fg-secondary;
  margin-top: $space-sm;
  display: block;
}

.form-item {
  margin-bottom: $space-2xl;
}

.label {
  font-size: 26rpx;
  font-weight: 800;
  color: $fg;
  margin-bottom: $space-md;
  display: block;
}

.input-wrap {
  position: relative;
}

.input {
  background: $surface;
  border-radius: $radius-md;
  padding: 28rpx 140rpx 28rpx $space-lg;
  font-size: 30rpx;
  font-weight: 600;
  color: $fg;
  border: 4rpx solid $border-strong;
  min-height: 88rpx;
  box-sizing: border-box;
  width: 100%;
}

.input-placeholder {
  color: $fg-tertiary;
}

.count {
  position: absolute;
  right: $space-lg;
  top: 50%;
  transform: translateY(-50%);
  font-size: 22rpx;
  font-weight: 700;
  color: $fg-tertiary;
  background: $surface-alt;
  padding: 4rpx 16rpx;
  border-radius: $radius-pill;
}

.grade-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $space-md;
}

.grade-item {
  position: relative;
  background: $surface;
  border: 4rpx solid $border-strong;
  border-radius: $radius-md;
  padding: $space-md $space-sm;
  min-height: 88rpx;
  box-sizing: border-box;
  text-align: center;
  transition: all $transition-fast;

  &:active {
    transform: scale(0.95);
  }

  &.active {
    border-color: $primary;
    background: $primary-soft;
  }
}

.grade-num {
  font-family: $font-display;
  font-size: 44rpx;
  font-weight: 800;
  color: $fg;
  line-height: 1.1;
  display: block;
}

.grade-text {
  font-size: 24rpx;
  font-weight: 700;
  color: $fg-secondary;
  margin-top: 4rpx;
  display: block;
}

.grade-item.active {
  .grade-num {
    color: $primary;
  }
}

.check {
  position: absolute;
  top: -16rpx;
  right: -16rpx;
  width: 44rpx;
  height: 44rpx;
  border-radius: $radius-circle;
  background: $primary;
  border: 4rpx solid #fff;
  display: flex;
  align-items: center;
  justify-content: center;

  svg {
    width: 22rpx;
    height: 22rpx;
  }
}

.cta-bar {
  position: sticky;
  bottom: 0;
  padding: $space-md $space-xl;
  padding-bottom: calc(64rpx + env(safe-area-inset-bottom));
  background: linear-gradient(180deg, rgba(238, 242, 255, 0) 0%, $bg 40%);
}

.btn-register {
  background: $primary;
  color: $fg-inverse;
  border-radius: $radius-pill;
  font-size: 32rpx;
  font-weight: 800;
  border: none;
  min-height: 96rpx;
  line-height: 96rpx;
  @include press-feedback;

  &.disabled {
    background: $fg-tertiary;
    box-shadow: none;
  }
}

/* ===== 桌面端（≥1024px）：居中表单 ===== */
@media (min-width: 1024px) {
  .register-page {
    max-width: 560px;
    margin: 0 auto;
  }
}
</style>
