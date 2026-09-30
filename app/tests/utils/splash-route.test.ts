import { describe, expect, it } from 'vitest'
import { resolveSplashDestination } from '@/utils/splash-route'

describe('resolveSplashDestination', () => {
  it('已注册用户分流到首页', () => {
    expect(resolveSplashDestination(true)).toBe('/pages/home/index')
  })

  it('新用户分流到引导页', () => {
    expect(resolveSplashDestination(false)).toBe('/pages/onboarding/index')
  })
})
