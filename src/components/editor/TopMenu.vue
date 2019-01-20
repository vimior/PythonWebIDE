<template>
  <div>
    <div class="project-icon float-left" @click="listProjects()" :title="$t('projectList')"></div>
    <div v-if="model.ideModel.selectNode !== null && model.ideModel.selectNode.type === 'dir'" class="file-icon float-left" @click="newFile()" :title="$t('createFile')"></div>
    <div v-else class="file-icon float-left" :title="$t('createFile')" style="opacity:0.3"></div>
    <div v-if="model.ideModel.selectNode !== null && model.ideModel.selectNode.type === 'dir'" class="folder-icon float-left" @click="newFolder()" :title="$t('createFolder')"></div>
    <div v-else class="folder-icon float-left" :title="$t('createFolder')" style="opacity:0.3"></div>
    <div v-if="model.ideModel.selectNode !== null" class="rename-icon float-left" @click="rename()" :title="$t('rename')"></div>
    <div v-else class="rename-icon float-left" :title="$t('rename')" style="opacity:0.3"></div>
    <div v-if="model.ideModel.selectNode !== null && model.ideModel.selectNode.path !== '/'" class="del-icon float-left" @click="delFile()" :title="$t('delete')"></div>
    <div v-else class="del-icon float-left" :title="$t('delete')" style="opacity:0.3"></div>
    <div class="status-icon float-left" :title="$t('status')" :class="{'el-icon-circle-check': model.socketModel.socketInfo.connected, 'el-icon-circle-close': !model.socketModel.socketInfo.connected}" :style="{color: model.socketModel.socketInfo.connected ? '#52bf53' : '#e15960'}"></div>
    <span>
      <div class="float-right stop-icon" @click="stopAll()" v-if="hasRunProgram" :title="$t('stopAll')"></div>
      <!-- <div class="float-right stop-icon-disabled" v-if="!hasRunProgram" :title="$t('stopAll')"></div> -->
    </span>
    <span>
      <div class="run-icon float-right" v-if="isPythonFile && !consoleLimit" @click="run()" :title="$t('run')"></div>
      <div class="run-icon-disabled float-right" v-if="!isPythonFile && !consoleLimit" :title="$t('canNotRun')"></div>
    </span>
  </div>
</template>

<script>
const path = require('path');

