<template>
  <div class="noselected code-tabs">
    <el-tabs
      v-model="pathSelected"
      type="card"
      closable
      @tab-remove="removeTab"
      @tab-click="selectTab"
    >
      <el-tab-pane
        v-for="item in codeItems"
        :key="item.path"
        :label="item.name"
        :name="item.path"
      >
        <template #label>
          <img :src="getIconUrl(item.path)" alt="" class="node-icon" />
          <span class="node-label">{{ item.name }}</span>
        </template>
        <span class="file-path">/{{ ideInfo.currProj.data.name + item.path }}</span>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { getIconForFile } from 'vscode-icons-js';

export default {
  data() {
    return {
    };
  },
  mounted() {
  },
  methods: {
    getIconUrl(path) {
      return require(`@/assets/vscode-icons/${getIconForFile(path.substring(path.lastIndexOf('.') + 1))}`);
    },
    getItem(path) {
      for (let i = 0; i < this.ideInfo.codeItems.length; i++) {
        if (this.ideInfo.codeItems[i].path === path) {
          return this.ideInfo.codeItems[i];
        }
      }
      return '';
    },
    selectTab(path) {
      // const item = this.getItem(path);
      // if (!item) return;
      // this.$emit('select-item', item);
    },
    removeTab(path) {
      const item = this.getItem(path);
      if (!item) return;
      this.$emit('close-item', item);
    }
  },
  watch: {
  },
  computed: {
    ideInfo() {
      return this.$store.state.ide.ideInfo;
    },
    codeItems() {
      return this.ideInfo.codeItems;
    },
    pathSelected: {
      get() {
        return this.ideInfo.currProj.pathSelected;
      },
      set(val) {
        const item = this.getItem(val);
        if (!item) return;
        this.$emit('select-item', item);
      }
    }
  },
  components: {
  },
};
</script>

<style>
.code-tabs .el-tabs {
  --el-tabs-header-height: 25px;
}
.code-tabs .el-tabs--card>.el-tabs__header .el-tabs__nav {
  border: none;
  background: #404041;
  border-radius: 0px;
}
.code-tabs .el-tabs--card>.el-tabs__header {
  border-color: #404041;
  background: #404041;
}
.code-tabs .el-tabs__content {
  margin-top: -15px;
}
.code-tabs .el-tabs__item {
  height: 26px;
  padding-left: 10px;
  padding-right: 3px;
  line-height: 26px;
  font-size: 13px;
  font-weight: 500;
  font-family: 'Gotham-Book';
  color: #CCCCCC;
  letter-spacing: -0.8px;
  opacity: 0.6;
}
.code-tabs .el-tabs--card>.el-tabs__header .el-tabs__item {
  border-left: none;
  border-right: 1px solid;
  border-bottom: none;
  border-color: #232323;
}
.code-tabs .el-tabs__item.is-active {
  color: white;
  background-color: #232323;
  opacity: 1.0;
}
.code-tabs .el-tabs--card>.el-tabs__header .el-tabs__item {
  color: #CCCCCC;
}
.code-tabs .el-tabs--card>.el-tabs__header .el-tabs__item.is-active .is-icon-close {
  background-color: #232323;
}
.code-tabs .el-tabs--card>.el-tabs__header .el-tabs__item .is-icon-close {
  right: -10px;
  background: #404041;
}
.code-tabs .el-tabs__nav-prev {
  margin-top: -6px;
  margin-left: 4px;
}
.code-tabs .el-tabs__nav-prev.is-disabled .el-icon {
  color: #232323;
}
.code-tabs .el-tabs__nav-next {
  margin-top: -6px;
  margin-right: 8px;
}
.code-tabs .el-tabs__nav-next.is-disabled .el-icon {
  color: #232323;
}
</style>

<style scoped>
.node-icon {
  width: 12px;
  height:12px;
}
.node-label {
  /* color:#A6A6A6; */
  letter-spacing: -0.8px;
  font-family: 'Gotham-Book';
  padding-left: 2px;
  color: white;
}
.file-path {
  /* color: lightblue; */
  font-size: 12px;
  /* background-color: rgba(255, 250, 226, 1.0); */
  width: 100%;
  background: #2E3032;
  color: #CCCCCC;
  font-family: 'Gotham-Book';
  /* margin-top: -5px; */
  padding-top: 1px;
}
</style>
