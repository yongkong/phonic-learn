/** 五维：一个单词学习的五个维度，按 形 → 义 → 音 → 记 → 用 展开（CONTEXT.md） */
export type DimensionKey = 'form' | 'meaning' | 'sound' | 'memory' | 'usage'

export interface Dimension {
  key: DimensionKey
  /** 界面动词变体（术语表：认形 / 识义 / 拼读 / 巧记 / 运用） */
  label: string
}

export const DIMENSIONS: Dimension[] = [
  { key: 'form', label: '认形' },
  { key: 'meaning', label: '识义' },
  { key: 'sound', label: '拼读' },
  { key: 'memory', label: '巧记' },
  { key: 'usage', label: '运用' },
]

/** 按序号（1-5）取维度 */
export function getDimension(index: number): Dimension | undefined {
  return DIMENSIONS[index - 1]
}

/** 维度 key → 序号（1-5） */
export function dimensionIndex(key: string): number | undefined {
  const idx = DIMENSIONS.findIndex((d) => d.key === key)
  return idx >= 0 ? idx + 1 : undefined
}
