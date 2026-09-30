/** 启动页分流：登录态去首页，否则进引导（两处均用 reLaunch，避免 splash 滞留返回栈） */
export function resolveSplashDestination(isLoggedIn: boolean): string {
  return isLoggedIn ? '/pages/home/index' : '/pages/onboarding/index'
}
