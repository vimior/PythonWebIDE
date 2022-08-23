<template>
  <div class="main-wrapper ide-wrapper">
    <TopMenu class="top-menu"
      :consoleLimit="consoleLimit"
      :hasRunProgram="hasRunProgram"
      @set-text-dialog="setTextDialog"
      @set-del-dialog="setDelDialog"
      @set-projs-dialog="setProjsDialog"
      v-on:run-item="runPathSelected"
      @stop-item="stop"
    ></TopMenu>
    <div id="total-frame" class="total-frame">
      <ProjTree id="left-frame" class="left-frame float-left"
        v-on:get-item="getFile"
      ></ProjTree>
      <div id="right-frame" class="right-frame float-right">
        <div class="float-left top-tab">
          <CodeTabs
            v-if="ideInfo.codeItems.length > 0"
            v-on:select-item="selectFile"
            v-on:close-item="closeFile">
          </CodeTabs>
        </div>
        <div class="float-left code-editor-frame">
          <template v-for="(item, index) in ideInfo.codeItems" :key="item.path + index">
            <IdeEditor 
              :codeItem="item"
              :codeItemIndex="index"
              :consoleLimit="consoleLimit"
              @run-item="runPathSelected"
              v-if="ideInfo.codeSelected.path === item.path" 
              v-on:update-item="updateItem"></IdeEditor>
          </template>
        </div>
        <div class="float-left console-tab" v-if="showConsole"  v-show="!isMarkdown">
          <ConsoleTabs
            v-if="ideInfo.consoleItems.length > 0"
            v-on:select-item="selectConsole"
            v-on:close-item="closeConsoleSafe"
          >
          </ConsoleTabs>
          <!-- <div class="run-icon float-right" v-if="ideInfo.consoleSelected.run === false && !(ideInfo.consoleSelected.name === 'Terminal' && ideInfo.consoleSelected.path === 'Terminal')" @click="run()" title="重新运行当前控制台指向的脚本"></div>
          <div class="stop-icon float-right" v-if="ideInfo.consoleSelected.run === true" @click="stop(ideInfo.consoleSelected.id)" title="停止当前控制台运行的脚本或命令"></div> -->
        </div>
        <div class="float-left console-frame"  v-show="!isMarkdown">
          <template v-for="(item, index) in ideInfo.consoleItems" :key="item.path + index">
            <ConsoleItem
              :item="item" 
              @run-item="runConsoleSelected"
              @stop-item="stop"
              v-if="ideInfo.consoleSelected.path === item.path && ideInfo.consoleSelected.id === item.id">
            </ConsoleItem>
          </template>
        </div>
        <CmdRun class="float-left result-frame" v-show="!isMarkdown"></CmdRun>
      </div>
      <DialogProjs v-if="showProjsDialog"
        @on-cancel="onCloseProjsDialog" @on-select="onSelectProj" @on-delete="onDeleteProj" 
        @set-text-dialog="setTextDialog"></DialogProjs>
      <DialogText v-if="showFileDialog" :title="dialogTitle" :text="dialogText" :tips="dialogTips" @check-input="inputIsLegal"
        @on-cancel="onCloseTextDialog" @on-create="onCreate"></DialogText>
      <DialogDelete v-if="showDeleteDialog" :title="dialogTitle"
        @on-cancel="onCancelDelete" @on-delete="onDelete"></DialogDelete>
    </div>
  </div>
</template>

<script>
import * as types from '../../store/mutation-types';
import { ElMessage, ElMessageBox } from 'element-plus';
import TopMenu from './pages/ide/TopMenu';
import CodeTabs from './pages/ide/CodeTabs';
import ConsoleItem from './pages/ide/ConsoleItem';
import ConsoleTabs from './pages/ide/ConsoleTabs';
import CmdRun from './pages/ide/CmdRun';
import ProjTree from './pages/ide/ProjTree';
import IdeEditor from './pages/ide/IdeEditor';
import DialogProjs from './pages/ide/dialog/DialogProjs';
import DialogText from './pages/ide/dialog/DialogText';
import DialogDelete from './pages/ide/dialog/DialogDelete';
const path = require('path');

