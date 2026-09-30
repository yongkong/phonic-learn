<template>
  <view class="home-page">
    <!-- User Greeting -->
    <view class="greeting">
      <text class="greeting-text">你好, <text class="nickname">{{ userStore.nickname }}</text></text>
      <text class="progress-text">已学会 {{ totals.learned }} / {{ totals.total }} 个单词</text>
    </view>

    <!-- Scene Map -->
    <view class="scene-map">
      <view class="map-header">
        <text class="map-title">学习地图</text>
        <text class="map-sub">{{ scenes.length }} 个场景</text>
      </view>

      <!-- Loading -->
      <view v-if="loading" class="map-status">
        <view class="loading-dots">
          <view class="dot dot-1"></view>
          <view class="dot dot-2"></view>
          <view class="dot dot-3"></view>
        </view>
      </view>

      <!-- Error -->
      <view v-else-if="loadError" class="map-status">
        <text class="status-text">加载失败了，请检查网络</text>
        <button class="btn-retry" @click="loadScenes">重试</button>
      </view>

      <!-- Scene Nodes -->
      <view v-else class="map-path">
        <view
          v-for="scene in scenes"
          :key="scene.id"
          class="scene-node"
          :class="sceneState(scene)"
          @click="openScene(scene)"
        >
          <view class="node-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path v-for="(d, i) in iconPaths(scene)" :key="i" :d="d" />
            </svg>
            <view v-if="sceneState(scene) !== 'fresh'" class="node-badge" :class="{ star: sceneState(scene) === 'done' }">
              <text>{{ sceneLearned(scene) }}/{{ sceneTotal(scene) }}</text>
            </view>
          </view>
          <view class="node-body">
            <view class="node-title">
              <text>{{ scene.name }}</text>
              <text v-if="sceneState(scene) === 'current'" class="tag">进行中</text>
            </view>
            <text class="node-desc">
              {{ sceneState(scene) === 'done' ? '全部掌握' : sceneState(scene) === 'current' ? `已学 ${sceneLearned(scene)} / ${sceneTotal(scene)}` : `共 ${sceneTotal(scene)} 个单词` }}
            </text>
            <view v-if="scene.progress > 0" class="node-progress">
              <view class="progress-bar">
                <view class="progress-fill" :style="{ width: progressPercent(scene) + '%' }"></view>
              </view>
              <text class="p-text">{{ progressPercent(scene) }}%</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- Overall Progress -->
    <view class="progress-section">
      <text class="section-title">学习进度</text>
      <view class="progress-bar big">
        <view class="progress-fill" :style="{ width: totals.percent + '%' }"></view>
      </view>
      <view class="progress-meta">
        <text class="progress-label">{{ totals.percent }}%</text>
        <text class="progress-label">{{ totals.total > 0 ? `${totals.learned}/${totals.total} 词` : '暂无单词' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getScenes } from '@/api/scene'
import { useUserStore } from '@/stores/user'
import type { Scene } from '@/types'

const userStore = useUserStore()
const scenes = ref<Scene[]>([])
const loading = ref(true)
const loadError = ref(false)

async function loadScenes() {
  loading.value = true
  loadError.value = false
  try {
    scenes.value = await getScenes()
  } catch {
    loadError.value = true
  } finally {
    loading.value = false
  }
}

onShow(() => {
  loadScenes()
})

const totals = computed(() => {
  let learned = 0
  let total = 0
  for (const scene of scenes.value) {
    learned += sceneLearned(scene)
    total += sceneTotal(scene)
  }
  return { learned, total, percent: total > 0 ? Math.round((learned / total) * 100) : 0 }
})

function sceneLearned(scene: Scene): number {
  return scene.sub_scenes.reduce((sum, sub) => sum + sub.learned_count, 0)
}

function sceneTotal(scene: Scene): number {
  return scene.sub_scenes.reduce((sum, sub) => sum + sub.word_count, 0)
}

type SceneState = 'done' | 'current' | 'fresh'

function sceneState(scene: Scene): SceneState {
  if (scene.progress >= 1) return 'done'
  if (scene.progress > 0) return 'current'
  return 'fresh'
}

function progressPercent(scene: Scene): number {
  return Math.round((scene.progress || 0) * 100)
}

function openScene(scene: Scene) {
  uni.navigateTo({ url: `/pages/scene/index?id=${scene.id}` })
}

// 线性 SVG 图标（Lucide 风格路径，按场景名映射；MASTER v2 禁止 emoji 当图标）
const SCENE_ICONS: Record<string, string[]> = {
  我的家: ['M3 10l9-7 9 7v10a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z'],
  我的学校: [
    'M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z',
    'M22 10v6',
    'M6 12.5V16a6 3 0 0 0 12 0v-3.5',
  ],
  超市购物: [
    'M7.4 21a1.6 1.6 0 1 0 3.2 0a1.6 1.6 0 1 0 -3.2 0',
    'M17.4 21a1.6 1.6 0 1 0 3.2 0a1.6 1.6 0 1 0 -3.2 0',
    'M2 3h3l2.6 12.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 7H6',
  ],
}

const FALLBACK_ICON = [
  'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z',
  'M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z',
]

function iconPaths(scene: Scene): string[] {
  return SCENE_ICONS[scene.name] || FALLBACK_ICON
}
</script>

<style lang="scss" scoped>
.home-page {
  padding: $space-xl;
  background: $bg;
  min-height: 100vh;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
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
  font-weight: 600;
  color: $fg-secondary;
  margin-top: $space-xs;
  display: block;
}

.scene-map {
  background: $surface;
  border: 2rpx solid $border;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  padding: $space-xl;
  margin-bottom: $space-xl;
}

.map-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: $space-xl;
}

