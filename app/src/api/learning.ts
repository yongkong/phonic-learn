import { request } from './request'
import type { LearningStats } from '@/types'

export const startSession = (data: { sub_scene_id: number; session_type?: string }) =>
  request('/api/v1/learning/start-session', { method: 'POST', data })

export const completeDimension = (data: { word_id: number; dimension: string; score?: number }) =>
  request('/api/v1/learning/complete-dimension', { method: 'POST', data })

export const completeWord = (data: { word_id: number; session_id: number; final_pronunciation_score?: number; spelling_correct?: boolean }) =>
  request('/api/v1/learning/complete-word', { method: 'POST', data })

export const recordPronunciation = (data: { word_id: number; score: number }) =>
  request('/api/v1/learning/record-pronunciation', { method: 'POST', data })

export const recordSpelling = (data: { word_id: number; correct: boolean }) =>
  request('/api/v1/learning/record-spelling', { method: 'POST', data })

export const endSession = (sessionId: number, durationSeconds: number) =>
  request('/api/v1/learning/end-session', {
    method: 'POST',
    data: { session_id: sessionId, duration_seconds: durationSeconds },
  })

export const getLearningStats = () => request<LearningStats>('/api/v1/learning/stats')
