import { BASE_URL } from '../utils/config'

export function uploadClothes(filePath) {
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: `${BASE_URL}/api/upload`,
      filePath,
      name: 'file',
      timeout: 180000,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(res.data))
        } else {
          reject(new Error(`上传失败: ${res.statusCode} ${res.data}`))
        }
      },
      fail: reject
    })
  })
}
