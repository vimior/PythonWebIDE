<template>
  <div class="main-wrapper editor-wrapper">
    <!-- <BaseCommonTopMenu
      :backTitle="$t('ide')"
      style="position:fixed;"
    ></BaseCommonTopMenu> -->
    <TopMenu class="top-menu"></TopMenu>
    <div id="total-frame" class="total-frame">
      <ElTree id="left-frame" class="left-frame float-left"></ElTree>
      <div id="right-frame" class="right-frame float-right">
        <div class="float-left top-tab">
          <!-- <div class="float-left" style="height:20px;width:1px;"></div> -->
          <template v-for="(item, index) in model.ideModel.codeItems">
            <CodeTab :item="item"
              :key="item.path + index"
              v-on:select-item="selectFile"
              v-on:close-item="closeFile"
              :selected="model.ideModel.selectFilePath === item.path">
            </CodeTab>
          </template>
        </div>
        <div class="float-left code-editor-frame">
          <template v-for="(item, index) in model.ideModel.codeItems">
            <CodeEditor 
              :item="item"
              :key="item.path + index"
              v-if="model.ideModel.selectFilePath === item.path" 
              v-on:update-item="updateItem"></CodeEditor>
          </template>
        </div>
        <div class="float-left console-tab" v-if="showConsole">
          <template v-for="(item, index) in model.ideModel.consoleItems">
            <ConsoleTab :item="item"
              :key="item.path + index"
              v-on:select-item="selectConsole"
              v-on:close-item="closeConsoleSafe"
              :selected="model.ideModel.selectConsoleItem.path === item.path && model.ideModel.selectConsoleItem.id === item.id">
            </ConsoleTab>
          </template>
          <div class="run-icon float-right" v-if="model.ideModel.selectConsoleItem.run === false && !(model.ideModel.selectConsoleItem.name === 'Terminal' && model.ideModel.selectConsoleItem.path === 'Terminal')" @click="run()" :title="$t('run')"></div>
          <div class="stop-icon float-right" v-if="model.ideModel.selectConsoleItem.run === true" @click="stop()" :title="$t('stop')"></div>
        </div>
        <div class="float-left console-frame">
          <template v-for="(item, index) in model.ideModel.consoleItems">
            <Console 
              :key="item.path + index"
              :item="item" 
              v-if="model.ideModel.selectConsoleItem.path === item.path && model.ideModel.selectConsoleItem.id === item.id">
            </Console>
          </template>
        </div>
        <CmdRun class="float-left result-frame"></CmdRun>
      </div>
      <DialogProjs v-if="model.ideModel.showProjsDialog"></DialogProjs>
      <DialogText v-if="model.ideModel.showFileDialog"></DialogText>
      <DialogDelete v-if="model.ideModel.showDeleteDialog"></DialogDelete>
    </div>
  </div>
</template>

<script>
import BaseCommonTopMenu from './common/BaseCommonTopMenu';
import TopMenu from './editor/TopMenu';
import CodeTab from './editor/CodeTab';
import Console from './editor/Console';
import ConsoleTab from './editor/ConsoleTab';
import CmdRun from './editor/CmdRun';
import ElTree from './editor/ElTree';
import CodeEditor from './editor/CodeEditor';
import DialogProjs from './editor/dialog/DialogProjs';
import DialogText from './editor/dialog/DialogText';
import DialogDelete from './editor/dialog/DialogDelete';

