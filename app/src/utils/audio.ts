const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 当前播放的取消句柄：新播放开始前先取消上一次（旧 Promise 以完成落定，
// 避免切换单词/例句时播放态永久卡死）
let currentStop: (() => void) | null = null

/** 播放一段音频；可重复调用，后一次播放会打断前一次（跟读场景友好） */
function playAudio(kind: 'words' | 'sentences', filename: string): Promise<void> {
  currentStop?.()
  return new Promise((resolve, reject) => {
    const ctx = uni.createInnerAudioContext()
    let settled = false
    const settle = (err?: unknown) => {
      if (settled) return
      settled = true
      currentStop = null
      if (err === undefined) resolve()
      else reject(err)
    }
    currentStop = () => {
      try {
        ctx.stop()
        ctx.destroy()
      } catch {
        // 部分平台 destroy 后回调异常，忽略
      }
      settle()
    }
    ctx.src = `${BASE_URL}/api/v1/audios/${kind}/${filename}`
    ctx.onEnded(() => settle())
    ctx.onError((err) => settle(err))
    ctx.play()
  })
}

export function playWordAudio(filename: string): Promise<void> {
  return playAudio('words', filename)
}

export function playSentenceAudio(filename: string): Promise<void> {
  return playAudio('sentences', filename)
}

export function stopAudio() {
  currentStop?.()
}
