<template>
  <div class="noselected console-tabs">
    <el-tabs
      v-model="pathSelected"
      type="card"
      closable
      @tab-remove="removeTab"
      @tab-click="selectTab"
    >
      <el-tab-pane
        v-for="item in consoleItems"
        :key="item.path + '-|-' + item.id"
        :label="item.name"
        :name="item.path + '-|-' + item.id"
      >
        <template #label>
          <img :src="getIconUrl(item.path)" alt="" class="node-icon" />
          <span class="node-label">{{ getItemPath(item) }}</span>
        </template>
        <!-- <span class="file-path">{{ getItemPath(item) }}</span> -->
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
    getItemPath(item) {
      return this.ideInfo.consoleSelected.path === item.path && this.ideInfo.consoleSelected.id === item.id && !(this.ideInfo.consoleSelected.name === 'Terminal' && this.ideInfo.consoleSelected.path === 'Terminal') ? '/' + this.ideInfo.currProj.data.name + item.path : item.name;
    },
    getIconUrl(path) {
      return require(`@/assets/vscode-icons/${getIconForFile(path.substring(path.lastIndexOf('.') + 1))}`);
    },
    getItem(path_id) {
      if (!path_id) return;
      const tmp = path_id.split('-|-');
      tmp[1] = Number(tmp[1]);
      for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
        if (this.ideInfo.consoleItems[i].path === tmp[0] && this.ideInfo.consoleItems[i].id === tmp[1]) {
          return this.ideInfo.consoleItems[i];
        }
      }
      return '';
    },
    selectTab(path) {
      // console.log('+======', path);
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
    consoleItems() {
      return this.ideInfo.consoleItems;
    },
    pathSelected: {
      get() {
        return this.ideInfo.consoleSelected.path + '-|-' + this.ideInfo.consoleSelected.id;
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
.console-tabs .el-tabs {
  --el-tabs-header-height: 25px;
}
.console-tabs .el-tabs__nav-wrap {
  background: #3A3D41;
  /* margin-top: -15px; */
  margin-top: -3px;
  height: 20px;
}
.console-tabs .el-tabs--card>.el-tabs__header .el-tabs__nav {
  border: none;
  background: #3A3D41;
  border-radius: 0px;
  height: 20px;
}
.console-tabs .el-tabs--card>.el-tabs__header {
  border-color: #3A3D41;
  background: #3A3D41;
  height: 20px;
}
.console-tabs .el-tabs__content {
  /* margin-top: -10px; */
}
.console-tabs .el-tabs__item {
  height: 20px;
  padding-left: 10px;
  padding-right: 3px;
  line-height: 20px;
  font-size: 12px;
  font-weight: 500;
  font-family: 'Gotham-Book';
  color: #CCCCCC;
  letter-spacing: -0.8px;
  opacity: 0.6;
}
.console-tabs .el-tabs--card>.el-tabs__header .el-tabs__item {
  border-left: none;
  border-right: 1px solid;
  border-bottom: none;
  border-color: #232323;
  height: 20px;
}
.console-tabs .el-tabs__item.is-active {
  color: white;
  /* background-color: #232323; */
  background-color: #666c71;
  opacity: 1.0;
}
.console-tabs .el-tabs--card>.el-tabs__header .el-tabs__item {
  color: #CCCCCC;
  height: 20px;
}
.console-tabs .el-tabs--card>.el-tabs__header .el-tabs__item.is-active .is-icon-close {
  /* background-color: #232323; */
  background-color: #666c71;
}
.console-tabs .el-tabs--card>.el-tabs__header .el-tabs__item .is-icon-close {
  right: -10px;
  background: #404041;
}
.console-tabs .el-tabs__nav-prev {
  margin-top: -10px;
  margin-left: 2px;
}
.console-tabs .el-tabs__nav-prev.is-disabled .el-icon {
  color: #232323;
}
.console-tabs .el-tabs__nav-next {
  margin-top: -10px;
  margin-right: 6px;
}
.console-tabs .el-tabs__nav-next.is-disabled .el-icon {
  color: #232323;
}
</style>

<style scoped>
.console-tabs {
  padding-left: 20px;
  background-color: #3A3D41;
  height: 20px;
}
.node-icon {
  width: 12px;
  height: 12px;
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
  /* padding-top: 1px; */
}
.run-icon {
  margin-right: 10px;
  margin-top: -1px;
  width: 16px;
  height: 16px;
  background-image: url('./../../../../assets/img/ide/icon_running.svg');
  cursor: pointer;
}
.stop-icon {
  margin-right: 10px;
  margin-top: -1px;
  width: 16px;
  height: 16px;
  background-image: url('./../../../../assets/img/ide/icon_stop.svg');
  cursor: pointer;
}
</style>
