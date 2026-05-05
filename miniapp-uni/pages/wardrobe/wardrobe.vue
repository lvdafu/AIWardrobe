<template>
  <view class="page">
    <view class="search-wrap">
      <input
        class="search-input"
        v-model="searchText"
        placeholder="搜索名称、描述..."
        placeholder-class="search-placeholder"
      />
    </view>

    <view class="filter-wrap">
      <view class="filter-row">
        <text class="filter-label">季节</text>
        <view class="chips">
          <view
            v-for="s in seasons"
            :key="s"
            class="chip"
            :class="{ active: selectedSeason === s }"
            @click="toggleSeason(s)"
          >
            {{ s }}
          </view>
        </view>
      </view>

      <view class="filter-row">
        <text class="filter-label">风格</text>
        <view class="chips">
          <view
            v-for="s in styles"
            :key="s"
            class="chip"
            :class="{ active: selectedStyle === s }"
            @click="toggleStyle(s)"
          >
            {{ s }}
          </view>
        </view>
      </view>
    </view>

    <block v-for="section in groupedSections" :key="section.key">
      <view class="section" v-if="section.items.length > 0">
        <view class="section-header">
          <text class="section-title">{{ section.title }}</text>
          <text class="section-count">{{ section.items.length }}</text>
        </view>

        <view class="grid">
          <view class="card" v-for="item in section.items" :key="item.id">
            <image class="card-image" :src="toImageUrl(item.image_url)" mode="aspectFit" />
            <view class="card-body">
              <text class="card-name">{{ item.item }}</text>
              <text class="card-desc">{{ item.description || '暂无描述' }}</text>
            </view>
          </view>
        </view>
      </view>
    </block>
  </view>
</template>

<script>
import { getWardrobe } from '../../api/wardrobe'
import { BASE_URL } from '../../utils/config'

export default {
  data() {
    return {
      wardrobe: {
        tops: [],
        bottoms: [],
        shoes: [],
        accessories: []
      },
      searchText: '',
      selectedSeason: '',
      selectedStyle: '',
      seasons: ['春', '夏', '秋', '冬'],
      styles: ['休闲', '正式', '运动', '商务', '复古', '简约', '日常']
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
    filteredItems() {
      const keyword = (this.searchText || '').trim().toLowerCase()
      return this.allItems.filter((item) => {
        const hitKeyword = !keyword ||
          (item.item || '').toLowerCase().includes(keyword) ||
          (item.description || '').toLowerCase().includes(keyword)

        const hitSeason = !this.selectedSeason || (item.season_semantics || []).includes(this.selectedSeason)
        const hitStyle = !this.selectedStyle || (item.style_semantics || []).includes(this.selectedStyle)

        return hitKeyword && hitSeason && hitStyle
      })
    },
    groupedSections() {
      const map = {
        top: { key: 'top', title: '上装', items: [] },
        bottom: { key: 'bottom', title: '下装', items: [] },
        shoes: { key: 'shoes', title: '鞋履', items: [] },
        accessory: { key: 'accessory', title: '配饰', items: [] }
      }

      this.filteredItems.forEach((item) => {
        const k = item.category in map ? item.category : 'accessory'
        map[k].items.push(item)
      })

      return [map.top, map.bottom, map.shoes, map.accessory]
    }
  },
  onLoad() {
    this.loadData()
  },
  onShow() {
    this.loadData()
  },
  methods: {
    toImageUrl(url) {
      if (!url) return ''
      if (/^https?:\/\//.test(url)) return url
      return `${BASE_URL}${url}`
    },
    toggleSeason(v) {
      this.selectedSeason = this.selectedSeason === v ? '' : v
    },
    toggleStyle(v) {
      this.selectedStyle = this.selectedStyle === v ? '' : v
    },
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
.page {
  min-height: 100vh;
  background: #f6f7fb;
  padding: 20rpx;
}

.search-wrap {
  background: #fff;
  border-radius: 24rpx;
  padding: 16rpx 20rpx;
}

.search-input {
  height: 72rpx;
  background: #f3f4f6;
  border-radius: 20rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
}

.search-placeholder {
  color: #9ca3af;
}

.filter-wrap {
  margin-top: 20rpx;
  background: #fff;
  border-radius: 24rpx;
  padding: 20rpx;
}

.filter-row {
  margin-bottom: 14rpx;
}

.filter-label {
  font-size: 28rpx;
  color: #4b5563;
  margin-right: 16rpx;
}

.chips {
  margin-top: 10rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 14rpx;
}

.chip {
  padding: 10rpx 22rpx;
  border-radius: 999rpx;
  background: #f3f4f6;
  color: #4b5563;
  font-size: 24rpx;
}

.chip.active {
  background: #e0ecff;
  color: #2563eb;
}

.section {
  margin-top: 22rpx;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 16rpx;
}

.section-title {
  font-size: 40rpx;
  font-weight: 600;
}

.section-count {
  color: #9ca3af;
  font-size: 28rpx;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20rpx;
}

.card {
  background: #fff;
  border-radius: 24rpx;
  overflow: hidden;
  border: 1rpx solid #e5e7eb;
}

.card-image {
  width: 100%;
  height: 260rpx;
  background: #f9fafb;
}

.card-body {
  padding: 16rpx;
}

.card-name {
  display: block;
  font-size: 28rpx;
  color: #111827;
  margin-bottom: 8rpx;
  line-height: 1.4;
}

.card-desc {
  display: block;
  font-size: 24rpx;
  color: #6b7280;
  line-height: 1.4;
}
</style>
