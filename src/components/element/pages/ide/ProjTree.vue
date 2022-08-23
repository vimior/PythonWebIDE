<template>
  <div>
    <el-tree
      id="tree-root"
      class="ide-project-list noselected"
      :props="treeProps"
      :data="[ideInfo.currProj.data]"
      node-key="uuid"
      ref="tree"
      highlight-current
      :expand-on-click-node="false"
      :indent=12
      :default-expanded-keys="defaultExpandedKeys"
      @node-expand="nodeExpand"
      @node-collapse="nodeCollapse"
      @node-click="handleNodeClick"
      >
      <template #default="{ node, data }">
        <span>
          <img :src="getIconUrl(data)" alt="" class="node-icon" />
          <span class="node-label">{{ node.label }}</span>
        </span>
      </template>
    </el-tree>
  </div>
</template>

<script>
import * as types from '../../../../store/mutation-types';
import { getIconForFile, getIconForFolder, getIconForOpenFolder } from 'vscode-icons-js';

export default {
  data() {
    return {
      getFile: true,
      treeProps: {
        uuid: 'uuid',
        label: 'label',
        children: 'children',
      },
    }
  },
  methods: {
    getIconUrl(data) {
      if (data.type === 'file') {
        return require(`@/assets/vscode-icons/${getIconForFile(data.path.substring(data.path.lastIndexOf('.') + 1))}`);
      }
      else if (data.type === 'dir' || data.type === 'folder') {
        if (this.expandedKeys.includes(data.path)) {
          return require(`@/assets/vscode-icons/${getIconForOpenFolder(data.label)}`);
        }
        else {
          return require(`@/assets/vscode-icons/${getIconForFolder(data.label)}`);
        }
      }
    },
    nodeExpand(data) {
      this.getFile = false;
      this.$store.commit('ide/addExpandNodeKey', data.uuid);
      this.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
    },
    nodeCollapse(data) {
      this.getFile = false;
      this.$store.commit('ide/delExpandNodeKey', data.uuid);
      this.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
    },
    handleNodeClick(data) {
      this.$store.commit('ide/setNodeSelected', data);
      if (data.type === 'file')
        this.$emit('get-item', data.path);
      // if (this.getFile === true && data.type === 'file') {
      //   this.$emit('get-item', data.path);
      // }
      // this.getFile = true;
    },
  },
  mounted() {
    this.$store.commit('ide/setTreeRef', this.$refs.tree);
    const self = this;
    setTimeout(() => {
      if (!self.ideInfo.treeRef) return;
      self.ideInfo.treeRef.setCurrentKey('/');
      if (self.ideInfo.treeRef.getCurrentNode() !== null) {
        self.$store.commit('ide/setNodeSelected', self.ideInfo.treeRef.getCurrentNode());
      }
      setTimeout(() => {
        if (self.ideInfo.currProj.pathSelected !== null) {
          self.ideInfo.treeRef.setCurrentKey(self.ideInfo.currProj.pathSelected);
          if (self.ideInfo.treeRef.getCurrentNode() !== null) {
            self.$store.commit('ide/setNodeSelected', self.ideInfo.treeRef.getCurrentNode());
          }
        }
      }, 200);
    }, 300);
  },
  watch: {
    'ideInfo.currProj.pathSelected': {
      handler(cur, old) {
        const self = this;
        setTimeout(() => {
          if (self.ideInfo.currProj.pathSelected) {
            self.ideInfo.treeRef.setCurrentKey(self.ideInfo.currProj.pathSelected);
            // self.$store.commit('ide/setNodeSelected', self.ideInfo.currProj.pathSelected);
          }
        }, 100);
      }
    },
  },
  computed: {
    ideInfo() {
      return this.$store.state.ide.ideInfo;
    },
    expandedKeys() {
      return this.ideInfo ? this.ideInfo.currProj.expandedKeys : [];
    },
    defaultExpandedKeys() {
      if (this.expandedKeys !== undefined) {
        const expandedKeys = []
        for (let i = 0; i < this.expandedKeys.length; i++) {
          let prefix = '';
          const tmp = this.expandedKeys[i].split('/');
          let flag = true;
          for (let j = 0; j < tmp.length; j++) {
            if (tmp[j]) {
              prefix += '/' + tmp[j]
              if (this.expandedKeys.indexOf(prefix) < 0) {
                flag = false;
                break;
              }
            }
            else {
              if (this.expandedKeys.indexOf('/') < 0) {
                flag = false;
                break;
              }
            }
          }
          if (flag) {
            if (expandedKeys.indexOf(this.expandedKeys[i]) < 0) {
              expandedKeys.push(this.expandedKeys[i]);
            }
          }
        }
        return expandedKeys;
      }
      else {
        return [];
      }
    }
  }
}
</script>
<style>
.tree {
  overflow-y: auto;
  overflow-x: auto;
}
.el-tree {
  /* min-width: 100%; */
  display: inline-block !important;
  min-width: 200px;
}

.tree::-webkit-scrollbar {/*滚动条整体样式*/
  width: 5px;     /*高宽分别对应横竖滚动条的尺寸*/
  height: 5px;
}
.tree::-webkit-scrollbar-thumb {/*滚动条里面小方块*/
  /* background: #87939A; */
  background: #545a5e;
}
.tree::-webkit-scrollbar-track {/*滚动条里面轨道*/
  background: #2F2F2F;
}
.ide-project-list .el-tree-node__content {
  /* height: 56px; */
  color: white;
}
.ide-project-list .el-tree-node.is-expanded>.el-tree-node__children {
  color: white;
}
.ide-project-list .el-tree-node.is-current>.el-tree-node__content {
  /*  选中没有子节点的节点的样式 */
  background-color: #383B3D;
}
.ide-project-list .el-tree-node__content:hover {
  /* 鼠标在节点上面的样式 */
  background-color: #383B3D;
}
.ide-project-list .el-tree-node:focus>.el-tree-node__content {
  /* 选中有子节点的节点样式 */
  /* background-color: rgb(26, 37, 51); */
  background: #383B3D;
  /* color: #FFF; */
}
.ide-project-list .el-tree-node.is-current>.el-tree-node__content .display-none {
  display: inline-block;
}
</style>

<style scoped>
.ide-project-list {
  background: #282828;
  color: #CCCCCC;
  /* padding-left: 10px; */
  /* padding-right: 10px; */
}
.node-icon {
  width: 15px;
  height:15px;
}
.node-label {
  color:#A6A6A6;
  letter-spacing: -0.8px;
  font-family: 'Gotham-Book';
  padding-left: 2px;
}
</style>


