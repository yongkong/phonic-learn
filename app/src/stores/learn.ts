import { defineStore } from 'pinia'
import {
  startSession,
  completeDimension,
  completeWord,
  endSession,
} from '@/api/learning'
import { DIMENSIONS } from '@/utils/dimensions'

/** advance() 的结果：moved=进入下一词，done=本子场景全部学完 */
export type AdvanceResult = 'moved' | 'done'

export const useLearnStore = defineStore('learn', {
  state: () => ({
    /** 当前学习会话（后端 LearningSession id），null 表示未开会话 */
    sessionId: null as number | null,
    sessionEnded: false,
    sessionStartTs: 0,
    sceneId: null as number | null,
    subSceneId: null as number | null,
    /** 子场景内的有序词 id 列表与当前位置 */
    wordIds: [] as number[],
    wordIndex: 0,
    /** 当前维度序号 1-5（形 → 义 → 音 → 记 → 用） */
    dimension: 1,
  }),
  getters: {
    currentWordId: (state): number | null => state.wordIds[state.wordIndex] ?? null,
    hasNextWord: (state): boolean => state.wordIndex < state.wordIds.length - 1,
  },
  actions: {
    /** 进入学习页：创建学习会话并定位起始词 */
    async beginSession(
      sceneId: number,
      subSceneId: number,
      wordIds: number[],
      startWordId: number
    ) {
      this.sceneId = sceneId
      this.subSceneId = subSceneId
      this.wordIds = wordIds
      const idx = wordIds.indexOf(startWordId)
      this.wordIndex = idx >= 0 ? idx : 0
      this.dimension = 1
      this.sessionEnded = false
      this.sessionStartTs = Date.now()
      const res = await startSession({
        sub_scene_id: subSceneId,
        session_type: 'scene_learning',
      })
      this.sessionId = res.session_id
    },

    /** 上报当前维度完成（静默失败不打断学习） */
    async reportDimension() {
      const dim = DIMENSIONS[this.dimension - 1]
      const wordId = this.currentWordId
      if (!dim || !wordId || !this.sessionId) return
      try {
        await completeDimension({ word_id: wordId, dimension: dim.key })
      } catch (e) {
        console.warn('上报维度完成失败', dim.key, e)
      }
    },

    /**
     * 前进一维：1-4 维上报后进入下一维；第 5 维上报后完词
     * （后端按简化 SM-2 记录下次复习时间）并自动进入下一词；
     * 全部学完返回 'done'。
     */
    async advance(): Promise<AdvanceResult> {
      if (this.dimension < DIMENSIONS.length) {
        await this.reportDimension()
        this.dimension++
        return 'moved'
      }
      await this.reportDimension() // usage
      const wordId = this.currentWordId
      if (wordId && this.sessionId) {
        try {
          await completeWord({ word_id: wordId, session_id: this.sessionId })
        } catch (e) {
          console.warn('完词上报失败', wordId, e)
        }
      }
      if (this.hasNextWord) {
        this.wordIndex++
        this.dimension = 1
        return 'moved'
      }
      return 'done'
    },

    /** 中途离开或全部学完：以请求体结束会话并上报时长（幂等） */
    async endLearning() {
      if (!this.sessionId || this.sessionEnded) return
      this.sessionEnded = true
      const duration = Math.max(0, Math.round((Date.now() - this.sessionStartTs) / 1000))
      try {
        await endSession(this.sessionId, duration)
      } catch (e) {
        console.warn('结束会话上报失败', e)
      } finally {
        this.sessionId = null
      }
    },

    prevDimension() {
      if (this.dimension > 1) this.dimension--
    },

    jumpDimension(index: number) {
      this.dimension = Math.min(Math.max(1, index), DIMENSIONS.length)
    },
  },
})
