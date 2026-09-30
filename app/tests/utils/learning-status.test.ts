import { describe, expect, it } from 'vitest'
import { getLearningStatusMeta } from '@/utils/learning-status'

describe('getLearningStatusMeta', () => {
  it('四种状态与术语表标签一一映射', () => {
    expect(getLearningStatusMeta('new').label).toBe('新学')
    expect(getLearningStatusMeta('learning').label).toBe('学习中')
    expect(getLearningStatusMeta('familiar').label).toBe('熟悉')
    expect(getLearningStatusMeta('mastered').label).toBe('掌握')
  })

  it('每种状态有形状标识（非仅颜色区分）', () => {
    for (const status of ['new', 'learning', 'familiar', 'mastered'] as const) {
      const meta = getLearningStatusMeta(status)
      expect(meta.shape.length).toBeGreaterThan(0)
      expect(meta.label.length).toBeGreaterThan(0)
    }
  })

  it('形状互不相同：新学○ / 学习中◐ / 熟悉☆ / 掌握★', () => {
    const shapes = ['new', 'learning', 'familiar', 'mastered'].map(
      (s) => getLearningStatusMeta(s).shape
    )
    expect(new Set(shapes).size).toBe(4)
  })

  it('未知状态回退到「新学」', () => {
    expect(getLearningStatusMeta('whatever' as never).label).toBe('新学')
  })
})
