export interface LetterInfo {
  char: string
  type: 'vowel' | 'consonant' | 'silent' | 'digraph'
  color: 'red' | 'blue' | 'gray' | 'purple'
}

const VOWELS = new Set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'])

export function analyzeLetters(word: string): LetterInfo[] {
  const letters = word.toLowerCase().split('')
  const result: LetterInfo[] = []

  for (let i = 0; i < letters.length; i++) {
    const char = letters[i]

    // Silent 'e' at end
    if (char === 'e' && i === letters.length - 1 && letters.length > 2) {
      result.push({ char, type: 'silent', color: 'gray' })
      continue
    }

    if (VOWELS.has(char)) {
      result.push({ char, type: 'vowel', color: 'red' })
    } else if (/[a-z]/.test(char)) {
      result.push({ char, type: 'consonant', color: 'blue' })
    }
  }

  return result
}
