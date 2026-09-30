export interface SplashDestination {
  url: string
  /** 是否 tabBar 页面：tab 页必须用 switchTab，否则 navigateTo */
  isTab: boolean
}

/** 启动页分流：登录态去首页，否则进引导 */
export function resolveSplashDestination(isLoggedIn: boolean): SplashDestination {
  return isLoggedIn
    ? { url: '/pages/home/index', isTab: true }
    : { url: '/pages/onboarding/index', isTab: false }
}
