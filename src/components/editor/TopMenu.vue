<template>
  <div>
    <div class="project-icon float-left" @click="listProjects()" title="Projects"></div>
    <div v-if="model.ideModel.selectNode !== null && model.ideModel.selectNode.type === 'dir'" class="file-icon float-left" @click="newFile()" title="Add File"></div>
    <div v-else class="file-icon float-left" title="Add File" style="opacity:0.3"></div>
    <div v-if="model.ideModel.selectNode !== null && model.ideModel.selectNode.type === 'dir'" class="folder-icon float-left" @click="newFolder()" title="Add Folder"></div>
    <div v-else class="folder-icon float-left" title="Add Folder" style="opacity:0.3"></div>
    <div v-if="model.ideModel.selectNode !== null" class="rename-icon float-left" @click="rename()" title="Rename"></div>
    <div v-else class="rename-icon float-left" title="Rename" style="opacity:0.3"></div>
    <div v-if="model.ideModel.selectNode !== null && model.ideModel.selectNode.path !== '/'" class="del-icon float-left" @click="delFile()" title="Delete"></div>
    <div v-else class="del-icon float-left" title="Delete" style="opacity:0.3"></div>
    <span>
      <div class="float-right stop-icon" @click="stopAll()" v-if="hasRunProgram" title='StopAll'></div>
      <div class="float-right stop-icon-disabled" v-if="!hasRunProgram" title='StopAll'></div>
    </span>
    <span>
      <div class="run-icon float-right" v-if="isPythonFile" @click="run()" title='Run'></div>
      <div class="run-icon-disabled float-right" v-if="!isPythonFile" title='Run'></div>
    </span>
  </div>
</template>

<script>
const path = require('path');

export default {
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
  },
  methods: {
    listProjects() {
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showProjsDialog = true;
    },
    newFile() {
      this.model.ideModel.dialogType = 'create-file';
      this.model.ideModel.dialogTitle = 'Create file';
      this.model.ideModel.dialogInputText = '';
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showFileDialog = true;
    },
    newFolder() {
      this.model.ideModel.dialogType = 'create-folder';
      this.model.ideModel.dialogTitle = 'Create folder';
      this.model.ideModel.dialogInputText = '';
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showFileDialog = true;
    },
    rename() {
      if (this.model.ideModel.selectNode.path === '/') {
        this.model.ideModel.dialogType = 'rename-project';
        this.model.ideModel.dialogTitle = `Rename project (${this.model.ideModel.curProjTree.name})`
        this.model.ideModel.dialogInputText = `${this.model.ideModel.curProjTree.name}`;
      }
      else if (this.model.ideModel.selectNode.type === 'dir') {
        const name = path.basename(this.model.ideModel.selectNode.path);
        this.model.ideModel.dialogType = 'rename-folder';
        this.model.ideModel.dialogTitle = `Rename folder (${this.model.ideModel.selectNode.path})`
        this.model.ideModel.dialogInputText = `${name}`;
      }
      else {
        const name = path.basename(this.model.ideModel.selectFilePath);
        this.model.ideModel.dialogType = 'rename-file';
        this.model.ideModel.dialogTitle = `Rename file (${this.model.ideModel.selectFilePath})`
        this.model.ideModel.dialogInputText = `${name}`;
      }
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showFileDialog = true;
    },
    delFile() {
      const name = path.basename(this.model.ideModel.selectNode.path);
      this.model.ideModel.dialogTitle = `Delete ${name}?`;
      this.model.ideModel.dialogTips = '';
      this.model.ideModel.showDeleteDialog = true;
    },
    run() {
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === false) {
          this.model.ideModel.consoleItems.splice(i, 1)
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
      this.model.ideModel.runPythonProgram(this.model.ideModel.consoleId, this.model.ideModel.selectFilePath);
      this.model.ideModel.consoleId = this.model.ideModel.consoleId + 1;
    },
    stopAll() {
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === true) {
          this.model.ideModel.stopPythonProgram(this.model.ideModel.consoleItems[i].id);
        }
      }
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