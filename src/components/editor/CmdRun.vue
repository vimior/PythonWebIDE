<template>
  <div class="cmd-div">
    <input
      class="float-left pip-input-text"
      id="pip-install-input-id"
      v-model="input"
      placeholder="pip install" />
    <span>
      <div class="run-icon float-right" v-if="!consoleLimit" @click="runCmd()" :title="$t('run')"></div>
    </span>
  </div>
</template>

<script>
export default {
  i18n: {
    messages: {
      en: {
        run: 'Run command',
      },
      cn: {
        run: '运行命令',
      },
    },
  },
  data() {
    return {
      input: '',
      model: window.GlobalUtil.model,
    };
  },
  mounted() {
    this.resize();
    window.addEventListener('resize', this.resize);
  },
  methods: {
    resize() {
      const ele = document.getElementById('pip-install-input-id');
      if (ele !== undefined && ele !== null) {
        ele.style.width = `${window.innerWidth - 240}px`;
      }
    },
    // stopCmd() {
    //   window.CommandsEditorSocket.stopPythonScript(() => {
    //   });
    // },
    runCmd() {
      if (this.input === null || this.input === undefined || this.input === '') {
        return;
      }

      let selected = false;
      if (this.model.ideModel.selectConsoleItem.run === false && this.model.ideModel.selectConsoleItem.name === 'Terminal' && this.model.ideModel.selectConsoleItem.path === 'Terminal') {
        selected = true;
        this.model.ideModel.selectConsoleItem.output = '';
        this.model.ideModel.selectConsoleItem.resultList = [];
      }
      else {
        for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
          if (this.model.ideModel.consoleItems[i].run === false && this.model.ideModel.consoleItems[i].name === 'Terminal' && this.model.ideModel.consoleItems[i].path === 'Terminal') {
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
          if (this.model.ideModel.consoleItems[i].run === false && this.model.ideModel.consoleItems[i].name === 'Terminal' && this.model.ideModel.consoleItems[i].path === 'Terminal') {
            this.model.ideModel.consoleItems.splice(i, 1);
            break;
          }
        }
        const item = {
          name: 'Terminal',
          path: 'Terminal',
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
      //   if (this.model.ideModel.consoleItems[i].run === false && this.model.ideModel.consoleItems[i].name === 'Terminal' && this.model.ideModel.consoleItems[i].path === 'Terminal') {
      //     this.model.ideModel.consoleItems.splice(i, 1)
      //     break;
      //   }
      // }
      // const item = {
      //   name: 'Terminal',
      //   path: 'Terminal',
      //   output: '',
      //   run: false,
      //   id: this.model.ideModel.consoleId,
      // }
      // this.model.ideModel.consoleItems.push(item)
      // this.model.ideModel.selectConsoleItem = item;
      if (!this.model.ideModel.consoleItems.includes(this.model.ideModel.selectConsoleItem)) {
        this.model.ideModel.consoleItems.push(this.model.ideModel.selectConsoleItem)
      }
      this.model.ideModel.runPipCmd(this.model.ideModel.consoleId, this.input);
      this.model.ideModel.consoleId = this.model.ideModel.consoleId + 1;
    },
  },
  beforeDestroy() {
  },
  watch: {
  },
  computed: {
    consoleLimit() {
      let count = 0;
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === true && this.model.ideModel.consoleItems[i].name === 'Terminal' && this.model.ideModel.consoleItems[i].path === 'Terminal') {
          count += 1;
        }
      }
      return count >= 2;
    }
  },
  components: {
  },
};
</script>

<style scoped>

.cmd-div {
  position: fixed;
  /* width: 100%; */
  height: 30px;
  left: 200px;
  bottom: 0px;
  background:#282828;
}

.pip-input-text {
  /* width:1100px; */
  height:30px;
  border:0;
  background:#46494B;
  color:white;
  /* box-shadow:inset 0 0 0px 0 rgba(255,255,255,0.50); */
  /* top: -5px; */
  bottom: 5px;
  padding-left: 10px;
  outline:none;
}

.run-icon {
  /* margin-right: 1px; */
  /* margin-top: 4px; */
  width: 30px;
  height: 30px;
  background: #3C3F41;
  background-image: url('./../../assets/img/ide/icon_running.svg');
  background-size: 16px 16px;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
}

.stop-icon {
  /* margin-right: 1px; */
  /* margin-top: 4px; */
  width: 30px;
  height: 30px;
  background: #3C3F41;
  background-image: url('./../../assets/img/ide/icon_stop.svg');
  background-size: 16px 16px;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
}
</style>
