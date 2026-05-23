import { defineStore } from 'pinia'

export const useLearnStore = defineStore('learn', {
  state: () => ({
    currentSceneId: null as number | null,
    currentSubSceneId: null as number | null,
    currentWordIndex: 0,
    currentDimension: 1 as number,
    currentWordId: null as number | null,
    sessionWords: [] as number[],
    sessionStartTime: 0,
    sessionScores: {} as Record<number, Record<string, number>>,
    isPaused: false,
    totalWords: 0,
  }),
  getters: {
    dimensions: () => ['form', 'meaning', 'sound', 'memory', 'usage'],
    progressPercent: (state) => {
      if (state.totalWords === 0) return 0
      return Math.round((state.currentWordIndex / state.totalWords) * 100)
    },
  },
  actions: {
    startSession(sceneId: number, subSceneId: number, totalWords: number) {
      this.currentSceneId = sceneId
      this.currentSubSceneId = subSceneId
      this.currentWordIndex = 0
      this.currentDimension = 1
      this.sessionWords = []
      this.sessionStartTime = Date.now()
      this.sessionScores = {}
      this.isPaused = false
      this.totalWords = totalWords
    },
    nextDimension() {
      if (this.currentDimension < 5) {
        this.currentDimension++
      }
    },
    prevDimension() {
      if (this.currentDimension > 1) {
        this.currentDimension--
      }
    },
    nextWord() {
      this.currentWordIndex++
      this.currentDimension = 1
      if (this.currentWordId) {
        this.sessionWords.push(this.currentWordId)
      }
    },
    completeSession() {
      this.currentSceneId = null
      this.currentSubSceneId = null
      this.currentWordIndex = 0
      this.currentDimension = 1
      this.currentWordId = null
      this.sessionWords = []
      this.sessionStartTime = 0
      this.sessionScores = {}
      this.totalWords = 0
    },
  },
})
