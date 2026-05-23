const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export interface ApiResponse<T = any> {
  code?: number
  message?: string
  data: T
}

export function request<T = any>(
  url: string,
  options: UniApp.RequestOptions = {}
): Promise<T> {
  return new Promise((resolve, reject) => {
    // Get token from storage
    const userStr = uni.getStorageSync('user')
    let token = ''
    try {
      const user = JSON.parse(userStr)
      token = user?.token || ''
    } catch (e) {}

    uni.request({
      url: `${BASE_URL}${url}`,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.header,
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data as T)
        } else if (res.statusCode === 401) {
          uni.showToast({ title: '请重新登录', icon: 'none' })
          reject(new Error('Unauthorized'))
        } else {
          const errorMsg = (res.data as any)?.detail || '请求失败'
          uni.showToast({ title: errorMsg, icon: 'none' })
          reject(new Error(errorMsg))
        }
      },
      fail: (err) => {
        uni.showToast({ title: '网络错误', icon: 'none' })
        reject(err)
      },
    })
  })
}