export default {
  data() {
    return {
      showDeleteDialog: false,
      showFileDialog: false,
      showProjsDialog: false,
      showCover: true,
      
      dialogType: '',
      dialogTitle: '',
      dialogTips: '',
      dialogText: '',
    }
  },
  components: {
    TopMenu,
    CodeTabs,
    ConsoleItem,
    ConsoleTabs,
    CmdRun,
    ProjTree,
    IdeEditor,
    DialogProjs,
    DialogText,
    DialogDelete,
  },
  created() {
  },
  mounted() {
    if (!this.wsInfo.rws) {
      this.$store.dispatch('websocket/init', {});
    }
    const self = this;
    const t = setInterval(() => {
      if (self.wsInfo.connected) {
        this.$store.dispatch(`ide/${types.IDE_LIST_PROJECTS}`, {
          callback: (dict) => {
            clearInterval(t);
            if (dict.code == 0) {
              this.$store.commit('ide/handleProjects', dict.data);
              self.getProject();
            }
          }
        })
      }
    }, 1000);
    window.addEventListener('resize', this.resize);
  },
  computed: {
    wsInfo() {
      return this.$store.getters['websocket/wsInfo']();
      // return this.$store.state.websocket.wsInfoMap.default;
    },
    ideInfo() {
      return this.$store.state.ide.ideInfo;
    },
    isMarkdown() {
      if (this.ideInfo.codeSelected.path)
        return this.ideInfo.codeSelected.path.endsWith('.md');
      else
        return false;
    },
    consoleLimit() {
      let count = 0;
      for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
        if (this.ideInfo.consoleItems[i].run === true && !(this.ideInfo.consoleItems[i].name === 'Terminal' && this.ideInfo.consoleItems[i].path === 'Terminal')) {
          count += 1;
        }
      }
      return count >= 3;
    },
    hasRunProgram() {
      return this.ideInfo.consoleItems.some(item => item.run);
    },
    showConsole() {
      const show = this.ideInfo.consoleItems.length !== 0;
      this.resize();
      return show;
    },
  },
  methods: {
    inputIsLegal(text, callback) {
      this.dialogText = text;
      let isLegal = this.checkStrIsLegal(this.dialogText, this.dialogType === 'create-file' || this.dialogType === 'rename-file');
      if (isLegal) {
        if (this.dialogType === 'create-project' || this.dialogType === 'rename-project') {
          isLegal = !this.isProjExist(this.dialogText);
        }
        else if (this.dialogType === 'create-file' || this.dialogType === 'rename-file' || this.dialogType === 'create-folder' || this.dialogType === 'rename-folder') {
          isLegal = !this.isFileExist(this.dialogText, this.dialogType === 'create-file' || this.dialogType === 'create-folder');
        }
      }
      callback(isLegal);
      return isLegal;
    },
    isProjExist(name) {
      const exist = this.ideInfo.projList.some(item => item.name === name);
      if (exist) {
        this.dialogTips = '工程名字已经存在';
      }
      return exist;
    },
    getParentData(path) {
      if (this.ideInfo.treeRef.currentNode && this.ideInfo.treeRef.currentNode.parent) {
        return this.ideInfo.treeRef.currentNode.parent.data;
      }
      else {
        let data = this.ideInfo.currProj.data;
        let alive = true;
        while (alive) {
          alive = false;
          for (var i = 0; i < data.children.length; i++) {
            if (data.children[i].path === this.ideInfo.nodeSelected.path) {
              return data;
            }
            else if (path.indexOf(data.children[i].path) === 0) {
              data = data.children[i];
              alive = true;
              break;
            }
          }
        }
      }
    },
    isFileExist(name, isCreate) {
      let exist = false;
      if (isCreate) {
        exist = this.ideInfo.nodeSelected.children.some(item => item.name === name);
      }
      else {
        const parentData = this.getParentData(this.ideInfo.nodeSelected.path);
        if (parentData && parentData.children)
          exist = parentData.children.some(item => item.name === name);
      }
      if (exist) {
        this.dialogTips = '已经存在相同名字文件';
      }
      return exist;
    },
    checkStrIsLegal(str, isFile) {
      this.dialogTips = '';
      let name = isFile ? str.lastIndexOf('.') !== -1 ? str.substring(0, str.lastIndexOf('.')) : str : str;
      if (!name) {
        this.dialogTips = '名字不能为空';
        return false;
      }
      else if (name.length > 15) {
        this.dialogTips = '名字长度不能超过15个字符';
        return false;
      }
      if (isFile && str.endsWith('.')) {
        this.dialogTips = '名字只能是字母和数字和下划线_';
        return false;
      }
      const ret = /^[a-zA-Z0-9_]+$/.test(name);
      if (!ret) {
        this.dialogTips = '名字只能是字母和数字和下划线_';
      }
      return ret;
    },
    listProjects(projectName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_LIST_PROJECTS}`, {
        callback: (dict) => {
          if (dict.code == 0) {
            self.$store.commit('ide/handleProjects', dict.data);
            if (projectName) {
              self.getProject(projectName);
            }
          }
        }
      });
    },
    getProject(name) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_GET_PROJECT}`, {
        projectName: name === undefined ? this.ideInfo.currProj.config.name : name,
        callback: (dict) => {
          if (dict.code == 0) {
            self.$store.commit('ide/handleProject', dict.data);
            for (var i = 0; i < self.ideInfo.currProj.config.openList.length; i++) {
              self.getFile(self.ideInfo.currProj.config.openList[i], false);
            }
          }
        }
      });
    },
    getFile(path, save) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_GET_FILE}`, {
        filePath: path,
        callback: (dict) => {
          if (dict.code == 0) {
            self.$store.commit('ide/handleGetFile', {
              filePath: path,
              data: dict.data,
              save: save
            });
            if (save !== false)
              self.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
          }
        }
      });
    },
    setTextDialog(data) {
      this.dialogType = data.type;
      this.dialogTitle = data.title;
      this.dialogText = data.text;
      this.dialogTips = data.tips;
      this.showFileDialog = true;
      this.showProjsDialog = false;
    },
    setDelDialog(data) {
      this.dialogType = '';
      this.dialogTitle = data.title;
      this.dialogText = '';
      this.dialogTips = '';
      this.showDeleteDialog = true;
    },
    setProjsDialog(data) {
      this.dialogType = '';
      this.dialogTitle = '';
      this.dialogText = '';
      this.dialogTips = '';
      this.showProjsDialog = true;
    },
    onCloseTextDialog() {
      this.showFileDialog = false;
      if (this.ideInfo.nodeSelected) {
        this.ideInfo.treeRef.setCurrentNode(this.ideInfo.nodeSelected);
      }
      if (this.dialogType === 'create-project') {
        this.showProjsDialog = true;
      }
    },
    onCloseProjsDialog() {
      this.showProjsDialog = false;
      this.showFileDialog = false;
      this.showDeleteDialog = false;
      if (this.ideInfo.nodeSelected) {
        this.ideInfo.treeRef.setCurrentNode(this.ideInfo.nodeSelected);
      }
    },
    onCancelDelete() {
      this.showDeleteDialog = false;
      if (this.ideInfo.nodeSelected) {
        this.ideInfo.treeRef.setCurrentNode(this.ideInfo.nodeSelected);
      }
    },
    deleteProject(projectName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_DEL_PROJECT}`, {
        projectName: projectName,
        callback: (dict) => {
          if (dict.code == 0) {
            self.$store.commit('ide/handleDelProject', projectName);
          }
        }
      });
    },
    deleteFile(filePath, projectName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_DEL_FILE}`, {
        projectName: projectName === undefined ? this.ideInfo.currProj.config.name : projectName,
        filePath: filePath,
        callback: (dict) => {
          if (dict.code == 0) {
            const parentData = self.getParentData(filePath);
            self.$store.commit('ide/handleDelFile', {parentData, filePath});
          }
        }
      });
    },
    deleteFolder(folderPath, projectName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_DEL_FOLDER}`, {
        projectName: projectName === undefined ? this.ideInfo.currProj.config.name : projectName,
        folderPath: folderPath,
        callback: (dict) => {
          if (dict.code == 0) {
            const parentData = self.getParentData(folderPath);
            if (parentData)
              self.$store.commit('ide/handleDelFolder', {parentData, folderPath});
          }
        }
      });
    },
    createProject(projectName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_CREATE_PROJECT}`, {
        projectName: projectName,
        callback: (dict) => {
          if (dict.code == 0) {
            self.listProjects(projectName);
          }
        }
      });
    },
    createFile(fileName, parentPath, projectName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_CREATE_FILE}`, {
        projectName: projectName === undefined ? this.ideInfo.currProj.config.name : projectName,
        parentPath: parentPath === undefined ? this.ideInfo.nodeSelected.path : parentPath,
        fileName: fileName,
        callback: (dict) => {
          if (dict.code == 0) {
            const newPath = path.join(self.ideInfo.nodeSelected.path, fileName);
            self.$store.commit('ide/addChildrenNode', {
              name: fileName,
              path: newPath,
              type: 'file'
            });
            self.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
          }
        }
      });
    },
    createFolder(folderName, parentPath, projectName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_CREATE_FOLDER}`, {
        projectName: projectName === undefined ? this.ideInfo.currProj.config.name : projectName,
        parentPath: parentPath === undefined ? this.ideInfo.nodeSelected.path : parentPath,
        folderName: folderName,
        callback: (dict) => {
          if (dict.code == 0) {
            const newPath = path.join(self.ideInfo.nodeSelected.path, folderName);
            self.$store.commit('ide/addChildrenNode', {
              name: folderName,
              path: newPath,
              type: 'dir'
            });
            self.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
          }
        }
      });
    },
    renameProject(newName, oldName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_RENAME_PROJECT}`, {
        oldName: oldName === undefined ? this.ideInfo.currProj.config.name : oldName,
        newName: newName,
        callback: (dict) => {
          if (dict.code == 0) {
            self.$store.commit('ide/handleRename', newName);
            self.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
          }
        }
      });
    },
    renameFile(newName, oldPath, projectName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_RENAME_FILE}`, {
        projectName: projectName === undefined ? this.ideInfo.currProj.config.name : projectName,
        oldPath: oldPath === undefined ? this.ideInfo.nodeSelected.path : oldPath,
        fileName: newName,
        callback: (dict) => {
          if (dict.code == 0) {
            self.$store.commit('ide/handleRename', newName);
            self.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
          }
        }
      });
    },
    renameFolder(newName, oldPath, projectName) {
      const self = this;
      this.$store.dispatch(`ide/${types.IDE_RENAME_FOLDER}`, {
        projectName: projectName === undefined ? this.ideInfo.currProj.config.name : projectName,
        oldPath: oldPath === undefined ? this.ideInfo.nodeSelected.path : oldPath,
        folderName: newName,
        callback: (dict) => {
          if (dict.code == 0) {
            self.$store.commit('ide/handleRename', newName);
            self.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
          }
        }
      });
    },
    onDelete() {
      this.showDeleteDialog = false;
      if (!this.ideInfo.nodeSelected || !this.ideInfo.nodeSelected.type) {
        // delete file
        this.deleteFile(this.ideInfo.nodeSelected.path);
      }
      else {
        if (this.ideInfo.nodeSelected.type === 'dir') {
          // delete folder
          this.deleteFolder(this.ideInfo.nodeSelected.path);
        }
        else {
          // delete file
          this.deleteFile(this.ideInfo.nodeSelected.path);
        }
      }
    },
    onCreate() {
      const text = this.dialogText;
      if (this.dialogType === 'create-file') {
        this.createFile(text);
      }
      else if (this.dialogType === 'rename-file') {
        this.renameFile(text);
      }
      else if (this.dialogType === 'create-folder') {
        this.createFolder(text);
      }
      else if (this.dialogType === 'rename-folder') {
        this.renameFolder(text);
      }
      else if (this.dialogType === 'create-project') {
        if (this.hasRunProgram) {
          const self = this;
          ElMessageBox.confirm(
            '是否停止所有运行中的程序并创建新工程?',
            '警告',
            {
              confirmButtonText: '停止并创建',
              cancelButtonText: '取消',
              type: 'warning',
            }
          )
          .then(() => {
            self.stopAll();
            self.$store.commit('ide/setConsoleItems', []);
            self.createProject(text);
          })
          .catch(() => {
            console.log('canceled create project');
          });
        }
        else {
          this.$store.commit('ide/setConsoleItems', []);
          this.createProject(text);
        }
      }
      else if (this.dialogType === 'rename-project') {
        this.renameProject(text);
      }
      this.showProjsDialog = false;
      this.showFileDialog = false;
      this.showDeleteDialog = false;
    },
    onDeleteProj(projectName) {
      const self = this;
      ElMessageBox.confirm(
        '是否删除工程?',
        '提示',
        {
          confirmButtonText: '删除',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )
      .then(() => {
        self.deleteProject(projectName);
        ElMessage({
          type: 'success',
          message: '删除成功',
        })
      })
      .catch(() => {
        ElMessage({
          type: 'info',
          message: '已取消',
        })
      });
    },
    onSelectProj(projectName) {
      if (this.hasRunProgram) {
        ElMessageBox.confirm(
          '是否停止所有运行中的程序并切换工程?',
          '警告',
          {
            confirmButtonText: '停止并切换',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        .then(() => {
          this.stopAll();
          this.$store.commit('ide/setConsoleItems', []);
          this.getProject(projectName);
          this.showProjsDialog = false;
        })
        .catch(() => {
          this.showProjsDialog = false;
        });
      }
      else {
        // this.$store.commit('ide/setConsoleItems', []);
        this.getProject(projectName);
        this.showProjsDialog = false;
        this.$store.commit('ide/setConsoleItems', []);
      }
    },
    selectFile(item) {
      this.$store.commit('ide/setPathSelected', item.path);
      this.$store.commit('ide/setCodeSelected', item);
      if (this.ideInfo.currProj.pathSelected) {
        this.ideInfo.treeRef.setCurrentKey(this.ideInfo.currProj.pathSelected);
      }
      this.$store.commit('ide/setNodeSelected', this.ideInfo.treeRef.getCurrentNode());
      this.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
    },
    closeFile(item) {
      const codeItems = []
      for (let i = 0; i < this.ideInfo.codeItems.length; i++) {
        if (item.path !== this.ideInfo.codeItems[i].path) {
          codeItems.push(this.ideInfo.codeItems[i]);        
        }
        else {
          if (i > 0) {
            if (this.ideInfo.currProj.pathSelected === item.path) {
              this.$store.commit('ide/setPathSelected', this.ideInfo.codeItems[i - 1].path);
              this.$store.commit('ide/setCodeSelected', this.ideInfo.codeItems[i - 1]);
              // this.$store.commit('ide/setNodeSelected', this.ideInfo.codeItems[i - 1]);
            }
          }
          else if (i < this.ideInfo.codeItems.length - 1) {
            if (this.ideInfo.currProj.pathSelected === item.path) {
              this.$store.commit('ide/setPathSelected', this.ideInfo.codeItems[i + 1].path);
              this.$store.commit('ide/setCodeSelected', this.ideInfo.codeItems[i + 1]);
              // this.$store.commit('ide/setNodeSelected', this.ideInfo.codeItems[i + 1]);
            }
          }
        }
      }
      this.$store.commit('ide/setCodeItems', codeItems);
      if (this.ideInfo.codeItems.length === 0) {
        this.$store.commit('ide/setPathSelected', null);
        this.$store.commit('ide/setCodeSelected', {});
        // this.$store.commit('ide/setNodeSelected', null);
      }
      this.$store.dispatch(`ide/${types.IDE_SAVE_PROJECT}`, {});
    },
    updateItem(path, codemirror) {
      for (let i = 0; i < this.ideInfo.codeItems.length; i++) {
        if (path === this.ideInfo.codeItems[i].path) {
          this.$store.commit('ide/setCodeItemMirror', {index: i, codemirror: codemirror});
          break;
        }
      }
    },
    selectConsole(item) {
      this.$store.commit('ide/setConsoleSelected', item);
    },
    closeConsoleSafe(item) {
      if (item.run === true) {
        ElMessageBox.confirm(
          '是否停止该程序并关闭终端?',
          '警告',
          {
            confirmButtonText: '停止并关闭',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        .then(() => {
          this.stop(item.id);
          this.closeConsole(item);
        })
        .catch(() => {
          console.log('canceled close console');
        });
      }
      else {
        this.closeConsole(item);
      }
    },
    closeConsole(item) {
      const consoleItems = []
      for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
        if (item.name === 'Terminal' && item.path === 'Terminal') {
          if (item.id !== this.ideInfo.consoleItems[i].id) {
            consoleItems.push(this.ideInfo.consoleItems[i]);
          }
          else {
            if (i > 0) {
              this.$store.commit('ide/setConsoleSelected', this.ideInfo.consoleItems[i - 1]);
            }
            else if (i < this.ideInfo.consoleItems.length - 1) {
              this.$store.commit('ide/setConsoleSelected', this.ideInfo.consoleItems[i + 1]);
            }
          }
        }
        else {
          if (item.path !== this.ideInfo.consoleItems[i].path || item.id !== this.ideInfo.consoleItems[i].id) {
            consoleItems.push(this.ideInfo.consoleItems[i]);
          }
          else {
            if (i > 0) {
              this.$store.commit('ide/setConsoleSelected', this.ideInfo.consoleItems[i - 1]);
            }
            else if (i < this.ideInfo.consoleItems.length - 1) {
              this.$store.commit('ide/setConsoleSelected', this.ideInfo.consoleItems[i + 1]);
            }
          }
        }
      }
      this.$store.commit('ide/setConsoleItems', consoleItems);
      if (this.ideInfo.consoleItems.length === 0) {
        this.$store.commit('ide/setConsoleSelected', {});
      }
      this.resize();
    },
    resize() {
      // const ele = document.getElementById('left-frame');
      // if (ele !== undefined && ele !== null) {
      //   ele.style.height = `${window.innerHeight - 30}px`;
      // }
      this.$store.commit('ide/setCodeHeight', this.ideInfo.consoleItems.length === 0 ? window.innerHeight - 102 : window.innerHeight - 326); // 338

      // for (let i = 0; i < this.ideInfo.codeItems.length; i++) {
      //   if (this.ideInfo.codeItems[i].codemirror !== null) {
      //     // this.ideInfo.codeItems[i].codemirror.setSize('auto', this.ideInfo.consoleItems.length === 0 ? window.innerHeight - 120 : window.innerHeight - 355)
      //     this.ideInfo.codeItems[i].codemirror.setSize('auto', this.ideInfo.consoleItems.length === 0 ? window.innerHeight - 102 : window.innerHeight - 338)
      //   }
      // }
    },
    runPathSelected() {
      let selected = false;
      if (this.ideInfo.consoleSelected.run === false && this.ideInfo.consoleSelected.path === this.ideInfo.currProj.pathSelected) {
        selected = true;
        this.$store.commit('ide/assignConsoleSelected', {
          stop: false,
          resultList: []
        });
      }
      else {
        for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
          if (this.ideInfo.consoleItems[i].run === false && this.ideInfo.consoleItems[i].path === this.ideInfo.currProj.pathSelected) {
            this.$store.commit('ide/setConsoleSelected', this.ideInfo.consoleItems[i]);
            selected = true;
            this.$store.commit('ide/assignConsoleSelected', {
              stop: false,
              resultList: []
            });
            break;
          }
        }
      }
      if (selected === false) {
        for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
          if (this.ideInfo.consoleItems[i].run === false && !(this.ideInfo.consoleItems[i].name === 'Terminal' && this.ideInfo.consoleItems[i].path === 'Terminal')) {
            this.$store.commit('ide/spliceConsoleItems', {start: i, count: 1});
            break;
          }
        }
        const item = {
          name: path.basename(this.ideInfo.currProj.pathSelected),
          path: this.ideInfo.currProj.pathSelected,
          resultList: [],
          run: false,
          stop: false,
          id: this.ideInfo.consoleId,
        }
        this.$store.commit('ide/addConsoleItem', item);
        this.$store.commit('ide/setConsoleSelected', item);
      }
      else {
        this.$store.commit('ide/assignConsoleSelected', {
          id: this.ideInfo.consoleId
        });
      }

      if (!this.ideInfo.consoleItems.includes(this.ideInfo.consoleSelected)) {
        this.$store.commit('ide/addConsoleItem', this.ideInfo.consoleSelected);
      }
      this.$store.dispatch(`ide/${types.IDE_RUN_PYTHON_PROGRAM}`, {
        msgId: this.ideInfo.consoleId,
        filePath: this.ideInfo.currProj.pathSelected,
        callback: {
          limits: -1,
          callback: (dict) => {
            this.$store.commit('ide/handleRunResult', dict);
          }
        }
      });
      this.$store.commit('ide/setConsoleId', this.ideInfo.consoleId + 1);
    },
    runConsoleSelected() {
      this.$store.dispatch(`ide/${types.IDE_RUN_PYTHON_PROGRAM}`, {
        msgId: this.ideInfo.consoleSelected.id,
        filePath: this.ideInfo.consoleSelected.path,
        callback: {
          limits: -1,
          callback: (dict) => {
            this.$store.commit('ide/handleRunResult', dict);
          }
        }
      });
    },
    stop(consoleId) {
      this.$store.dispatch(`ide/${types.IDE_STOP_PYTHON_PROGRAM}`, {
        consoleId: consoleId,
        callback: {
          limits: -1,
          callback: (dict) => {
            this.$store.commit('ide/handleStopResult', {
              consoleId: consoleId,
              dict: dict
            });
          }
        }
      });
    },
    stopAll() {
      for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
        if (this.ideInfo.consoleItems[i].run === true) {
          this.stop(this.ideInfo.consoleItems[i].id);
        }
      }
      this.stop(null);
    }
  }
}
</script>
<style scoped>
.ide-wrapper {
  text-align: left;
  background-color: #1E1E1E;
  color: #CCCCCC;
}
a {
  color: white;
}
.total-frame {
  /*background-color:gray;*/
  position: fixed;
  width: 100%;
  height: 100%;
  top: 30px;
  /* top: 76px; */
  left: 0;
  /* display: inline-flex; */
  /* left: 10px; */
  /* border:1px solid #96c2f1; */
  /* background:yellow; */
  /*top: 200px;
  left: 100px;*/
}
body {
  scrollbar-track-color: #3C3F41;
}
.top-menu {
  position: fixed;
  width: 100%;
  height: 36px;
  top: 0;
  /* top: 40px; */
  left: 0;
  background: #313131;
  /* background: #252526; */
}
.top-tab {
  width: 100%;
  /* background: #313335; */
  /* background-color: yellow; */
  background: #252526;
}
.left-frame {
  /* width:200px; */
  width: 200px;
  height: calc(100% - 31px);
  overflow-y: auto;
  overflow-x: auto;
  /* background: #2E3032; */
  /* background: #383B3D; */
  background: #282828;
  color: #CCCCCC;
  /* scrollbar-track-color: #3C3F41; */
  /* SCROLLBAR-TRACK-COLOR: aquamarine; */
}
.left-frame::-webkit-scrollbar {/*滚动条整体样式*/
  width: 6px;     /*高宽分别对应横竖滚动条的尺寸*/
  height: 6px;
}
.left-frame::-webkit-scrollbar-thumb {/*滚动条里面小方块*/
  background: #87939A;
}
.left-frame::-webkit-scrollbar-track {/*滚动条里面轨道*/
  background: #2F2F2F;
}
.right-frame {
  position: absolute;
  left: 200px;
  right: 0px;
  /* width:90%; */
  /* width: 100%; */
  height: 100%;
  overflow-x: hidden;
  overflow-y: hidden;
  /*background-color:#e9e6d3;*/
  background: #3C3F41;
}
.code-editor-frame {
  /* position: absolute; */
  /* width: 100%; */
  /* position: relative; */
  width: 100%;
  /* height: 100%; */
}
.console-tab {
  /* position: fixed; */
  width: 100%;
  /* bottom: 200px; */
  background: #3A3D41;
  /* left: 200px; */
  /* bottom: 232px; */
  /* padding: 0px; */
  /* margin: 0px; */
  /* height: 20px; */
}
.run-icon {
  margin-right: 20px;
  margin-top: -5px;
  width: 16px;
  height: 16px;
  background-image: url('./../../assets/img/ide/icon_running.svg');
  cursor: pointer;
}
.stop-icon {
  margin-right: 20px;
  margin-top: 5px;
  width: 16px;
  height: 16px;
  background-image: url('./../../assets/img/ide/icon_stop.svg');
  cursor: pointer;
}
.console-frame {
  background-color:#e9e6d3;
  left: 0px;
  bottom: 0px;
  padding: 0px;
  margin: 0px;
  /* overflow-y: scroll;
  overflow-x: scroll; */
}
.result-frame {
  /* left: 200px;
  bottom: 0px;
  padding: 0px;
  margin: 0px; */
  width: calc(100% - 200px);
}
</style>
