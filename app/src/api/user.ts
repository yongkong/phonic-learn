import { request } from './request'
import type { User, UserStats } from '@/types'

export const registerUser = (data: { nickname: string; grade: number }) =>
  request<User>('/api/v1/users/register', { method: 'POST', data })

export const getCurrentUser = () => request<User>('/api/v1/users/me')

export const getUserStats = () => request<UserStats>('/api/v1/users/me/stats')
