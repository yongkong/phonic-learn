export function setItem<T>(key: string, value: T): void {
  try {
    uni.setStorageSync(key, JSON.stringify(value))
  } catch (e) {
    console.error('Storage set error:', e)
  }
}

export function getItem<T>(key: string): T | null {
  try {
    const value = uni.getStorageSync(key)
    return value ? JSON.parse(value) : null
  } catch (e) {
    return null
  }
}

export function removeItem(key: string): void {
  try {
    uni.removeStorageSync(key)
  } catch (e) {}
}
