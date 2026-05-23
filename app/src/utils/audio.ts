const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

let innerAudioContext: UniApp.InnerAudioContext | null = null

export function getAudioContext() {
  if (!innerAudioContext) {
    innerAudioContext = uni.createInnerAudioContext()
  }
  return innerAudioContext
}

export function playWordAudio(filename: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const audio = getAudioContext()
    audio.src = `${BASE_URL}/api/v1/audios/words/${filename}`
    audio.onPlay(() => {})
    audio.onEnded(() => resolve())
    audio.onError((err) => reject(err))
    audio.play()
  })
}

export function stopAudio() {
  if (innerAudioContext) {
    innerAudioContext.stop()
  }
}
