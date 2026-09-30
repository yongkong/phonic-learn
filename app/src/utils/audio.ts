const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

let innerAudioContext: UniApp.InnerAudioContext | null = null

function getAudioContext() {
  if (!innerAudioContext) {
    innerAudioContext = uni.createInnerAudioContext()
  }
  return innerAudioContext
}

/** 播放一段音频；每次重建监听，可重复调用供跟读 */
function playAudio(kind: 'words' | 'sentences', filename: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const audio = getAudioContext()
    audio.src = `${BASE_URL}/api/v1/audios/${kind}/${filename}`
    audio.stop()
    audio.onEnded(() => resolve())
    audio.onError((err) => reject(err))
    audio.play()
  })
}

export function playWordAudio(filename: string): Promise<void> {
  return playAudio('words', filename)
}

export function playSentenceAudio(filename: string): Promise<void> {
  return playAudio('sentences', filename)
}

export function stopAudio() {
  if (innerAudioContext) {
    innerAudioContext.stop()
  }
}
