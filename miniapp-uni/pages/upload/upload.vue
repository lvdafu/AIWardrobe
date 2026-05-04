<template>
  <view class="page">
    <view class="card">
      <view class="section-title">上传衣物照片</view>
      <button type="primary" @click="chooseAndUpload">选择并上传</button>
      <view class="tip">支持相册/拍照，上传后会自动识别类别和描述。</view>
    </view>

    <view class="card" v-if="result">
      <view class="section-title">识别结果</view>
      <view class="line">名称：{{ result.item }}</view>
      <view class="line">类别：{{ result.category }}</view>
      <view class="line">描述：{{ result.description || '无' }}</view>
      <image
        v-if="result.image_url"
        :src="result.image_url"
        mode="widthFix"
        class="preview"
      />
    </view>
  </view>
</template>

<script>
import { uploadClothes } from '../../api/upload'

export default {
  data() {
    return {
      result: null
    }
  },
  methods: {
    chooseAndUpload() {
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: async (res) => {
          const filePath = res.tempFilePaths[0]
          uni.showLoading({ title: '上传中' })
          try {
            this.result = await uploadClothes(filePath)
            uni.showToast({ title: '上传成功', icon: 'success' })
          } catch (error) {
            uni.showToast({ title: '上传失败', icon: 'none' })
          } finally {
            uni.hideLoading()
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.tip {
  color: #6b7280;
  margin-top: 16rpx;
}

.line {
  margin-bottom: 12rpx;
}

.preview {
  width: 100%;
  margin-top: 16rpx;
  border-radius: 12rpx;
}
</style>
