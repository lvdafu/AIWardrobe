import { request } from '../utils/request'

export const getWeather = (location = '上海') => {
  return request('/api/weather', 'GET', { location })
}
