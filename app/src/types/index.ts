// 用户相关
export interface User {
  id: number
  nickname: string
  grade: number
  avatar_url: string | null
  token: string
  created_at: string
}

export interface UserStats {
  total_learned: number
  total_mastered: number
  total_pending_review: number
  study_streak_days: number
  today_learned: number
  today_target: number
  weekly_stats: { date: string; words_count: number }[]
  average_pronunciation_score: number | null
}

// 场景相关
export interface SubScene {
  id: number
  name: string
  icon: string | null
  sort_order: number
  description: string | null
  illustration_url: string | null
  word_count: number
  learned_count: number
  is_unlocked: boolean
}

export interface Scene {
  id: number
  name: string
  icon: string
  sort_order: number
  description: string | null
  target_grades: string
  sub_scenes: SubScene[]
  progress: number
}

// 单词相关
export interface Meaning {
  pos: string
  cn: string
}

export interface ExampleSentence {
  en: string
  cn: string
  audio_filename: string | null
}

export interface PhonicsLetterSound {
  letter: string
  sound: string
  type: 'vowel' | 'consonant' | 'silent' | 'digraph'
  color: 'red' | 'blue' | 'gray' | 'purple'
}

export interface PhonicsAnalysis {
  syllables: string[]
  syllable_phonetics: string[]
  stress_index: number
  letter_sounds: PhonicsLetterSound[]
}

export interface MemoryTip {
  type: string
  content: string
}

export interface WordListItem {
  id: number
  spelling: string
  emoji: string | null
  phonetic_us: string | null
  meanings: Meaning[]
  image_url: string | null
  audio_filename: string | null
  learning_status: 'new' | 'learning' | 'familiar' | 'mastered'
  pronunciation_score: number | null
}

export interface WordDetail extends WordListItem {
  phonetic_uk: string | null
  example_sentences: ExampleSentence[]
  phonic_analysis: PhonicsAnalysis
  memory_tips: MemoryTip[] | null
  tags: string[] | null
  grade_range: string
}

// 学习相关
export interface DimensionProgress {
  completed: boolean
  score?: number
  completed_at?: string
}

export interface WordProgress {
  form: DimensionProgress
  meaning: DimensionProgress
  sound: DimensionProgress
  memory: DimensionProgress
  usage: DimensionProgress
}

export interface LearningStats {
  total_words: number
  learned_words: number
  mastered_words: number
  pending_review: number
  today_learned: number
  today_target: number
  average_score: number | null
  /** 五维完成总数（各学习记录已完成维度之和） */
  dimensions_completed: number
  /** 最早到点的复习安排（简化 SM-2 产物），无则 null */
  next_review_at: string | null
}
