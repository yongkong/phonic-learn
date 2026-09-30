import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { nextTick } from 'vue'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { useUserStore } from '@/stores/user'
import { resetUniStorage } from '../setup'

import type { User } from '@/types'

const fakeUser: User = {
  id: 1,
  nickname: '小明',
  grade: 3,
  avatar_url: null,
  token: 'tok-abc123',
  created_at: '2026-09-30T00:00:00Z',
}

function createTestPinia() {
  const pinia = createPinia()
  pinia.use(piniaPluginPersistedstate)
  // pinia 2.3 在 install 前只把插件排队（toBeInstalled），
  // 真实应用由 app.use(pinia) 触发 install，这里用桩 app 同步模拟
  pinia.install({ provide: () => {}, config: { globalProperties: {} } } as never)
  setActivePinia(pinia)
}

beforeEach(() => {
  resetUniStorage()
  createTestPinia()
})

describe('useUserStore', () => {
  it('初始为未登录', () => {
    const store = useUserStore()
    expect(store.isLoggedIn).toBe(false)
  })

  it('setUser 保存注册返回的用户与 token', () => {
    const store = useUserStore()
    store.setUser(fakeUser)
    expect(store.isLoggedIn).toBe(true)
    expect(store.token).toBe('tok-abc123')
    expect(store.nickname).toBe('小明')
    expect(store.grade).toBe(3)
  })

  it('状态持久化到 uni storage，新 store 实例可恢复登录态', async () => {
    const store = useUserStore()
    store.setUser(fakeUser)
    // 持久化经由 $subscribe 刷写，等一个微任务确保落盘
    await nextTick()

    // 模拟刷新页面：重建 pinia，再取 store
    createTestPinia()
    const restored = useUserStore()
    expect(restored.isLoggedIn).toBe(true)
    expect(restored.token).toBe('tok-abc123')
    expect(restored.nickname).toBe('小明')
  })

  it('logout 清空凭证回到未登录，持久化同步失效', () => {
    const store = useUserStore()
    store.setUser(fakeUser)
    store.logout()

    expect(store.isLoggedIn).toBe(false)
    expect(store.token).toBe('')

    createTestPinia()
    expect(useUserStore().isLoggedIn).toBe(false)
  })
})
