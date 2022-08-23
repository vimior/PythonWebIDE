<template>
  <div>
    <div class="back-icon float-left" @click="backHome"><el-icon><back /></el-icon></div>
    <div class="project-icon float-left" @click="listProjects()" title="工程列表"></div>
    <div v-if="ideInfo.nodeSelected !== null && ideInfo.nodeSelected.type === 'dir'" class="file-icon float-left" @click="newFile()" title="新建文件"></div>
    <div v-else class="file-icon float-left disable-icon" title="新建文件"></div>
    <div v-if="ideInfo.nodeSelected !== null && ideInfo.nodeSelected.type === 'dir'" class="folder-icon float-left" @click="newFolder()" title="新建文件夹"></div>
    <div v-else class="folder-icon float-left disable-icon" title="新建文件夹"></div>
    <div v-if="ideInfo.nodeSelected !== null" class="rename-icon float-left" @click="rename()" title="重命名"></div>
    <div v-else class="rename-icon float-left disable-icon" title="重命名"></div>
    <div v-if="ideInfo.nodeSelected !== null && ideInfo.nodeSelected.path !== '/'" class="del-icon float-left" @click="delFile()" title="删除"></div>
    <div v-else class="del-icon float-left disable-icon" title="删除"></div>
    <div class="status-icon float-left" title="状态" :class="{'el-icon-circle-check': wsInfo.connected, 'el-icon-circle-close': !wsInfo.connected}" :style="{color: wsInfo.connected ? '#52bf53' : '#e15960'}"></div>
    <span>
      <div class="float-right stop-icon" @click="stopAll()" v-if="hasRunProgram" title="停止所有运行的脚本"></div>
      <!-- <div class="float-right stop-icon-disabled" v-if="!hasRunProgram" title="停止所有运行的脚本"></div> -->
    </span>
    <span>
      <div class="run-icon float-right" v-if="isPythonFile && !consoleLimit" @click="$emit('run-item')" title="运行当前选中的脚本"></div>
      <div class="run-icon-disabled float-right" v-if="!isPythonFile && !consoleLimit" title="无法运行，当前选中的文件不是python文件"></div>
    </span>
  </div>
</template>

<script>
import { Back } from '@element-plus/icons';
// import * as types from '../../../../store/mutation-types';
const path = require('path');

export default {
  props: {
    consoleLimit: Boolean,
    hasRunProgram: Boolean,
  },
  data() {
    return {
      isRun: true,
    }
  },
  computed: {
    wsInfo() {
      return this.$store.getters['websocket/wsInfo']();
    },
    ideInfo() {
      return this.$store.state.ide.ideInfo;
    },
    isPythonFile() {
      return this.ideInfo.currProj.pathSelected !== null && this.ideInfo.codeItems.length > 0 && this.ideInfo.currProj.pathSelected.endsWith('.py');
      // return this.ideInfo.currProj.pathSelected !== null && this.ideInfo.codeItems.length > 0 && this.ideInfo.currProj.pathSelected.lastIndexOf('.py') === this.ideInfo.currProj.pathSelected.length - 3;
    },
  },
  components: {
    Back,
  },
  methods: {
    backHome() {
      this.$router.push('/');
    },
    listProjects() {
      this.$emit('setProjsDialog', {});
    },
    newFile() {
      this.$emit('setTextDialog', {
        type: 'create-file',
        title: '新建文件',
        text: '',
        tips: ''
      });
    },
    newFolder() {
      this.$emit('setTextDialog', {
        type: 'create-folder',
        title: '新建文件夹',
        text: '',
        tips: ''
      });
    },
    rename() {
      let dialogType = '';
      let dialogTitle = ''; 
      let dialogInputText = '';
      if (this.ideInfo.nodeSelected.path === '/') {
        dialogType = 'rename-project';
        dialogTitle = `重命名工程 (${this.ideInfo.currProj.data.name})`
        dialogInputText = `${this.ideInfo.currProj.data.name}`;
      }
      else if (this.ideInfo.nodeSelected.type === 'dir') {
        const name = path.basename(this.ideInfo.nodeSelected.path);
        dialogType = 'rename-folder';
        dialogTitle = `重命名文件夹 (${this.ideInfo.nodeSelected.path})`
        dialogInputText = `${name}`;
      }
      else {
        const name = path.basename(this.ideInfo.currProj.pathSelected);
        dialogType = 'rename-file';
        dialogTitle = `重命名文件 (${this.ideInfo.currProj.pathSelected})`
        dialogInputText = `${name}`;
      }
      this.$emit('setTextDialog', {
        type: dialogType,
        title: dialogTitle,
        text: dialogInputText,
        tips: ''
      });
    },
    delFile() {
      this.$emit('setDelDialog', {
        type: '',
        title: `删除 ${path.basename(this.ideInfo.nodeSelected.path)}?`,
        text: '',
        tips: ''
      });
    },
    // run() {
    //   let selected = false;
    //   if (this.ideInfo.consoleSelected.run === false && this.ideInfo.consoleSelected.path === this.ideInfo.currProj.pathSelected) {
    //     selected = true;
    //     this.$store.commit('ide/assignConsoleSelected', {
    //       stop: false,
    //       resultList: []
    //     });
    //   }
    //   else {
    //     for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
    //       if (this.ideInfo.consoleItems[i].run === false && this.ideInfo.consoleItems[i].path === this.ideInfo.currProj.pathSelected) {
    //         this.$store.commit('ide/setConsoleSelected', this.ideInfo.consoleItems[i]);
    //         selected = true;
    //         this.$store.commit('ide/assignConsoleSelected', {
    //           stop: false,
    //           resultList: []
    //         });
    //         break;
    //       }
    //     }
    //   }
    //   if (selected === false) {
    //     for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
    //       if (this.ideInfo.consoleItems[i].run === false && !(this.ideInfo.consoleItems[i].name === 'Terminal' && this.ideInfo.consoleItems[i].path === 'Terminal')) {
    //         this.$store.commit('ide/spliceConsoleItems', {start: i, count: 1});
    //         break;
    //       }
    //     }
    //     const item = {
    //       name: path.basename(this.ideInfo.currProj.pathSelected),
    //       path: this.ideInfo.currProj.pathSelected,
    //       resultList: [],
    //       run: false,
    //       stop: false,
    //       id: this.ideInfo.consoleId,
    //     }
    //     this.$store.commit('ide/addConsoleItem', item);
    //     this.$store.commit('ide/setConsoleSelected', item);
    //   }
    //   else {
    //     this.$store.commit('ide/assignConsoleSelected', {
    //       id: this.ideInfo.consoleId
    //     });
    //   }
    //   // for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
    //   //   if (this.ideInfo.consoleItems[i].run === false && !(this.ideInfo.consoleItems[i].name === 'Terminal' && this.ideInfo.consoleItems[i].path === 'Terminal')) {
    //   //     this.$store.commit('ide/spliceConsoleItems', {start: i, count: 1});
    //   //     break;
    //   //   }
    //   // }
    //   // const item = {
    //   //   name: path.basename(this.ideInfo.currProj.pathSelected),
    //   //   path: this.ideInfo.currProj.pathSelected,
    //   //   resultList: [],
    //   //   run: false,
    //   //   stop: false,
    //   //   id: this.ideInfo.consoleId,
    //   // }
    //   // this.$store.commit('ide/addConsoleItem', item);
    //   // this.$store.commit('ide/setConsoleSelected', item);

    //   if (!this.ideInfo.consoleItems.includes(this.ideInfo.consoleSelected)) {
    //     this.$store.commit('ide/addConsoleItem', this.ideInfo.consoleSelected);
    //   }
    //   this.$store.dispatch(`ide/${types.IDE_RUN_PYTHON_PROGRAM}`, {
    //     msgId: this.ideInfo.consoleId,
    //     filePath: this.ideInfo.currProj.pathSelected,
    //     callback: {
    //       limits: -1,
    //       callback: (dict) => {
    //         this.$store.commit('ide/handleRunResult', dict);
    //       }
    //     }
    //   });
    //   this.$store.commit('ide/setConsoleId', this.ideInfo.consoleId + 1);
    // },
    // stop(consoleId) {
    //   this.$store.dispatch(`ide/${types.IDE_STOP_PYTHON_PROGRAM}`, {
    //     consoleId: consoleId,
    //     callback: {
    //       limits: -1,
    //       callback: (dict) => {
    //         this.$store.commit('ide/handleStopResult', {
    //           consoleId: consoleId,
    //           dict: dict
    //         });
    //       }
    //     }
    //   });
    // },
    stopAll() {
      for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
        if (this.ideInfo.consoleItems[i].run === true) {
          this.$emit('stop-item', this.ideInfo.consoleItems[i].id);
          // this.stop(this.ideInfo.consoleItems[i].id);
        }
      }
      this.$emit('stop-item', null);
      // this.stop(null);
    }
  }
}
</script>

