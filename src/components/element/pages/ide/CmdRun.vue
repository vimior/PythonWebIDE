<template>
  <div class="cmd-div">
    <input
      class="float-left pip-input-text"
      id="pip-install-input-id"
      v-model="inputText"
      placeholder="pip install" />
    <span>
      <div class="run-icon float-right" v-if="!consoleLimit" @click="runCmd()" title="运行命令"></div>
    </span>
  </div>
</template>

<script>
import * as types from '../../../../store/mutation-types';

export default {
  data() {
    return {
      inputText: '',
    };
  },
  mounted() {
    // this.resize();
    // window.addEventListener('resize', this.resize);
  },
  methods: {
    resize() {
      const ele = document.getElementById('pip-install-input-id');
      if (ele !== undefined && ele !== null) {
        ele.style.width = `${window.innerWidth - 235}px`;
      }
    },
    runCmd() {
      if (this.inputText === null || this.inputText === undefined || this.inputText === '') {
        return;
      }

      let selected = false;
      if (this.ideInfo.consoleSelected.run === false && this.ideInfo.consoleSelected.name === 'Terminal' && this.ideInfo.consoleSelected.path === 'Terminal') {
        selected = true;
        this.$store.commit('ide/assignConsoleSelected', {
          stop: false,
          resultList: []
        });
      }
      else {
        for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
          if (this.ideInfo.consoleItems[i].run === false && this.ideInfo.consoleItems[i].name === 'Terminal' && this.ideInfo.consoleItems[i].path === 'Terminal') {
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
          if (this.ideInfo.consoleItems[i].run === false && this.ideInfo.consoleItems[i].name === 'Terminal' && this.ideInfo.consoleItems[i].path === 'Terminal') {
            this.$store.commit('ide/spliceConsoleItems', {start: i, count: 1});
            break;
          }
        }
        const item = {
          name: 'Terminal',
          path: 'Terminal',
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

      // for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
      //   if (this.ideInfo.consoleItems[i].run === false && this.ideInfo.consoleItems[i].name === 'Terminal' && this.ideInfo.consoleItems[i].path === 'Terminal') {
      //     this.$store.commit('ide/spliceConsoleItems', {start: i, count: 1});
      //     break;
      //   }
      // }
      // const item = {
      //   name: 'Terminal',
      //   path: 'Terminal',
      //   resultList: [],
      //   run: false,
      //   stop: false,
      //   id: this.ideInfo.consoleId,
      // }
      // this.$store.commit('ide/addConsoleItem', item);
      // this.$store.commit('ide/setConsoleSelected', item);

      if (!this.ideInfo.consoleItems.includes(this.ideInfo.consoleSelected)) {
        this.$store.commit('ide/addConsoleItem', this.ideInfo.consoleSelected);
      }
      this.$store.dispatch(`ide/${types.IDE_RUN_PIP_COMMAND}`, {
        msgId: this.ideInfo.consoleId,
        command: this.inputText,
        callback: {
          limits: -1,
          callback: (dict) => {
            this.$store.commit('ide/handleRunResult', dict);
          }
        }
      });
      this.$store.commit('ide/setConsoleId', this.ideInfo.consoleId + 1);
    },
  },
  watch: {
  },
  computed: {
    ideInfo() {
      return this.$store.state.ide.ideInfo;
    },
    consoleLimit() {
      let count = 0;
      for (let i = 0; i < this.ideInfo.consoleItems.length; i++) {
        if (this.ideInfo.consoleItems[i].run === true && this.ideInfo.consoleItems[i].name === 'Terminal' && this.ideInfo.consoleItems[i].path === 'Terminal') {
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
  /* left: 200px; */
  bottom: 0px;
  background: #46494B;
}

.pip-input-text {
  /* width:1100px; */
  /* width: calc(100% - 235px); */
  height: 30px;
  border: none;
  background: #46494B;
  color: white;
  /* box-shadow:inset 0 0 0px 0 rgba(255,255,255,0.50); */
  /* top: -5px; */
  /* bottom: 5px; */
  /* padding-left: 10px; */
  outline: none;
}

.run-icon {
  /* margin-right: 1px; */
  /* margin-top: 4px; */
  width: 30px;
  height: 30px;
  background: #3C3F41;
  background-image: url('~@/assets/img/ide/icon_running.svg');
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
  background-image: url('~@/assets/img/ide/icon_stop.svg');
  background-size: 16px 16px;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
}
</style>
