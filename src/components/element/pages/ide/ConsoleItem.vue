<template>
  <div class="console-div">
    <div class="console-sidebar">
      <div class="run-icon float-right" v-if="item.run === false && !(item.name === 'Terminal' && item.path === 'Terminal')" @click="$emit('run-item')" title="重新运行当前控制台指向的脚本"></div>
      <div class="stop-icon float-right" v-if="item.run === true" @click="$emit('stop-item', item.id)" title="停止当前控制台运行的脚本或命令"></div>
    </div>
    <textarea
      readonly="readonly"
      :id="'console-'+item.id"
      type="textarea"
      class="console-area"
      :value="content"
      @input="$emit('input', $event.target.value)">
    </textarea>
  </div>
</template>

<script>
export default {
  props: {
    item: Object,
  },
  mounted() {
    // this.resize();
    // window.addEventListener('resize', this.resize);
  },
  computed: {
    content() {
      if (this.item.run && this.item.resultList.length >= 20) {
        return this.item.resultList.slice(this.item.resultList.length - 20).join('\n') + '\n';
      }
      else {
        return this.item.resultList.join('\n') + '\n';
      }
    }
  },
  watch: {
    content(cur, old) {
      this.scroll();
    }
  },
  methods: {
    scroll() {
      const textArea = document.getElementById('console-' + this.item.id)
      if (textArea !== undefined && textArea !== null) {
        textArea.scrollTop = textArea.scrollHeight;
      }
    },
    resize() {
      const ele= document.getElementById('console-' + this.item.id)
      if (ele !== undefined && ele !== null) {
        ele.style.width = `${window.innerWidth - 225}px`;
      }
    }
  }
}
</script>

<style scoped>
.console-div {
  position: fixed;
  width: 100%;
  height: 200px;
  left: 200px;
  bottom: 31px;
  display: inline-flex;
  /* width: calc(100% - 205px); */
}
.console-sidebar {
  width: 20px;
  height: 200px;
  background: #3A3D41;
}
.console-area {
  /* background: #313131; */
  background: #232323;
  /* width: 70%; */
  color: white;
  /* width: 200px; */
  /* border: 1px #e1e4e8 solid; */
  border: 0px solid black;
  outline: none;
  resize: none;
  width: calc(100% - 225px);
  height: 200px;
  /* height: 100%; */
  /* bottom: 10px; */
  overflow-x: auto;
  overflow-y: auto;
}
.run-icon {
  margin-right: 3px;
  margin-top: 2px;
  width: 16px;
  height: 16px;
  background-image: url('./../../../../assets/img/ide/icon_running.svg');
  cursor: pointer;
}
.stop-icon {
  margin-right: 3px;
  margin-top: 2px;
  width: 16px;
  height: 16px;
  background-image: url('./../../../../assets/img/ide/icon_stop.svg');
  cursor: pointer;
}

.console-area::-webkit-scrollbar {/*滚动条整体样式*/
  width: 5px;     /* 高宽分别对应横竖滚动条的尺寸 */
  height: 5px;
}
.console-area::-webkit-scrollbar-thumb {/*滚动条里面小方块*/
  /* background: #87939A; */
  background: #545a5e;
}
.console-area::-webkit-scrollbar-track {/*滚动条里面轨道*/
  background: #2F2F2F;
}
</style>


