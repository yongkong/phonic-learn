import { defineStore } from 'pinia'
import type { User } from '@/types'
import { uniStorage } from '@/utils/uni-storage'

export const USER_STORAGE_KEY = 'user'

/** 从持久化存储读取 token（请求层使用；兼容旧平铺 {token} 格式） */
export function readStoredToken(): string {
  try {
    const parsed = JSON.parse(uni.getStorageSync(USER_STORAGE_KEY))
    return parsed?.user?.token || parsed?.token || ''
  } catch {
    return ''
  }
}

export const useUserStore = defineStore('user', {
  state: (): { user: User | null } => ({
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.user,
    nickname: (state) => state.user?.nickname || '',
    grade: (state) => state.user?.grade || 0,
    token: (state) => state.user?.token || '',
  },
  actions: {
    setUser(user: User) {
      this.user = user
    },
    logout() {
      this.user = null
    },
  },
  // key 固定为 USER_STORAGE_KEY：请求层经 readStoredToken 读取同一形状
  persist: { key: USER_STORAGE_KEY, storage: uniStorage },
})
