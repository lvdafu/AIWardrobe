<template>
  <view class="page">
    <view class="card">
      <view class="section-title">推荐参数</view>
      <input class="input" v-model="location" placeholder="城市，如上海" />
      <input class="input" v-model="goal" placeholder="场景，如通勤/约会/运动" />
      <button type="primary" @click="loadData">获取推荐</button>
    </view>

    <view class="card" v-if="data">
      <view class="section-title">推荐结果</view>
      <view class="line">天气：{{ weatherCondition }} {{ weatherTemperature }}°C</view>
      <view class="line">总结：{{ outfitSummary }}</view>
      <view class="line">上装：{{ suggestedTop }}</view>
      <view class="line">下装：{{ suggestedBottom }}</view>
      <view class="line">鞋履：{{ suggestedShoes }}</view>
    </view>

    <view class="card" v-if="recommendationText">
      <view class="section-title">AI 文案</view>
      <view class="text">{{ recommendationText }}</view>
    </view>
  </view>
</template>

<script>
import { getRecommendation } from '../../api/recommendation'

export default {
  data() {
    return {
      location: '上海',
      goal: '',
      data: null
    }
  },
  computed: {
    weatherCondition() {
      return this.data && this.data.weather ? this.data.weather.condition || '' : ''
    },
    weatherTemperature() {
      return this.data && this.data.weather ? this.data.weather.temperature || '' : ''
    },
    outfitSummary() {
      return this.data && this.data.outfit_summary ? this.data.outfit_summary : '暂无'
    },
    suggestedTop() {
      return this.data && this.data.suggested_top && this.data.suggested_top.item
        ? this.data.suggested_top.item
        : '无'
    },
    suggestedBottom() {
      return this.data && this.data.suggested_bottom && this.data.suggested_bottom.item
        ? this.data.suggested_bottom.item
        : '无'
    },
    suggestedShoes() {
      return this.data && this.data.suggested_shoes && this.data.suggested_shoes.item
        ? this.data.suggested_shoes.item
        : '无'
    },
    recommendationText() {
      return this.data && this.data.recommendation_text ? this.data.recommendation_text : ''
    }
  },
  methods: {
    async loadData() {
      uni.showLoading({ title: '生成中' })
      try {
        this.data = await getRecommendation({
          location: this.location,
          goal: this.goal
        })
      } catch (error) {
        uni.showToast({ title: '推荐失败', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
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
  margin-bottom: 16rpx;
  background: #fff;
}

.line {
  margin-bottom: 12rpx;
}

.text {
  line-height: 1.7;
  white-space: pre-wrap;
}
</style>
