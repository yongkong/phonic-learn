// pinia-plugin-persistedstate 在 uni-app 各端的存储适配器。
// 直接透传原始字符串（插件自己负责 JSON 序列化），保证 H5 与小程序端行为一致。
export const uniStorage = {
  getItem: (key: string): string => (uni.getStorageSync(key) as string) ?? '',
  setItem: (key: string, value: string) => {
    uni.setStorageSync(key, value)
  },
}
