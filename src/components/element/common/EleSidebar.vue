<template>
  <div class="v-sidebar">
    <el-menu
      class="v-sidebar-el-menu"
      :default-active="onRoutes"
      :collapse="collapse"
      background-color="#324157"
      text-color="#bfcbd9"
      active-text-color="#20a0ff"
      unique-opened
      router>
      <el-menu-item index="/">
        <el-icon><home-filled /></el-icon>
        <span>首页</span>
      </el-menu-item>

      <el-sub-menu index="base">
        <template #title>
          <el-icon><magic-stick /></el-icon>
          <span>基础组件</span>
        </template>
        <el-menu-item :index="basePath + 'base'">
          <span>基础组件</span>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="data">
        <template #title>
          <el-icon><data-board /></el-icon>
          <span>数据展示</span>
        </template>
        <el-menu-item :index="basePath + 'table'">
          <span>基础表格</span>
        </el-menu-item>
        <el-menu-item :index="basePath + 'tree'">
          <span>树形控件</span>
        </el-menu-item>
        <el-menu-item :index="basePath + 'timeline'">
          <span>时间线</span>
        </el-menu-item>
        <el-menu-item :index="basePath + 'progress'">
          <span>进度条</span>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="navigation">
        <template #title>
          <el-icon><location /></el-icon>
          <span>导航相关</span>
        </template>
        <el-menu-item :index="basePath + 'tabs'">
          <span>Tabs选项卡</span>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="forms">
        <template #title>
          <el-icon><document /></el-icon>
          <span>表单组件</span>
        </template>
        <el-menu-item :index="basePath + 'base-form'">
          <span>基础表单</span>
        </el-menu-item>
        <el-menu-item :index="basePath + 'upload-file'">
          <span>上传文件</span>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="draggable">
        <template #title>
          <el-icon><rank /></el-icon>
          <span>拖拽组件</span>
        </template>
        <el-menu-item :index="basePath + 'draggable-list'">
          <span>拖拽列表</span>
        </el-menu-item>
        <el-menu-item :index="basePath + 'draggable-dialog'">
          <span>拖拽弹框</span>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="charts">
        <template #title>
          <el-icon><pie-chart /></el-icon>
          <span>图表</span>
        </template>
        <el-menu-item :index="basePath + 'vue-schart'">
          <span>Vue-Schart</span>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="editors">
        <template #title>
          <el-icon><edit /></el-icon>
          <span>编辑器</span>
        </template>
        <el-menu-item :index="basePath + 'codemirror-editor'">
          <span title="CodeMirror-Editor">代码编辑器</span>
        </el-menu-item>
        <el-menu-item :index="basePath + 'markdown-editor'">
          <span title="Markdown-Editor">Markdown编辑器</span>
        </el-menu-item>
        <el-menu-item :index="basePath + 'quill-editor'">
          <span title="Quill-Editor">富文本编辑器</span>
        </el-menu-item>
      </el-sub-menu>
      
    </el-menu>
  </div>
</template>

<script>
import { HomeFilled, DataBoard, MagicStick, Location, Edit, Document, Rank, PieChart } from '@element-plus/icons';

export default {
  props: {
    collapse: Boolean,
  },
  data() {
    return {
      basePath: '/element/'
    }
  },
  computed: {
    onRoutes() {
      return this.$route.path.replace('/', '');
    }
  },
  components: {
    HomeFilled,
    DataBoard,
    MagicStick,
    Location,
    Edit,
    Document,
    Rank,
    PieChart,
  }
}
</script>

<style scoped>
.v-sidebar {
  position: absolute;
  top: 70px;
  bottom: 0;
  left: 0;
  overflow-y: auto;
  overflow-x: hidden;
  text-align: left;
  display: block;
}
.v-sidebar::-webkit-scrollbar {
  width: 0;
}
.v-sidebar-el-menu {
  height: 100%;
}
.v-sidebar-el-menu:not(.el-menu--collapse) {
  width: 200px;
}
</style>