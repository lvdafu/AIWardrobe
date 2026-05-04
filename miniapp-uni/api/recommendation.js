import { request } from '../utils/request'

export const getRecommendation = (params = {}) => {
  return request('/api/recommendation', 'GET', {
    location: params.location || '上海',
    goal: params.goal || ''
  })
}
