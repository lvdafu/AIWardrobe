import { request } from '../utils/request'

export const getWardrobe = () => {
  return request('/api/wardrobe', 'GET')
}
