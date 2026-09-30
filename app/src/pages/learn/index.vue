<template>
  <view class="learn-page">
    <!-- Error / Loading -->
    <view v-if="loadState === 'loading'" class="learn-status">
      <view class="loading-dots">
        <view class="dot dot-1"></view>
        <view class="dot dot-2"></view>
        <view class="dot dot-3"></view>
      </view>
    </view>
    <view v-else-if="loadState === 'error'" class="learn-status">
      <text class="status-text">{{ wordId ? '加载失败了，请检查网络' : '缺少单词参数，请从词表进入' }}</text>
      <button class="btn-back" @click="handleBackOrRetry">{{ wordId ? '重试' : '返回词表' }}</button>
    </view>

    <template v-else>
      <!-- Word Header -->
      <view class="word-header">
        <view class="word-main">
          <text class="word-spelling">{{ word?.spelling }}</text>
          <text v-if="word?.phonetic_us" class="word-phonetic">{{ word.phonetic_us }}</text>
        </view>
        <button class="btn-audio" :class="{ playing: playingWord }" @click="playWord" aria-label="播放单词发音">
          <AudioIcon :filled="playingWord" :wave="2" class="audio-icon" />
        </button>
      </view>

      <!-- Dimension Steps -->
      <view class="dimension-steps">
        <view
          v-for="(dim, i) in DIMENSIONS"
          :key="dim.key"
          class="step"
          :class="{ active: i + 1 === currentDimension, completed: i + 1 < currentDimension }"
          @click="jumpDimension(i + 1)"
        >
          <text class="step-index">{{ i + 1 }}</text>
          <text class="step-label">{{ dim.label }}</text>
        </view>
      </view>

      <!-- Dimension Content -->
      <view class="dimension-content">
        <!-- 认形：自然拼读着色（元音红 / 辅音蓝 / 静音灰，语义色不随风格更改） -->
        <view v-if="currentDimension === 1" class="panel">
          <view class="letter-row">
            <view
              v-for="(seg, i) in letterSegments"
              :key="i"
              class="letter-block"
              :style="{ color: seg.color }"
            >
              <text class="letter-char">{{ seg.letter }}</text>
              <text class="letter-sound">{{ seg.sound }}</text>
            </view>
          </view>
          <view class="legend">
            <text class="legend-item"><text class="dot-mark vowel" />元音</text>
            <text class="legend-item"><text class="dot-mark consonant" />辅音</text>
            <text class="legend-item"><text class="dot-mark silent" />静音</text>
          </view>
        </view>

        <!-- 识义：情景词义与配图 -->
        <view v-else-if="currentDimension === 2" class="panel">
          <view v-if="word?.emoji" class="meaning-illustration">
            <text class="illustration">{{ word.emoji }}</text>
          </view>
          <view class="meaning-list">
            <view v-for="(m, i) in word?.meanings || []" :key="i" class="meaning-item">
              <text class="meaning-pos">{{ m.pos }}</text>
              <text class="meaning-cn">{{ m.cn }}</text>
            </view>
          </view>
        </view>

        <!-- 拼读：音节拆分 -->
        <view v-else-if="currentDimension === 3" class="panel">
          <view class="syllable-row">
            <template v-for="(syl, i) in word?.phonic_analysis?.syllables || []" :key="i">
              <view v-if="i > 0" class="syllable-sep">·</view>
              <view class="syllable-chip">{{ syl }}</view>
            </template>
          </view>
          <view class="syllable-phonetics">
            <text v-for="(p, i) in word?.phonic_analysis?.syllable_phonetics || []" :key="i" class="phonetic-chip">{{ p }}</text>
          </view>
          <button class="btn-listen-repeat" @click="playWord">
            <AudioIcon :wave="1" class="listen-icon" />
            <text>听一听，跟着读</text>
          </button>
        </view>

        <!-- 巧记：联想助记 -->
        <view v-else-if="currentDimension === 4" class="panel">
          <view v-for="(tip, i) in word?.memory_tips || []" :key="i" class="tip-card">
            <text class="tip-type">{{ tipTypeLabel(tip.type) }}</text>
            <text class="tip-content">{{ tip.content }}</text>
          </view>
          <view v-if="!(word?.memory_tips || []).length" class="empty-hint">
            <text>这个词还没有助记提示</text>
          </view>
        </view>

        <!-- 运用：情景例句 -->
        <view v-else class="panel">
          <view v-for="(sent, i) in word?.example_sentences || []" :key="i" class="sentence-card">
            <view class="sentence-body">
              <text class="sentence-en">{{ sent.en }}</text>
              <text class="sentence-cn">{{ sent.cn }}</text>
            </view>
            <button
              v-if="sent.audio_filename"
              class="btn-sentence-audio"
              :class="{ playing: playingSentence === sent.audio_filename }"
              @click="playSentence(sent.audio_filename)"
              :aria-label="`播放例句 ${i + 1}`"
            >
              <AudioIcon :filled="playingSentence === sent.audio_filename" :wave="1" class="sentence-audio-icon" />
            </button>
          </view>
        </view>
      </view>

      <!-- Dimension Nav -->
      <view class="dimension-nav">
        <button class="btn-prev" :disabled="currentDimension <= 1" @click="prevDimension">上一维</button>
        <button class="btn-next" @click="nextDimension">
          {{ currentDimension < 5 ? '下一维' : '完成学习' }}
        </button>
      </view>
    </template>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { onLoad, onUnload } from '@dcloudio/uni-app'
