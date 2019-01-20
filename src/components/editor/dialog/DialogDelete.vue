
<template>
  <div id="root-delete" class="noselected">
    <div class="dialog-wrap">
      <div class="dialog-cover" @click="closeMyself"></div>
      <div class="dialog-content">
        <span class="top-title">{{ model.ideModel.dialogTitle }}</span>
        <div style="margin-top:156px;">
          <div class="float-left btn-cancel" @click="closeMyself">
            {{ $t('cancel') }}
          </div>
          <div class="float-left btn-delete cursor-pointer" @click="ondelete">
            {{ $t('delete') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// const path = require('path')
export default {
  i18n: {
    messages: {
      en: {
        cancel: 'Cancel',
        delete: 'Delete',
      },
      cn: {
        cancel: '关闭',
        delete: '删除',
      },
    },
  },
  data() {
    return {
      model: window.GlobalUtil.model,
    }
  },
  methods: {
    closeMyself() {
      this.model.ideModel.showDeleteDialog = false;
      if (this.model.ideModel.selectNode !== null) {
        this.model.ideModel.projElTree.setCurrentNode(this.model.ideModel.selectNode);
      }
    },
    ondelete() {
      this.model.ideModel.showDeleteDialog = false;
      if (this.model.ideModel.selectNode === null || this.model.ideModel.selectNode === undefined) {
        this.model.ideModel.deleteFolder(this.model.ideModel.selectNode.path);
        this.model.ideModel.deleteFile(this.model.ideModel.selectNode.path);
      }
      else {
        if (this.model.ideModel.selectNode.type === 'dir') {
          this.model.ideModel.deleteFolder(this.model.ideModel.selectNode.path);
        }
        else {
          this.model.ideModel.deleteFile(this.model.ideModel.selectNode.path);
        }
      }
    },
  },
  components: {
  },
  mounted() {
  },
  computed: {
  },
}
</script>

<style scoped>
.top-title {
  position: absolute;
  left: 130px;
  top: 70px;
  text-align: center;
  /* height: 67px; */
  font-family: 'Gotham-Medium';
  font-size: 16px;
  color: #FFFFFF;
  letter-spacing: -1px;
  /* background-color: yellow; */
  /* line-height: 16px; */
}
.dialog-content {
  width: 356px;
  position: fixed;
  height: 196px;
  top: 20%;
  left: 0px;
  right: 0px;
  margin-left:auto;
  margin-right:auto;
  z-index: 10;
  background: #303030;
  overflow: hidden;
}
.dialog-close:hover {
  color: #4fc08d;
}
.dialog-add {
  width: 100%;
  height: 100px;
  /* background-color: yellow; */
}
.btn-cancel {
  width: 178px;
  height: 40px;
  /* margin-top: 230px; */
  /* background-color: yellow; */
  background: #484848;
  text-align: center;
  font-family: 'Gotham-Book';
  font-size: 14px;
  color: #7B7B7B;
  letter-spacing: -0.88px;
  line-height: 40px;
  cursor: pointer;
}
.btn-delete {
  width: 178px;
  height: 40px;
  /* margin-top: 230px; */
  /* margin-left: 178px; */
  /* background-color: green; */
  background: #E24D4A;
  text-align: center;
  font-family: 'Gotham-Book';
  font-size: 14px;
  color: #FFFFFF;
  letter-spacing: -0.88px;
  line-height: 40px;
  /* cursor: pointer; */
}
</style>
