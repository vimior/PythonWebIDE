<template>
  <div class="dialog-wrap">
    <div class="dialog-cover" @click="closeMyself"></div>
    <div class="dialog-content">
      <div class="dialog-top">
        <span class="proj-top-title">{{ $t('title') }}</span>
        <div class="dialog-close" @click="closeMyself">
        </div>
      </div>
      <table>
        <tr>
          <th class="dialog-table-head">{{ $t('projectName') }}</th>
          <th class="dialog-table-head">{{ $t('date') }}</th>
          <th class="dialog-table-head">{{ $t('option') }}</th>
        </tr>
      </table>
      <div class="dialog-table">
        <table>
          <template v-for="data in model.ideModel.projList">
            <tr @dblclick="onSelect(data.name)" :key="data.name">
              <td>{{ data.name }}</td>
              <td>{{ data.ctime }}</td>
              <td>
                <div class="float-left proj-selected" v-if="model.ideModel.curProjTree.name === data.name"></div>
                <div class="float-left proj-open" v-if="model.ideModel.curProjTree.name !== data.name" @click="onSelect(data.name)">Open</div>
                <!-- btn_trash.svg -->
                <div class="proj-icon-trash float-left" v-if="model.ideModel.curProjTree.name !== data.name" @click="onDelete(data.name)"></div>
              </td>
            </tr>
          </template>
        </table>
      </div>
      <div class="dialog-add">
        <div class="dialog-add-content" @click="addProj()">
          <span>+</span>
          <span>{{ $t('newProject') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const path = require('path');

export default {
  i18n: {
    messages: {
      en: {
        title: 'Select a Project',
        projectName: 'Project name',
        date: 'Date',
        type: 'Type',
        Delete: 'Delete',
        option: 'Option',
        newProject: 'New Project',
      },
      cn: {
        title: '请选择一个项目',
        projectName: '',
        date: '时间',
        type: '类型',
        Delete: '删除',
        option: 'Option',
        newProject: '新建项目',
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
      this.model.ideModel.showFileDialog = false;
      this.model.ideModel.showProjsDialog = false;
      this.model.ideModel.showDeleteDialog = false;
      if (this.model.ideModel.selectNode !== null) {
        this.model.ideModel.projElTree.setCurrentNode(this.model.ideModel.selectNode);
      }
    },
    addProj() {
      this.model.ideModel.dialogType = 'create-project';
      this.model.ideModel.dialogTitle = 'New project name';
      this.model.ideModel.dialogInputText = '';
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showFileDialog = true;
      // setTimeout(() => {
      //   document.getElementById('input-text').focus();
      // });
      // window.GlobalUtil.setInputFocus();
    },
    onSelect(projectName) {
      if (this.hasRunProgram()) {
        this.$confirm('Are you stop all program and select other project?', 'Warning', {
          confirmButtonText: 'Stop and select',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }).then(() => {
          this.stopAll();
          this.model.ideModel.consoleItems = [];
          console.log('select', projectName);
          this.model.ideModel.getProject(projectName)
          this.model.ideModel.showProjsDialog = false;
        }).catch(() => {
          console.log('canceled select project');
          this.model.ideModel.showProjsDialog = false;
        })
      }
      else {
        this.model.ideModel.consoleItems = [];
        console.log('select', projectName);
        this.model.ideModel.getProject(projectName)
        this.model.ideModel.showProjsDialog = false;
      }
    },
    onDelete(projectName) {
      console.log('delete', projectName);
      this.model.ideModel.deleteProject(projectName)
    },
    hasRunProgram() {
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === true) {
          return true;
        }
      }
      return false;
    },
    stopAll() {
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === true) {
          this.model.ideModel.stopPythonProgram(this.model.ideModel.consoleItems[i].id);
        }
      }
    },
  },
}
</script>

<style scoped>
.proj-top-title {
  position: absolute;
  left: 24px;
  top: 25px;
  /* height: 67px; */
  font-family: 'Gotham-Medium';
  font-size: 16px;
  color: #FFFFFF;
  letter-spacing: -1px;
  /* background-color: yellow; */
  /* line-height: 16px; */
}
.dialog-content {
  width: 580px;
  position: fixed;
  height: 340px;
  top: 20%;
  left: 0px;
  right: 0px;
  margin-left:auto;
  margin-right:auto;
  z-index: 10;
  background: #303030;
  overflow: hidden;
}
.dialog-top {
  width: 100%;
  height: 67px;
  background: #3F4955;
}
.dialog-table {
  /* width: 100%; */
  width: 600px;
  height: 140px;
  overflow-y: scroll;
}
.dialog-table-head {
  width: 194px;
  height: 66px;
  /* font-family: 'Gotham-Medium'; */
  font-size: 16px;
  color: #FFFFFF;
  letter-spacing: -1px;
  text-align: center;
  line-height: 16px;
}
.dialog-table td {
  width: 194px;
  height: 40px;
  /* font-family: 'Gotham-Book'; */
  font-size: 12px;
  color: #FFFFFF;
  padding-left: 50px;
  letter-spacing: -0.38px;
  /* text-align: center; */
  line-height: 12px;
}
.dialog-table tr:hover {
  background: rgba(255, 255, 255, 0.1);
}
.dialog-table tr:hover td {
  /* color: black; */
  font-size: 13px;
}
.dialog-close {
  position: absolute;
  right: 10px;
  top: 25px;
  width: 20px;
  height: 20px;
  text-align: center;
  cursor: pointer;
  background-position: center;
  background-image: url('./../../../assets/img/pop/icon_close.svg');
  background-size: 10px 11px;
  background-repeat: no-repeat;
}
.dialog-close:hover {
  color: #4fc08d;
}
.dialog-add {
  width: 100%;
  height: 100px;
  /* background-color: yellow; */

}
.dialog-add-content {
  position: absolute;
  bottom: 16px;
  left: 0;
  right: 0;
  margin: auto;
  /* background-color: yellow; */
  width: 496px;
  height: 26px;
  font-family: 'Gotham-Book';
  text-align: center;
  line-height: 10px;
  letter-spacing: -0.5px;
  color: #FFFFFF;
  padding-top: 8px;
  border:1px dashed #5C5C5C;
  cursor: pointer;
}
.proj-icon-trash {
  margin-left: 20px;
  width: 30px;
  height: 30px;
  background-image: url('./../../../assets/img/pop/btn_trash.svg');
  background-size: 8px 10px;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
}
.proj-open {
  font-family: 'Gotham-Book';
  font-size: 12px;
  color: #FFFFFF;
  letter-spacing: -0.38px;
  line-height: 26px;
  height: 26px;
  margin-left: 10px;
  cursor: pointer;
}
.proj-selected {
  width: 30px;
  height: 30px;
  margin-left: 10px;
  background-image: url('./../../../assets/img/pop/icon_select.svg');
  background-size: 16px 16px;
  background-repeat: no-repeat;
  background-position: center;
}
</style>
