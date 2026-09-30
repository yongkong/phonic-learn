import type { WordListItem } from '@/types'

export type LearningStatus = WordListItem['learning_status']

export interface LearningStatusMeta {
  /** 中文标签（CONTEXT.md 术语表：新学 / 学习中 / 熟悉 / 掌握） */
  label: string
  /** 形状标识：状态不能只靠颜色区分，需配形状 + 文字 */
  shape: 'circle' | 'half' | 'star-outline' | 'star'
}

const META: Record<LearningStatus, LearningStatusMeta> = {
  new: { label: '新学', shape: 'circle' },
  learning: { label: '学习中', shape: 'half' },
  familiar: { label: '熟悉', shape: 'star-outline' },
  mastered: { label: '掌握', shape: 'star' },
}

export function getLearningStatusMeta(status: LearningStatus): LearningStatusMeta {
  return META[status] || META.new
}
