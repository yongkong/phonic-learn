import { describe, expect, it } from 'vitest'
import { getLearningStatusMeta } from '@/utils/learning-status'

const ALL = ['new', 'learning', 'familiar', 'mastered'] as const

describe('getLearningStatusMeta', () => {
  it('四种状态与术语表标签一一映射', () => {
    expect(getLearningStatusMeta('new').label).toBe('新学')
    expect(getLearningStatusMeta('learning').label).toBe('学习中')
    expect(getLearningStatusMeta('familiar').label).toBe('熟悉')
    expect(getLearningStatusMeta('mastered').label).toBe('掌握')
  })

  it('每种状态有形状标识与图标绘制段（非仅颜色区分）', () => {
    for (const status of ALL) {
      const meta = getLearningStatusMeta(status)
      expect(meta.shape.length).toBeGreaterThan(0)
      expect(meta.label.length).toBeGreaterThan(0)
      expect(meta.icon.length).toBeGreaterThan(0)
      expect(meta.icon.every((seg) => seg.d.length > 0)).toBe(true)
    }
  })

  it('四档形状互不相同：○ / ◐ / ☆ / ★', () => {
    const shapes = ALL.map((s) => getLearningStatusMeta(s).shape)
    expect(new Set(shapes).size).toBe(4)
  })

  it('渲染段（路径 + 填充态）互不相同：熟悉描边星 ≠ 掌握实心星', () => {
    const sigs = ALL.map((s) =>
      getLearningStatusMeta(s)
        .icon.map((seg) => `${seg.d}|${seg.filled ? 1 : 0}`)
        .join(';')
    )
    expect(new Set(sigs).size).toBe(4)
    expect(getLearningStatusMeta('familiar').icon[0].filled).toBeFalsy()
    expect(getLearningStatusMeta('mastered').icon[0].filled).toBe(true)
  })

  it('未知状态回退到「新学」', () => {
    expect(getLearningStatusMeta('whatever' as never).label).toBe('新学')
  })
})
