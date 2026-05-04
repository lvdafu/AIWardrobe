<template>
  <view class="page">
    <view class="card">
      <view class="section-title">当前城市</view>
      <input class="input" v-model="location" placeholder="输入城市，如上海" />
      <button type="primary" @click="loadWeather">刷新天气</button>
    </view>

    <view class="card" v-if="weather">
      <view class="section-title">天气信息</view>
      <view class="line">地点：{{ weather.location || location }}</view>
      <view class="line">天气：{{ weather.condition }}</view>
      <view class="line">温度：{{ weather.temperature }}°C</view>
      <view class="line">体感：{{ weather.feelsLike }}°C</view>
    </view>

    <view class="card">
      <view class="section-title">快捷入口</view>
      <button @click="goRecommend">今日推荐</button>
      <button @click="goWardrobe">我的衣橱</button>
      <button @click="goUpload">上传衣物</button>
    </view>
  </view>
</template>

<script>
import { getWeather } from '../../api/weather'

export default {
  data() {
    return {
      location: '上海',
      weather: null
    }
  },
  onLoad() {
    this.loadWeather()
  },
  methods: {
    async loadWeather() {
      uni.showLoading({ title: '加载中' })
      try {
        this.weather = await getWeather(this.location)
      } catch (error) {
        uni.showToast({ title: '天气加载失败', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
    },
    goRecommend() {
      uni.switchTab({ url: '/pages/recommend/recommend' })
    },
    goWardrobe() {
      uni.switchTab({ url: '/pages/wardrobe/wardrobe' })
    },
    goUpload() {
      uni.switchTab({ url: '/pages/upload/upload' })
    }
  }
}
</script>

<style scoped>
.input {
  height: 76rpx;
  border: 1rpx solid #e5e7eb;
  border-radius: 12rpx;
  padding: 0 20rpx;
  margin-bottom: 20rpx;
  background: #fff;
}

.line {
  margin-bottom: 12rpx;
}

button {
  margin-bottom: 16rpx;
}
</style>
