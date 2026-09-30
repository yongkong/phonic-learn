import type { PhonicsLetterSound } from '@/types'

// 自然拼读语义色（教学功能色）：与 styles/tokens.scss 的同名令牌保持一致，
// 模板内联着色需要 JS 侧色值，故在此单源维护
export const PHONIC_COLORS: Record<PhonicsLetterSound['color'], string> = {
  red: '#FF6B6B', // 元音 $vowel
  blue: '#4F46E5', // 辅音 $consonant
  gray: '#9CA3AF', // 静音 $silent
  purple: '#8B5CF6', // 字母组合 $digraph
}
