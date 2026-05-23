import { request } from './request'
import type { Scene, WordListItem, WordDetail } from '@/types'

export const getScenes = () => request<Scene[]>('/api/v1/scenes')

export const getScene = (id: number) => request<Scene>(`/api/v1/scenes/${id}`)

export const getSubSceneWords = (subSceneId: number) =>
  request<WordListItem[]>(`/api/v1/words/sub-scenes/${subSceneId}/words`)

export const getWordDetail = (wordId: number) =>
  request<WordDetail>(`/api/v1/words/${wordId}`)
