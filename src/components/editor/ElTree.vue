<template>
  <div>
    <el-tree
      id="tree-root"
      class="ide-project-list noselected"
      :data="[model.ideModel.curProjTree]"
      node-key="uuid"
      ref="tree"
      highlight-current
      :expand-on-click-node="false"
      :indent=12
      :render-content="renderContent"
      :default-expanded-keys="curProjExpandedKeys"
      @node-expand="nodeExpand"
      @node-collapse="nodeCollapse"
      @node-click="handleNodeClick"
      >
    </el-tree>
  </div>
</template>

<script>
import * as types from '../../store/mutation-types';

export default {
  data() {
    return {
      model: window.GlobalUtil.model,
      getFile: true,
      fileIcon: {
        py: require('@/assets/img/ide/language_python.svg'),
        doc: require('@/assets/img/ide/icon_documents.svg'),
        md: require('@/assets/img/ide/icon_md.svg'),
        folder: require('@/assets/img/ide/icon_folder.svg'),
        openfolder: require('@/assets/img/ide/icon_openfolder.svg'),
      },
    }
  },
  defaultProps: {
    children: 'children',
    label: 'label',
    uuid: 'uuid',
  },
  methods: {
    increaseCounter() {
      this.$store.commit(types.INCRESE_COUNTER);
    },
    nodeExpand(data) {
      this.getFile = false;
      this.model.ideModel.curProjAddExpandedKeys(data.uuid);
    },
    nodeCollapse(data) {
      this.getFile = false;
      this.model.ideModel.curProjRemoveExpandedKeys(data.uuid);
    },
    handleNodeClick(data) {
      this.model.ideModel.selectNode = data;
      if (this.getFile === true && data.type === 'file') {
        this.model.ideModel.getFile(data.path);
      }
      this.getFile = true;
    },
    renderContent(h, { node, data, store }) {
      let textColorStyle = data !== null && this.model.ideModel.selectFilePath === data.path && data.type === 'file' ? 'color:#4F7597;' : 'color:#A6A6A6;';
      textColorStyle = `${textColorStyle}font-family:'Gotham-Book';letter-spacing:-0.8px;padding-left:20px;`;
      let url = '';
      if (data.type === 'file') {
        if (data.path.indexOf('.py') >= 0) {
          url = this.fileIcon.py;
        }
        else if (data.path.indexOf('.md') >= 0) {
          url = this.fileIcon.md;
        }
        else {
          url = this.fileIcon.doc;
        }
      }
      else if (data.type === 'dir' || data.type === 'folder') {
        url = this.fileIcon.folder;
        if (this.model.ideModel.curProjExpandedKeys.includes(data.path)) {
          url = this.fileIcon.openfolder;
        }
      }
      const urlstyle = `background:url('${url}') no-repeat center left;${textColorStyle}`;
      return (
          <span class="">
            <span style={urlstyle}>
              { data.label }
            </span>
          </span>
      );
    }
  },
  mounted() {
    this.model.ideModel.projElTree = this.$refs.tree;
    const self = this;
    setTimeout(() => {
      self.$refs.tree.setCurrentKey('/');
      if (self.$refs.tree.getCurrentNode() !== null) {
        self.model.ideModel.selectNode = self.$refs.tree.getCurrentNode();
      };
      setTimeout(() => {
        if (self.model.ideModel.selectFilePath !== null) {
          self.$refs.tree.setCurrentKey(self.model.ideModel.selectFilePath);
          if (self.$refs.tree.getCurrentNode() !== null) {
            self.model.ideModel.selectNode = self.$refs.tree.getCurrentNode();
          };
        }
      }, 200);
    }, 300);
  },
  watch: {
    'model.ideModel.selectFilePath': {
      handler(cur, old) {
        const self = this;
        setTimeout(() => {
          if (self.model.ideModel.selectFilePath !== null) {
            self.$refs.tree.setCurrentKey(self.model.ideModel.selectFilePath);
          }
        }, 100);
      }
    }
  },
  computed: {
    counter () {
      return this.$store.state.model.counter
    },
    curProjExpandedKeys() {
      if (this.model.ideModel.curProjExpandedKeys !== undefined) {
        this.model.ideModel.curProjExpandedKeys.sort();
        const curProjExpandedKeys = []
        for (let i = 0; i < this.model.ideModel.curProjExpandedKeys.length; i++) {
          let prefix = '';
          const tmp = this.model.ideModel.curProjExpandedKeys[i].split('/');
          let flag = true;
          for (let j = 0; j < tmp.length; j++) {
            if (tmp[j]) {
              prefix += '/' + tmp[j]
              if (this.model.ideModel.curProjExpandedKeys.indexOf(prefix) < 0) {
                flag = false;
                break;
              }
            }
            else {
              if (this.model.ideModel.curProjExpandedKeys.indexOf('/') < 0) {
                flag = false;
                break;
              }
            }
          }
          if (flag) {
            if (curProjExpandedKeys.indexOf(this.model.ideModel.curProjExpandedKeys[i]) < 0) {
              curProjExpandedKeys.push(this.model.ideModel.curProjExpandedKeys[i]);
            }
          }
        };
        return curProjExpandedKeys;
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
  /* width:80px;
  height: 500px; */
}
.el-tree {
  /* min-width: 100%; */
  display:inline-block !important;
}

.tree::-webkit-scrollbar {/*滚动条整体样式*/
  width: 4px;     /*高宽分别对应横竖滚动条的尺寸*/
  height: 4px;
}
.tree::-webkit-scrollbar-thumb {/*滚动条里面小方块*/
  background: #87939A;
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
  background-color: rgb(26, 37, 51);
}
.ide-project-list .el-tree-node__content:hover {
  /* 鼠标在节点上面的样式 */
  background-color: #272c35;
}
.ide-project-list .el-tree-node:focus>.el-tree-node__content {
  /* 选中有子节点的节点样式 */
  background-color: rgb(26, 37, 51);
}
.ide-project-list .el-tree-node.is-current>.el-tree-node__content .display-none {
  display: inline-block;
}
</style>

<style scoped>
.ide-project-list {
  background: #2E3032;
  padding-left: 10px;
  /* color: white; */
}
/* .ide-project-list:selected {
  background: blue;
} */
.ide-project-list:hover {
  color: red;
}
.ide-project-list .el-tree-node__content {
  /* height: 36px; */
}
.ide-project-list .el-tree-node.is-expanded>.el-tree-node__children {
  /* background: #E8E8E8; */
}
.ide-project-list .el-tree-node.is-current>.el-tree-node__content {
  /* background-color: #575C62;
  color: #fff; */
}
.ide-project-list .el-tree-node.is-current>.el-tree-node__content .display-none {
  /* display: inline-block; */
}
</style>