export default {
  i18n: {
    messages: {
      en: {
        ide: 'IDE',
        run: 'Rerun the script pointed to by the current console',
        stop: 'Stop the script or command that the current console is running',
      },
      cn: {
        ide: '集成开发环境',
        run: '重新运行当前控制台指向的脚本',
        stop: '停止当前控制台运行的脚本或命令',
      },
    },
  },
  data() {
    return {
      model: window.GlobalUtil.model,
    }
  },
  mounted() {
    window.addEventListener('resize', this.resize);
    setTimeout(this.model.ideModel.listProjects, 200);
  },
  computed: {
    showConsole() {
      const show = this.model.ideModel.consoleItems.length !== 0;
      this.resize();
      return show;
    }
  },
  methods: {
    selectFile(item) {
      console.log('debug file select: ', item.path)
      this.model.ideModel.selectFilePath = item.path;
      this.model.ideModel.selectNode = item;
      this.model.ideModel.saveProject();
    },
    closeFile(item) {
      console.log('debug file close: ', item.path)
      const codeItems = []
      for (let i = 0; i < this.model.ideModel.codeItems.length; i++) {
        if (item.path !== this.model.ideModel.codeItems[i].path) {
          codeItems.push(this.model.ideModel.codeItems[i])
        }
        else {
          if (i > 0) {
            if (this.model.ideModel.selectFilePath === item.path) {
              this.model.ideModel.selectFilePath = this.model.ideModel.codeItems[i - 1].path;
            }
          }
          else if (i < this.model.ideModel.codeItems.length - 1) {
            if (this.model.ideModel.selectFilePath === item.path) {
              this.model.ideModel.selectFilePath = this.model.ideModel.codeItems[i + 1].path;
            }
          }
        }
      }
      this.model.ideModel.codeItems = codeItems;
      if (codeItems.length === 0) {
        this.model.ideModel.selectFilePath = null;
      }
      this.model.ideModel.saveProject();
    },
    updateItem(path, codemirror) {
      for (let i = 0; i < this.model.ideModel.codeItems.length; i++) {
        if (path === this.model.ideModel.codeItems[i].path) {
          this.model.ideModel.codeItems[i].codemirror = codemirror;
          break;
        }
      }
    },
    selectConsole(item) {
      console.log('debug console select: ', item)
      this.model.ideModel.selectConsoleItem = item;
    },
    closeConsoleSafe(item) {
      console.log('debug console close: ', item)
      if (item.run === true) {
        this.$confirm('Close the tab will stop this program, are you stop?', 'Warning', {
          confirmButtonText: 'Stop and close',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }).then(() => {
          this.model.ideModel.stopPythonProgram(item.id);
          this.closeConsole(item);
        }).catch(() => {
          console.log('canceled close console');
        })
      }
      else {
        this.closeConsole(item);
      }
    },
    closeConsole(item) {
      const consoleItems = []
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (item.name === 'Terminal' && item.path === 'Terminal') {
          if (item.id !== this.model.ideModel.consoleItems[i].id) {
            consoleItems.push(this.model.ideModel.consoleItems[i]);
          }
          else {
            if (i > 0) {
              this.model.ideModel.selectConsoleItem = this.model.ideModel.consoleItems[i - 1];
            }
            else if (i < this.model.ideModel.consoleItems.length - 1) {
              this.model.ideModel.selectConsoleItem = this.model.ideModel.consoleItems[i + 1];
            }
          }
        }
        else {
          if (item.path !== this.model.ideModel.consoleItems[i].path || item.id !== this.model.ideModel.consoleItems[i].id) {
            consoleItems.push(this.model.ideModel.consoleItems[i]);
          }
          else {
            if (i > 0) {
              this.model.ideModel.selectConsoleItem = this.model.ideModel.consoleItems[i - 1];
            }
            else if (i < this.model.ideModel.consoleItems.length - 1) {
              this.model.ideModel.selectConsoleItem = this.model.ideModel.consoleItems[i + 1];
            }
          }
        }
      }
      this.model.ideModel.consoleItems = consoleItems;
      if (this.model.ideModel.consoleItems.length === 0) {
        this.model.ideModel.selectConsoleItem = {};
      }
      this.resize();
    },
    resize() {
      const ele = document.getElementById('left-frame');
      if (ele !== undefined && ele !== null) {
        ele.style.height = `${window.innerHeight - 30}px`;
      }
      for (let i = 0; i < this.model.ideModel.codeItems.length; i++) {
        if (this.model.ideModel.codeItems[i].codemirror !== null) {
          // this.model.ideModel.codeItems[i].codemirror.setSize('auto', this.model.ideModel.consoleItems.length === 0 ? window.innerHeight - 120 : window.innerHeight - 355)
          this.model.ideModel.codeItems[i].codemirror.setSize('auto', this.model.ideModel.consoleItems.length === 0 ? window.innerHeight - 102 : window.innerHeight - 338)
        }
      }
    },
    run() {
      this.model.ideModel.runPythonProgram(this.model.ideModel.selectConsoleItem.id, this.model.ideModel.selectConsoleItem.path);
    },
    stop() {
      if (this.model.ideModel.selectConsoleItem.run === true) {
        this.model.ideModel.stopPythonProgram(this.model.ideModel.selectConsoleItem.id);
      }
    }
  },
  beforeDestroy() {
  },
  components: {
    BaseCommonTopMenu,
    TopMenu,
    CodeTab,
    Console,
    ConsoleTab,
    CmdRun,
    ElTree,
    CodeEditor,
    DialogProjs,
    DialogText,
    DialogDelete,
  }
}
</script>
<style scoped>
.editor-wrapper {
  text-align: left;
}
a {
  color: white;
}
.total-frame {
  /*background-color:gray;*/
  position: fixed;
  width:100%;
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
}
.top-tab {
  width: 100%;
  /* background: #313335; */
  /* background-color: yellow; */
  background: #282828;
}
.left-frame {
  /* width:200px; */
  width: 200px;
  height: 100%;
  overflow-y: auto;
  overflow-x: auto;
  background: #2E3032;
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
  bottom: 210px;
  /* background: #313335; */
  /* background-color: yellow; */
  background: #2f3550ee;
}
.run-icon {
  margin-right: 20px;
  margin-top: 5px;
  width: 16px;
  height: 16px;
  background-image: url('./../assets/img/ide/icon_running.svg');
  cursor: pointer;
}
.stop-icon {
  margin-right: 20px;
  margin-top: 5px;
  width: 16px;
  height: 16px;
  background-image: url('./../assets/img/ide/icon_stop.svg');
  cursor: pointer;
}
.console-frame {
  background-color:#e9e6d3;
  left:0px;
  bottom:0px;
  padding:0px;
  margin:0px;
  /* overflow-y: scroll;
  overflow-x: scroll; */
}
.result-frame {
  /* position: absolute; */
  background-color:#e9e6d3;
  /*position:absolute;*/
  left:0px;
  bottom:0px;
  padding:0px;
  margin:0px;
}
</style>