.map-title {
  font-family: $font-display;
  font-size: 34rpx;
  font-weight: 800;
  color: $fg;
}

.map-sub {
  font-size: 24rpx;
  font-weight: 600;
  color: $fg-tertiary;
}

.map-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 360rpx;
  gap: $space-lg;
}

.status-text {
  font-size: 28rpx;
  font-weight: 600;
  color: $fg-secondary;
}

.btn-retry {
  background: $primary;
  color: $fg-inverse;
  font-size: 28rpx;
  font-weight: 800;
  border-radius: $radius-pill;
  border: none;
  min-height: 88rpx;
  min-width: 240rpx;
  line-height: 88rpx;
  box-shadow: $edge-primary-sm;

  &::after {
    border: none;
  }

  &:active {
    transform: translateY(4rpx);
    box-shadow: none;
  }
}

.map-path {
  position: relative;
  padding-left: $space-sm;

  // 节点之间的虚线路径
  &::before {
    content: '';
    position: absolute;
    left: 103rpx;
    top: 56rpx;
    bottom: 56rpx;
    border-left: 6rpx dashed $border-strong;
    z-index: 0;
  }
}

.scene-node {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: $space-md;
  margin-bottom: $space-lg;

  &:last-child {
    margin-bottom: 0;
  }
}

.node-icon {
  width: 144rpx;
  height: 144rpx;
  border-radius: $radius-lg;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 4rpx solid #fff;
  box-shadow: $shadow-md;
  position: relative;
  transition: transform $transition-normal;
  background: $primary-soft;
  color: $primary;

  svg {
    width: 60rpx;
    height: 60rpx;
  }
}

.scene-node:active .node-icon {
  transform: scale(0.94);
}

.scene-node.done .node-icon {
  background: $success;
  color: $fg-inverse;
}

.scene-node.current .node-icon {
  background: $accent;
  color: $fg-inverse;
}

.node-badge {
  position: absolute;
  bottom: -12rpx;
  right: -12rpx;
  min-width: 48rpx;
  height: 48rpx;
  padding: 0 12rpx;
  border-radius: $radius-pill;
  background: $surface;
  border: 4rpx solid $border;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  font-weight: 800;
  color: $fg-secondary;
  box-sizing: border-box;

  &.star {
    color: $accent-dark;
    border-color: #ffdfc2;
  }
}

.node-body {
  flex: 1;
  min-width: 0;
  background: $surface;
  border-radius: $radius-md;
  border: 2rpx solid $border;
  box-shadow: $shadow-sm;
  padding: $space-md $space-lg;
}

.node-title {
  font-size: 30rpx;
  font-weight: 800;
  color: $fg;
  display: flex;
  align-items: center;
  gap: $space-sm;
}

.node-title .tag {
  font-size: 20rpx;
  font-weight: 800;
  padding: 4rpx 16rpx;
  border-radius: $radius-pill;
  background: $accent;
  color: $fg-inverse;
  letter-spacing: 1rpx;
  flex-shrink: 0;
}

.node-desc {
  font-size: 24rpx;
  font-weight: 600;
  color: $fg-secondary;
  margin-top: 4rpx;
  display: block;
}

.node-progress {
  display: flex;
  align-items: center;
  gap: $space-sm;
  margin-top: $space-md;
}

.progress-bar {
  flex: 1;
  height: 16rpx;
  background: $border-light;
  border-radius: $radius-pill;
  overflow: hidden;

  &.big {
    height: 20rpx;
  }
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, $primary-light, $primary);
  border-radius: $radius-pill;
  transition: width $transition-slow;
}

.p-text {
  font-size: 22rpx;
  font-weight: 800;
  color: $fg-secondary;
  min-width: 64rpx;
  text-align: right;
}

.progress-section {
  background: $surface;
  border: 2rpx solid $border;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  padding: $space-xl;
}

.section-title {
  font-size: 30rpx;
  font-weight: 800;
  color: $fg;
  margin-bottom: $space-md;
  display: block;
}

.progress-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: $space-sm;
}

.progress-label {
  font-size: 24rpx;
  font-weight: 700;
  color: $fg-secondary;
}

.loading-dots {
  display: flex;
  gap: $space-sm;
}

.dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: $radius-circle;
  background: $primary-light;
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
