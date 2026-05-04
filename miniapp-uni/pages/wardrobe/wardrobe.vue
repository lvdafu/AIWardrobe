<template>
  <view class="page">
    <view class="card">
      <button type="primary" @click="loadData">刷新衣橱</button>
    </view>

    <view class="card">
      <view class="section-title">衣橱统计</view>
      <view class="line">上装：{{ wardrobe.tops.length }}</view>
      <view class="line">下装：{{ wardrobe.bottoms.length }}</view>
      <view class="line">鞋履：{{ wardrobe.shoes.length }}</view>
      <view class="line">配饰：{{ wardrobe.accessories.length }}</view>
    </view>

    <view class="card" v-if="allItems.length">
      <view class="section-title">全部单品（前 20 条）</view>
      <view class="line" v-for="item in firstTwentyItems" :key="item.id">
        #{{ item.id }} {{ item.item }}（{{ item.category }}）
      </view>
    </view>
  </view>
</template>

<script>
import { getWardrobe } from '../../api/wardrobe'

export default {
  data() {
    return {
      wardrobe: {
        tops: [],
        bottoms: [],
        shoes: [],
        accessories: []
      }
    }
  },
  computed: {
    allItems() {
      return [
        ...this.wardrobe.tops,
        ...this.wardrobe.bottoms,
        ...this.wardrobe.shoes,
        ...this.wardrobe.accessories
      ]
    },
    firstTwentyItems() {
      return this.allItems.slice(0, 20)
    }
  },
  onLoad() {
    this.loadData()
  },
  methods: {
    async loadData() {
      uni.showLoading({ title: '加载中' })
      try {
        this.wardrobe = await getWardrobe()
      } catch (error) {
        uni.showToast({ title: '衣橱加载失败', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
    }
  }
}
</script>

<style scoped>
.line {
  margin-bottom: 12rpx;
}
</style>
