// uni.* 全局 API 的内存实现，供 store 与工具函数测试使用
const memStorage = new Map<string, string>()

const uniMock = {
  getStorageSync: (key: string) => memStorage.get(key) ?? '',
  setStorageSync: (key: string, value: string) => {
    memStorage.set(key, value)
  },
  removeStorageSync: (key: string) => {
    memStorage.delete(key)
  },
}

;(globalThis as unknown as { uni: typeof uniMock }).uni = uniMock

export function resetUniStorage() {
  memStorage.clear()
}
