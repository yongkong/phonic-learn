import { describe, expect, it } from 'vitest'
import { DIMENSIONS, getDimension, dimensionIndex } from '@/utils/dimensions'

describe('五维维度映射（CONTEXT.md 术语表）', () => {
  it('顺序为 form → meaning → sound → memory → usage', () => {
    expect(DIMENSIONS.map((d) => d.key)).toEqual([
      'form',
      'meaning',
      'sound',
      'memory',
      'usage',
    ])
  })

  it('界面动词变体一一映射：认形 / 识义 / 拼读 / 巧记 / 运用', () => {
    expect(DIMENSIONS.map((d) => d.label)).toEqual([
      '认形',
      '识义',
      '拼读',
      '巧记',
      '运用',
    ])
  })

  it('不含漂移措辞「拼写」「组词」「发音」', () => {
    for (const d of DIMENSIONS) {
      expect(d.label).not.toMatch(/拼写|组词|发音/)
    }
  })

  it('getDimension / dimensionIndex 按 1-5 序号互查', () => {
    expect(getDimension(1)?.key).toBe('form')
    expect(getDimension(5)?.key).toBe('usage')
    expect(getDimension(6)).toBeUndefined()
    expect(dimensionIndex('sound')).toBe(3)
    expect(dimensionIndex('nope')).toBeUndefined()
  })
})
