import type { WordListItem } from '@/types'

export type LearningStatus = WordListItem['learning_status']

/** 状态图标的单个绘制段（filled=true 时填充，否则仅描边） */
export interface StatusIconSegment {
  d: string
  filled?: boolean
}

export interface LearningStatusMeta {
  /** 中文标签（CONTEXT.md 术语表：新学 / 学习中 / 熟悉 / 掌握） */
  label: string
  /** 形状标识：状态不能只靠颜色区分，需配形状 + 文字 */
  shape: 'circle' | 'half' | 'star-outline' | 'star'
  /** 线性小图标绘制段（24 viewBox，stroke 2.4、圆帽） */
  icon: StatusIconSegment[]
}

const RING = 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z'
const STAR = 'M12 3l1.9 5.8L20 10.6l-4.9 3.9 1.6 6-4.7-3.6-4.7 3.6 1.6-6L4 10.6l6.1-1.8z'

const META: Record<LearningStatus, LearningStatusMeta> = {
  // ○ 空心圆
  new: { label: '新学', shape: 'circle', icon: [{ d: RING }] },
  // ◐ 外环描边 + 左半填充
  learning: {
    label: '学习中',
    shape: 'half',
    icon: [
      { d: RING },
      { d: 'M12 3a9 9 0 0 0 0 18z', filled: true },
    ],
  },
  // ☆ 描边星
  familiar: { label: '熟悉', shape: 'star-outline', icon: [{ d: STAR }] },
  // ★ 实心星
  mastered: { label: '掌握', shape: 'star', icon: [{ d: STAR, filled: true }] },
}

export function getLearningStatusMeta(status: LearningStatus): LearningStatusMeta {
  return META[status] || META.new
}
