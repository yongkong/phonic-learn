<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('App Launch')
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style lang="scss">
page {
  background-color: $bg;
  font-family: $font-body;
  color: $fg;
  font-size: 28rpx;
}

/* 桌面端（≥1024px）：SiteHeader 顶栏替代底部 tabBar 与原生标题栏 */
@media (min-width: 1024px) {
  uni-tabbar,
  .uni-tabbar,
  uni-page-head {
    display: none !important;
  }
}
</style>
