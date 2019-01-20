<template>
  <div class="noselected">
    <div class="">
      <div class="float-left console-tab" name="console-tab" :id="getTabId()" :style="{'background': selected? '#3F4955' : 'transparent'}">
        <div class="float-left console-tab-item-border">
          <div class="float-left" :class="{'tab-left-icon': !selected, 'tab-left-icon-white': selected}" @click="$emit('select-item', item)" :style='{"background-image": "url("+ icon + ")"}'></div>
          <div class="float-left console-tab-item" @click="$emit('select-item', item)">
            <div class="float-left" :class="{'console-tab-background-color-unselect': !selected, 'console-tab-background-color': selected}">{{ selected && !(model.ideModel.selectConsoleItem.name === 'Terminal' && model.ideModel.selectConsoleItem.path === 'Terminal') ? '/' + model.ideModel.curProjTree.name + item.path : item.name }}</div>
          </div>
          <div @click="$emit('close-item', item)" class="float-left" :class="{'tab-cancel': !selected, 'tab-cancel-white': selected}"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: ['item', 'selected'],
  data() {
    return {
      model: window.GlobalUtil.model,
      fileIcon: {
        py: require('@/assets/img/ide/language_python.svg'),
        py2: require('@/assets/img/ide/language-python_white.svg'),
        doc: require('@/assets/img/ide/icon_documents.svg'),
        md: require('@/assets/img/ide/icon_md.svg'),
      },
    };
  },
  methods: {
    getTabId() {
      const uuid = this.item.name;
      return `console-tab-${uuid}`;
    },
  },
  beforeDestroy() {
  },
  watch: {
  },
  computed: {
    icon() {
      if (this.item.path.indexOf('.py') >= 0) {
        if (this.selected) {
          return this.fileIcon.py2;
        }
        return this.fileIcon.py;
      }
      else if (this.item.path.indexOf('.md') >= 0) {
        return this.fileIcon.md;
      }
      else {
        return this.fileIcon.doc;
      }
    }
  },
  components: {
  },
};
</script>

<style scoped>
.console-tab {
  height: 26px;
  line-height: 26px;
  font-family: 'Gotham-Book';
  font-size: 12px;
  color: #A5ACB3;
  letter-spacing: -0.8px;
  /*pointer-events:none;*/
}
.tab-cancel {
  /* background-color:yellow; */
  width: 20px;
  height: 26px;
  text-align:center;
  line-height:26px;
  cursor:pointer;
  background-image: url('./../../assets/img/ide/icon_close.svg');
  background-size: 6px 6px;
  background-repeat: no-repeat;
  background-position: center;
}
.tab-cancel-white {
  /* background-color:yellow; */
  width: 20px;
  height: 26px;
  text-align:center;
  line-height:26px;
  cursor:pointer;
  background-image: url('./../../assets/img/ide/icon_close_white.svg');
  background-size: 6px 6px;
  background-repeat: no-repeat;
  background-position: center;
}
.tab-left-icon {
  margin-left: 8px;
  margin-top: 7px;
  width: 12px;
  height: 12px;
  background-image: url('./../../assets/img/ide/language_python.svg');
  background-size: 12px 12px;
}
.tab-left-icon-white {
  margin-left: 8px;
  margin-top: 7px;
  width: 12px;
  height: 12px;
  background-image: url('./../../assets/img/ide/language-python_white.svg');
  background-size: 12px 12px;
}
.console-tab-item {
  height: 26px;
  padding-left: 10px;
  padding-right: 3px;
}
.console-tab-item-border {
  /* border: solid 1px gray; */
}
.console-tab-background-color {
  /* background-color:pink; */
  color: white;
}
.console-tab-background-color-unselect {
  /* background-color:transparent; */
  color: #A5ACB3;
}
</style>
