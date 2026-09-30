import { defineStore } from 'pinia'
import type { User } from '@/types'
import { uniStorage } from '@/utils/uni-storage'

export const useUserStore = defineStore('user', {
  state: (): { user: User | null; isOnboarded: boolean } => ({
    user: null,
    isOnboarded: false,
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
      this.isOnboarded = true
    },
    logout() {
      this.user = null
      this.isOnboarded = false
    },
  },
  // key 固定为 'user'：请求层从 uni.getStorageSync('user') 读取 token
  persist: { key: 'user', storage: uniStorage },
})
