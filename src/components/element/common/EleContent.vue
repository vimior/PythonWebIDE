<template>
  <div class="v-content-box">
    <div class="v-content-title">
      <span>
        <el-icon><reading /></el-icon>
        {{ $route.meta.title }}
      </span>
    </div>
    <el-card class="v-content-card">
      <div class="content">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </div>
    </el-card>
  </div>
</template>

<script>
import {List, Reading} from '@element-plus/icons';

export default {
  props: {
    tag: Object,
    tags: List,
  },
  data() {
    return {

    }
  },
  components: {
    Reading,
  }
}
</script>

<style scoped>
html, body {
  overflow: hidden;
  overflow-y: hidden;
  overflow-x: hidden;
}
.v-content-box {
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 40px;
  width: auto;
  height: 100%;
  /* padding: 10px; */
  overflow-y: auto;
  box-sizing: border-box;
}
.v-content-box .v-content-title {
  position: fixed;
  /* height: 20px; */
  text-align: left;
  /* margin-left: 5px; */
  margin-top: -34px;
  font-size: 20px;
}
.v-content-box .v-content-card .content {
  background: white;
  margin-left: 5px;
  /* margin-top: 30px; */
  border-radius: 10px;
  padding: 20px 30px 20px 30px;
}
</style>