<style scoped>
.back-icon {
  margin-top: 8px;
  margin-right: 10px;
  margin-left: 10px;
}
.project-icon {
  margin-left: 17px;
  margin-top: 13px;
  width: 24px;
  height: 24px;
  background-image: url('~@/assets/img/ide/btn_addproject.svg');
  background-size: 13px 11px;
  background-repeat: no-repeat;
  cursor: pointer;
}
.folder-icon {
  margin-left: 20px;
  margin-top: 6px;
  width: 24px;
  height: 24px;
  background-image: url('~@/assets/img/ide/btn_addfolder.svg');
  cursor: pointer;
}
.file-icon {
  margin-left: 10px;
  margin-top: 6px;
  width: 24px;
  height: 24px;
  background-image: url('~@/assets/img/ide/icon_addfile.svg');
  cursor: pointer;
}
.rename-icon {
  margin-left: 20px;
  margin-top: 6px;
  width: 24px;
  height: 24px;
  background-image: url('~@/assets/img/ide/btn_rename.svg');
  cursor: pointer;
}
.del-icon {
  margin-left: 20px;
  margin-top: 6px;
  width: 24px;
  height: 24px;
  background-image: url('~@/assets/img/ide/btn_trash.svg');
  cursor: pointer;
}
.status-icon {
  margin-left: 20px;
  margin-top: 12px;
  width: 24px;
  height: 24px;
  color: '#52bf53';
}
.disable-icon {
  opacity: 0.3;
  cursor: not-allowed;
}
.stop-icon {
  margin-right: 20px;
  margin-top: 10px;
  width: 16px;
  height: 16px;
  color: #656666;
  background-image: url('~@/assets/img/ide/icon_stop.svg');
  cursor: pointer;
}
.stop-icon-disabled {
  margin-right: 20px;
  margin-top: 10px;
  width: 16px;
  height: 16px;
  background-image: url('~@/assets/img/ide/icon_stop_gray.svg');
  cursor: pointer;
}
.run-icon {
  margin-right: 30px;
  margin-top: 8px;
  width: 16px;
  height: 16px;
  background-image: url('~@/assets/img/ide/icon_running.svg');
  cursor: pointer;
}
.run-icon-disabled {
  margin-right: 30px;
  margin-top: 8px;
  width: 16px;
  height: 16px;
  background-image: url('~@/assets/img/ide/icon_running_gray.svg');
  cursor: pointer;
}
</style>