import { getWordDetail } from '@/api/scene'
import { DIMENSIONS } from '@/utils/dimensions'
import { playWordAudio, playSentenceAudio } from '@/utils/audio'
import { useLearnStore } from '@/stores/learn'
import { stopAudio } from '@/utils/audio'
import AudioIcon from '@/components/AudioIcon.vue'
import { PHONIC_COLORS } from '@/utils/phonics-colors'
import type { WordDetail } from '@/types'

const learnStore = useLearnStore()
const word = ref<WordDetail | null>(null)
const loadState = ref<'loading' | 'ready' | 'error'>('loading')
const wordId = ref(0)
const playingWord = ref(false)
const playingSentence = ref('')
// 维度状态以 learn store 为单源（工单6 会话流转在其上扩展）
const { currentDimension } = storeToRefs(learnStore)

onUnload(() => {
  stopAudio()
})

onLoad((options) => {
  wordId.value = Number(options?.wordId || 0)
  learnStore.currentSceneId = Number(options?.sceneId || 0) || null
  learnStore.currentSubSceneId = Number(options?.subSceneId || 0) || null
  learnStore.currentWordId = wordId.value || null
  loadWord()
})

async function loadWord() {
  if (!wordId.value) {
    loadState.value = 'error'
    return
  }
  loadState.value = 'loading'
  try {
    word.value = await getWordDetail(wordId.value)
    loadState.value = 'ready'
  } catch {
    loadState.value = 'error'
  }
}

// 形维字母着色：letter_sounds 的 color 是教学语义（红/蓝/灰/紫），不随风格更改
const letterSegments = computed(() =>
  (word.value?.phonic_analysis?.letter_sounds || []).map((seg) => ({
    letter: seg.letter,
    sound: seg.sound,
    color: PHONIC_COLORS[seg.color] || '#1E1B4B',
  }))
)

const TIP_TYPE_LABELS: Record<string, string> = {
  image: '形象联想',
  homophone: '谐音',
  story: '小故事',
  association: '联想',
}

function tipTypeLabel(type: string): string {
  return TIP_TYPE_LABELS[type] || '巧记'
}

async function playWord() {
  const filename = word.value?.audio_filename
  if (!filename || playingWord.value) return
  playingWord.value = true
  try {
    await playWordAudio(filename)
  } catch {
    uni.showToast({ title: '音频播放失败', icon: 'none' })
  } finally {
    // 被新播放取消时不清除新播放的态
    if (playingWord.value) playingWord.value = false
  }
}

async function playSentence(filename: string) {
  if (playingSentence.value === filename) return
  playingSentence.value = filename
  try {
    await playSentenceAudio(filename)
  } catch {
    uni.showToast({ title: '音频播放失败', icon: 'none' })
  } finally {
    // 仅当仍是自己时清理，避免清掉新播放的态
    if (playingSentence.value === filename) playingSentence.value = ''
  }
}

function jumpDimension(index: number) {
  learnStore.currentDimension = index
}

function prevDimension() {
  learnStore.prevDimension()
}

