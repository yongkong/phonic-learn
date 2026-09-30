import { describe, expect, it } from 'vitest'
import { resolveSplashDestination } from '@/utils/splash-route'

describe('resolveSplashDestination', () => {
  it('已注册用户分流到首页（tabBar 页）', () => {
    const dest = resolveSplashDestination(true)
    expect(dest.url).toBe('/pages/home/index')
    expect(dest.isTab).toBe(true)
  })

  it('新用户分流到引导页（非 tabBar 页）', () => {
    const dest = resolveSplashDestination(false)
    expect(dest.url).toBe('/pages/onboarding/index')
    expect(dest.isTab).toBe(false)
  })
})
