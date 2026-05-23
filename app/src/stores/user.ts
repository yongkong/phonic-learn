import { defineStore } from 'pinia'
import type { User } from '@/types'

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
  persist: true,
})