function nextDimension() {
  if (learnStore.currentDimension < 5) {
    learnStore.nextDimension()
  } else {
    // 完词流转与自动下一词属工单6（学习会话生命周期）
    handleBackOrRetry()
  }
}

function handleBackOrRetry() {
  if (!wordId.value) {
    uni.navigateBack()
  } else {
    loadWord()
  }
}
</script>

<style lang="scss" scoped>
.learn-page {
  padding: $space-xl;
  background: $bg;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.learn-status {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: $space-lg;
  min-height: 500rpx;
}

.status-text {
  font-size: 28rpx;
  font-weight: 600;
  color: $fg-secondary;
}

.btn-back {
  background: $primary;
  color: $fg-inverse;
  font-size: 28rpx;
  font-weight: 800;
  border-radius: $radius-pill;
  border: none;
  min-height: 88rpx;
  min-width: 240rpx;
  line-height: 88rpx;
  @include press-feedback($edge-primary-sm, none);
}

/* Word Header */
.word-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: $surface;
  border: 2rpx solid $border;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  padding: $space-lg $space-xl;
}

.word-spelling {
  font-family: $font-display;
  font-size: 64rpx;
  font-weight: 800;
  color: $fg;
  line-height: 1.1;
  display: block;
}

.word-phonetic {
  font-size: 26rpx;
  font-weight: 600;
  color: $fg-tertiary;
  margin-top: 4rpx;
  display: block;
}

.btn-audio {
  width: 96rpx;
  height: 96rpx;
  border-radius: $radius-circle;
  background: $primary;
  color: $fg-inverse;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: none;
  flex-shrink: 0;
  margin-left: $space-md;
  @include press-feedback($edge-primary-sm, none);

  .audio-icon {
    width: 48rpx;
    height: 48rpx;
  }

  &.playing {
    background: $primary-dark;
  }
}

/* Dimension Steps */
.dimension-steps {
  display: flex;
  gap: $space-sm;
  margin: $space-lg 0;
}

.step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
  padding: $space-sm 0;
  border-radius: $radius-md;
  background: $surface;
  border: 2rpx solid $border;
  min-height: 88rpx;
  justify-content: center;
  transition: all $transition-fast;

  &.active {
    background: $primary;
    border-color: $primary;

    .step-index,
    .step-label {
      color: $fg-inverse;
    }
  }

  &.completed {
    border-color: $primary;
    background: $primary-soft;

    .step-index {
      color: $primary;
    }
  }
}

.step-index {
  font-family: $font-display;
  font-size: 24rpx;
  font-weight: 800;
  color: $fg-secondary;
  line-height: 1;
}

.step-label {
  font-size: 24rpx;
  font-weight: 800;
  color: $fg-secondary;
  line-height: 1.2;
}

/* Dimension Content */
.dimension-content {
  flex: 1;
}

.panel {
  background: $surface;
  border: 2rpx solid $border;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  padding: $space-xl;
}

/* 认形 */
.letter-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: $space-md;
}

.letter-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  min-width: 88rpx;
  padding: $space-md $space-sm;
  background: $bg;
  border-radius: $radius-md;
  border: 2rpx solid $border-light;
}

.letter-char {
  font-family: $font-display;
  font-size: 72rpx;
  font-weight: 800;
  line-height: 1.1;
}

.letter-sound {
  font-size: 22rpx;
  font-weight: 700;
  color: $fg-secondary;
}

.legend {
  display: flex;
  justify-content: center;
  gap: $space-lg;
  margin-top: $space-lg;
}

