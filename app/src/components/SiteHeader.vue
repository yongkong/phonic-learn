<template>
  <view class="site-header">
    <view class="inner">
      <view class="brand" @click="go('/pages/home/index')">
        <view class="brand-mark">
          <text>W</text>
        </view>
        <text class="brand-name">Word<text class="hl">World</text></text>
      </view>

      <view class="site-nav">
        <view
          v-for="item in items"
          :key="item.url"
          class="nav-item"
          :class="{ active: item.url === active }"
          @click="go(item.url)"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path v-for="(d, i) in item.icon" :key="i" :d="d" />
          </svg>
          <text>{{ item.label }}</text>
        </view>
      </view>

      <view class="header-right">
        <view class="meta-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
            <path d="M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z" />
          </svg>
          <text>{{ userStore.nickname || '小学者' }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'

// 图标与 scripts/gen-tab-icons.mjs 同源（Lucide 线性，MASTER v2）
defineProps<{ active: string }>()

const userStore = useUserStore()

const items = [
  {
    url: '/pages/home/index',
    label: '学习',
    icon: [
      'M12 7v14',
      'M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-5a4 4 0 0 0-4 4 4 4 0 0 0-4-4z',
    ],
  },
  {
    url: '/pages/practice/index',
    label: '练习',
    icon: ['M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z', 'm15 5 4 4'],
  },
  {
    url: '/pages/essay/index',
    label: '作文',
    icon: [
      'M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z',
      'M14 2v4a2 2 0 0 0 2 2h4',
      'M10 9H8',
      'M16 13H8',
      'M16 17H8',
    ],
  },
  {
    url: '/pages/profile/index',
    label: '我的',
    icon: ['M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2', 'M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z'],
  },
]

function go(url: string) {
  uni.switchTab({ url })
}
</script>

<style lang="scss" scoped>
// 桌面顶栏：仅 ≥1024px 显示（移动端仍用原生 tabBar）
.site-header {
  display: none;
}

@media (min-width: 1024px) {
  .site-header {
    display: block;
    background: $surface;
    border-bottom: 2rpx solid $border;
    position: sticky;
    top: 0;
    z-index: 100;
    margin: -40rpx -40rpx 32rpx; /* 抵消页面内边距，通栏到边 */

    .inner {
      max-width: 1080px;
      margin: 0 auto;
      padding: 0 24px;
      height: 64px;
      display: flex;
      align-items: center;
    }
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
  }

  .brand-mark {
    width: 36px;
    height: 36px;
    border-radius: 11px;
    background: linear-gradient(135deg, $primary-light, $primary-dark);
    color: $fg-inverse;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: $font-display;
    font-size: 20px;
    font-weight: 800;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);
  }

  .brand-name {
    font-family: $font-display;
    font-size: 18px;
    font-weight: 800;
    color: $fg;

    .hl {
      color: $accent;
    }
  }

  .site-nav {
    display: flex;
    gap: 6px;
    margin-left: 24px;
  }

  .nav-item {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 9px 18px;
    border-radius: $radius-pill;
    font-size: 15px;
    font-weight: 800;
    color: $fg-secondary;
    cursor: pointer;
    min-height: 44px;
    box-sizing: border-box;
    transition: background $transition-fast, color $transition-fast;

    svg {
      width: 17px;
      height: 17px;
    }

    &:hover {
      background: $primary-soft;
      color: $primary;
    }

    &.active {
      background: $primary;
      color: $fg-inverse;
      box-shadow: 0 2px 0 $primary-dark;
    }
  }

  .header-right {
    margin-left: auto;
    display: flex;
    align-items: center;
  }

  .meta-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    border-radius: $radius-pill;
    background: $bg;
    border: 2rpx solid $border;
    font-family: $font-display;
    font-size: 14px;
    font-weight: 800;
    color: $fg-secondary;

    svg {
      width: 16px;
      height: 16px;
      color: $primary;
    }
  }
}
</style>
