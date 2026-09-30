import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'

const apiMock = vi.hoisted(() => ({
  startSession: vi.fn(),
  completeDimension: vi.fn(),
  completeWord: vi.fn(),
  endSession: vi.fn(),
}))
vi.mock('@/api/learning', () => apiMock)

import { useLearnStore } from '@/stores/learn'

function setup() {
  const pinia = createPinia()
  setActivePinia(pinia)
  apiMock.startSession.mockReset()
  apiMock.completeDimension.mockReset()
  apiMock.completeWord.mockReset()
  apiMock.endSession.mockReset()
  apiMock.startSession.mockResolvedValue({ session_id: 42, message: '' })
  apiMock.completeDimension.mockResolvedValue({})
  apiMock.completeWord.mockResolvedValue({
    word_id: 0,
    status: 'familiar',
    next_review_at: '2026-10-01T00:00:00',
  })
  apiMock.endSession.mockResolvedValue({})
  return useLearnStore()
}

const WORD_IDS = [11, 12, 13]

describe('learn store 会话生命周期', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-09-30T10:00:00Z'))
  })

  it('进入学习即创建会话并定位起始词', async () => {
    const store = setup()
    await store.beginSession(3, 4, WORD_IDS, 12)
    expect(apiMock.startSession).toHaveBeenCalledWith({
      sub_scene_id: 4,
      session_type: 'scene_learning',
    })
    expect(store.sessionId).toBe(42)
    expect(store.currentWordId).toBe(12)
    expect(store.dimension).toBe(1)
  })

  it('逐维按 form → meaning → sound → memory → usage 顺序上报', async () => {
    const store = setup()
    await store.beginSession(3, 4, WORD_IDS, 11)
    await store.advance() // form 完成
    await store.advance() // meaning 完成
    expect(apiMock.completeDimension.mock.calls.map((c) => c[0].dimension)).toEqual([
      'form',
      'meaning',
    ])
    expect(store.dimension).toBe(3)
    expect(apiMock.completeWord).not.toHaveBeenCalled()
  })

  it('五维走完自动完词并进入下一词', async () => {
    const store = setup()
    await store.beginSession(3, 4, WORD_IDS, 11)
    for (let i = 0; i < 5; i++) await store.advance()
    expect(apiMock.completeDimension.mock.calls.map((c) => c[0].dimension)).toEqual([
      'form',
      'meaning',
      'sound',
      'memory',
      'usage',
    ])
    expect(apiMock.completeWord).toHaveBeenCalledWith(
      expect.objectContaining({ word_id: 11, session_id: 42 })
    )
    expect(store.currentWordId).toBe(12)
    expect(store.dimension).toBe(1)
  })

  it('最后一个词完成后返回 done，不越界', async () => {
    const store = setup()
    await store.beginSession(3, 4, WORD_IDS, 13)
    for (let i = 0; i < 5; i++) await store.advance()
    expect(store.currentWordId).toBe(13)
    expect(apiMock.completeWord).toHaveBeenCalledWith(
      expect.objectContaining({ word_id: 13 })
    )
    expect(await store.advance()).toBe('done')
  })

  it('中途离开以请求体结束会话并上报时长', async () => {
    const store = setup()
    await store.beginSession(3, 4, WORD_IDS, 11)
    vi.advanceTimersByTime(90_000)
    await store.endLearning()
    // API 层签名是位置参数；「以请求体发送」由后端回归测试锁定
    expect(apiMock.endSession).toHaveBeenCalledWith(42, 90)
    // 重复结束不重复上报
    await store.endLearning()
    expect(apiMock.endSession).toHaveBeenCalledTimes(1)
  })

  it('完词流转后学习状态由后端返回（familiar）', async () => {
    const store = setup()
    await store.beginSession(3, 4, WORD_IDS, 11)
    for (let i = 0; i < 5; i++) await store.advance()
    const res = await apiMock.completeWord.mock.results[0].value
    expect(res.status).toBe('familiar')
  })
})