.legend-item {
  font-size: 24rpx;
  font-weight: 600;
  color: $fg-secondary;
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.dot-mark {
  width: 20rpx;
  height: 20rpx;
  border-radius: $radius-circle;
  display: inline-block;

  &.vowel { background: $vowel; }
  &.consonant { background: $consonant; }
  &.silent { background: $silent; }
}

/* 识义 */
.meaning-illustration {
  display: flex;
  justify-content: center;
  margin-bottom: $space-lg;
}

.illustration {
  font-size: 140rpx;
  line-height: 1.2;
}

.meaning-list {
  display: flex;
  flex-direction: column;
  gap: $space-md;
}

.meaning-item {
  display: flex;
  align-items: baseline;
  gap: $space-md;
  background: $bg;
  border-radius: $radius-md;
  padding: $space-md $space-lg;
}

.meaning-pos {
  font-size: 24rpx;
  font-weight: 800;
  color: $primary;
  flex-shrink: 0;
}

.meaning-cn {
  font-size: 30rpx;
  font-weight: 700;
  color: $fg;
}

/* 拼读 */
.syllable-row {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: $space-sm;
}

.syllable-sep {
  font-size: 48rpx;
  font-weight: 800;
  color: $syllable-sep;
  line-height: 1;
}

.syllable-chip {
  font-family: $font-display;
  font-size: 64rpx;
  font-weight: 800;
  color: $fg;
  background: $bg;
  border: 2rpx solid $border;
  border-radius: $radius-md;
  padding: $space-md $space-xl;
}

.syllable-phonetics {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: $space-sm;
  margin-top: $space-lg;
}

.phonetic-chip {
  font-size: 26rpx;
  font-weight: 700;
  color: $fg-secondary;
  background: $bg;
  border-radius: $radius-pill;
  padding: 8rpx $space-lg;
}

.btn-listen-repeat {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $space-sm;
  margin-top: $space-xl;
  background: $accent;
  color: $fg-inverse;
  border-radius: $radius-pill;
  border: none;
  min-height: 88rpx;
  font-size: 28rpx;
  font-weight: 800;
  @include press-feedback($edge-accent-sm, none);

  .listen-icon {
    width: 36rpx;
    height: 36rpx;
  }
}

/* 巧记 */
.tip-card {
  display: flex;
  flex-direction: column;
  gap: $space-xs;
  background: $bg;
  border-radius: $radius-md;
  padding: $space-md $space-lg;
  margin-bottom: $space-md;

  &:last-child {
    margin-bottom: 0;
  }
}

.tip-type {
  font-size: 22rpx;
  font-weight: 800;
  color: $accent-dark;
  background: $accent-soft;
  border-radius: $radius-pill;
  padding: 4rpx $space-md;
  align-self: flex-start;
}

.tip-content {
  font-size: 28rpx;
  font-weight: 600;
  color: $fg;
  line-height: 1.6;
}

.empty-hint {
  text-align: center;
  padding: $space-xl 0;

  text {
    font-size: 26rpx;
    color: $fg-tertiary;
  }
}

/* 运用 */
.sentence-card {
  display: flex;
  align-items: center;
  gap: $space-md;
  background: $bg;
  border-radius: $radius-md;
  padding: $space-md $space-lg;
  margin-bottom: $space-md;
  min-height: 120rpx;

  &:last-child {
    margin-bottom: 0;
  }
}

.sentence-body {
  flex: 1;
  min-width: 0;
}

.sentence-en {
  font-size: 30rpx;
  font-weight: 700;
  color: $fg;
  line-height: 1.5;
  display: block;
}

.sentence-cn {
  font-size: 24rpx;
  font-weight: 600;
  color: $fg-secondary;
  margin-top: 4rpx;
  display: block;
}

.btn-sentence-audio {
  width: 88rpx;
  height: 88rpx;
  border-radius: $radius-circle;
  background: $surface;
  border: 2rpx solid $border-strong;
  color: $primary;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  flex-shrink: 0;
  @include press-feedback($edge-primary-sm, none);

  .sentence-audio-icon {
    width: 40rpx;
    height: 40rpx;
  }

  &.playing {
    background: $primary;
    color: $fg-inverse;
    border-color: $primary;
  }
}

/* Nav */
.dimension-nav {
  display: flex;
  gap: $space-md;
  margin-top: $space-lg;
  padding-bottom: calc($space-lg + env(safe-area-inset-bottom));
}

.dimension-nav button {
  flex: 1;
  min-height: 96rpx;
  line-height: 96rpx;
  border-radius: $radius-pill;
  font-size: 30rpx;
  font-weight: 800;
  border: none;
}

.btn-prev {
  background: $surface;
  color: $fg;
  border: 2rpx solid $border-strong;

  &[disabled] {
    color: $fg-tertiary;
    background: $surface-alt;
  }
}

.btn-next {
  background: $primary;
  color: $fg-inverse;
  @include press-feedback;
}

/* Loading dots */
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

@media (prefers-reduced-motion: reduce) {
  .dot {
    animation: none;
    opacity: 0.8;
  }
}
</style>
