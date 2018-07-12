<template>
  <div>
    <el-tree
      id="tree-root"
      class="ide-project-list noselected"
      :data="[model.ideModel.curProjTree]"
      node-key="uuid"
      ref="tree"
      highlight-current
      :default-expanded-keys="model.ideModel.curProjExpandedKeys"
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
      if (this.getFile === true) {
        this.model.ideModel.getFile(data.path);
      }
      this.getFile = true;
    },
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
    }
  }
}
</script>
<style>
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