export default {
  i18n: {
    messages: {
      en: {
        projectList: 'Projects',
        createFile: 'New file',
        createFolder: 'New folder',
        renameProj: 'Rename project',
        renameFolder: 'Rename folder',
        renameFile: 'Rename file',
        rename: 'Rename',
        delete: 'Delete',
        status: 'Status',
        run: 'Run the currently selected script',
        stopAll: 'Stop all running scripts',
        canNotRun: 'Unable to run, the currently selected file is not a python file',
      },
      cn: {
        projectList: '工程列表',
        createFile: '新建文件',
        createFolder: '新建文件夹',
        renameProj: '重命名工程',
        renameFolder: '重命名文件夹',
        renameFile: '重命名文件',
        rename: '重命名',
        delete: '删除',
        status: '状态',
        run: '运行当前选中的脚本',
        stopAll: '停止所有运行的脚本',
        canNotRun: '无法运行，当前选中的文件不是python文件',
      },
    },
  },
  data() {
    return {
      model: window.GlobalUtil.model,
      isRun: true,
    }
  },
  computed: {
    hasRunProgram() {
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === true) {
          return true;
        }
      }
      return false;
    },
    isPythonFile() {
      return this.model.ideModel.selectFilePath !== null && this.model.ideModel.codeItems.length > 0 && this.model.ideModel.selectFilePath.lastIndexOf('.py') === this.model.ideModel.selectFilePath.length - 3
    },
    consoleLimit() {
      let count = 0;
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === true && !(this.model.ideModel.consoleItems[i].name === 'Terminal' && this.model.ideModel.consoleItems[i].path === 'Terminal')) {
          count += 1;
        }
      }
      return count >= 3;
    }
  },
  methods: {
    listProjects() {
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showProjsDialog = true;
    },
    newFile() {
      this.model.ideModel.dialogType = 'create-file';
      this.model.ideModel.dialogTitle = this.$t('createFile');
      this.model.ideModel.dialogInputText = '';
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showFileDialog = true;
    },
    newFolder() {
      this.model.ideModel.dialogType = 'create-folder';
      this.model.ideModel.dialogTitle = this.$t('createFolder');
      this.model.ideModel.dialogInputText = '';
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showFileDialog = true;
    },
    rename() {
      if (this.model.ideModel.selectNode.path === '/') {
        this.model.ideModel.dialogType = 'rename-project';
        this.model.ideModel.dialogTitle = `${this.$t('renameProj')} (${this.model.ideModel.curProjTree.name})`
        this.model.ideModel.dialogInputText = `${this.model.ideModel.curProjTree.name}`;
      }
      else if (this.model.ideModel.selectNode.type === 'dir') {
        const name = path.basename(this.model.ideModel.selectNode.path);
        this.model.ideModel.dialogType = 'rename-folder';
        this.model.ideModel.dialogTitle = `${this.$t('renameFolder')} (${this.model.ideModel.selectNode.path})`
        this.model.ideModel.dialogInputText = `${name}`;
      }
      else {
        const name = path.basename(this.model.ideModel.selectFilePath);
        this.model.ideModel.dialogType = 'rename-file';
        this.model.ideModel.dialogTitle = `${this.$t('renameFile')} (${this.model.ideModel.selectFilePath})`
        this.model.ideModel.dialogInputText = `${name}`;
      }
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showFileDialog = true;
    },
    delFile() {
      const name = path.basename(this.model.ideModel.selectNode.path);
      this.model.ideModel.dialogTitle = `${this.$t('delete')} ${name}?`;
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showDeleteDialog = true;
    },
    run() {
      let selected = false;
      if (this.model.ideModel.selectConsoleItem.run === false && this.model.ideModel.selectConsoleItem.path === this.model.ideModel.selectFilePath) {
        selected = true;
        this.model.ideModel.selectConsoleItem.output = '';
        this.model.ideModel.selectConsoleItem.resultList = [];
      }
      else {
        for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
          if (this.model.ideModel.consoleItems[i].run === false && this.model.ideModel.consoleItems[i].path === this.model.ideModel.selectFilePath) {
            this.model.ideModel.selectConsoleItem = this.model.ideModel.consoleItems[i];
            selected = true;
            this.model.ideModel.selectConsoleItem.output = '';
            this.model.ideModel.selectConsoleItem.resultList = [];
            break;
          }
        }
      }
      if (selected === false) {
        for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
          if (this.model.ideModel.consoleItems[i].run === false && !(this.model.ideModel.consoleItems[i].name === 'Terminal' && this.model.ideModel.consoleItems[i].path === 'Terminal')) {
            this.model.ideModel.consoleItems.splice(i, 1);
            break;
          }
        }
        const item = {
          name: path.basename(this.model.ideModel.selectFilePath),
          path: this.model.ideModel.selectFilePath,
          output: '',
          run: false,
          id: this.model.ideModel.consoleId,
        }
        this.model.ideModel.consoleItems.push(item)
        this.model.ideModel.selectConsoleItem = item;
      }
      else {
        this.model.ideModel.selectConsoleItem.id = this.model.ideModel.consoleId;
      }
      // for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
      //   if (this.model.ideModel.consoleItems[i].run === false && !(this.model.ideModel.consoleItems[i].name === 'Terminal' && this.model.ideModel.consoleItems[i].path === 'Terminal')) {
      //     this.model.ideModel.consoleItems.splice(i, 1)
      //     break;
      //   }
      // }
      // const item = {
      //   name: path.basename(this.model.ideModel.selectFilePath),
      //   path: this.model.ideModel.selectFilePath,
      //   output: '',
      //   run: false,
      //   id: this.model.ideModel.consoleId,
      // }
      // this.model.ideModel.consoleItems.push(item)
      // this.model.ideModel.selectConsoleItem = item;
      if (!this.model.ideModel.consoleItems.includes(this.model.ideModel.selectConsoleItem)) {
        this.model.ideModel.consoleItems.push(this.model.ideModel.selectConsoleItem)
      }
      this.model.ideModel.runPythonProgram(this.model.ideModel.consoleId, this.model.ideModel.selectFilePath);
      this.model.ideModel.consoleId = this.model.ideModel.consoleId + 1;
    },
    stopAll() {
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === true) {
          this.model.ideModel.stopPythonProgram(this.model.ideModel.consoleItems[i].id);
        }
      }
      this.model.ideModel.stopPythonProgram(null);
    }
  }
}
</script>

<style scoped>
.project-icon {
  margin-left: 17px;
  margin-top: 13px;
  width: 24px;
  height: 24px;
  background-image: url('./../../assets/img/ide/btn_addproject.svg');
  background-size: 13px 11px;
  background-repeat: no-repeat;
  cursor: pointer;
}
.folder-icon {
  margin-left: 20px;
  margin-top: 6px;
  width: 24px;
  height: 24px;
  background-image: url('./../../assets/img/ide/btn_addfolder.svg');
  cursor: pointer;
}
.file-icon {
  margin-left: 10px;
  margin-top: 6px;
  width: 24px;
  height: 24px;
  background-image: url('./../../assets/img/ide/icon_addfile.svg');
  cursor: pointer;
}
.rename-icon {
  margin-left: 20px;
  margin-top: 6px;
  width: 24px;
  height: 24px;
  background-image: url('./../../assets/img/ide/btn_rename.svg');
  /* cursor: pointer; */
}
.del-icon {
  margin-left: 20px;
  margin-top: 6px;
  width: 24px;
  height: 24px;
  background-image: url('./../../assets/img/ide/btn_trash.svg');
  /* cursor: pointer; */
}
.status-icon {
  margin-left: 20px;
  margin-top: 12px;
  width: 24px;
  height: 24px;
  color: '#52bf53';
}
.stop-icon {
  margin-right: 20px;
  margin-top: 10px;
  width: 16px;
  height: 16px;
  color: #656666;
  background-image: url('./../../assets/img/ide/icon_stop.svg');
  cursor: pointer;
}
.stop-icon-disabled {
  margin-right: 20px;
  margin-top: 10px;
  width: 16px;
  height: 16px;
  background-image: url('./../../assets/img/ide/icon_stop_gray.svg');
  cursor: pointer;
}
.run-icon {
  margin-right: 30px;
  margin-top: 8px;
  width: 16px;
  height: 16px;
  background-image: url('./../../assets/img/ide/icon_running.svg');
  cursor: pointer;
}
.run-icon-disabled {
  margin-right: 30px;
  margin-top: 8px;
  width: 16px;
  height: 16px;
  background-image: url('./../../assets/img/ide/icon_running_gray.svg');
  cursor: pointer;
}
</style>