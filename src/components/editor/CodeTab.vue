<template>
  <div class="noselected">
    <div class="">
      <div class="float-left top-tab" name="top-tab" :id="getTabId()" :style="{'background': selected? '#3F4955' : 'transparent'}">
        <div class="float-left top-tab-item-border">
          <div class="float-left" :class="{'tab-left-icon': !selected, 'tab-left-icon-white': selected}" @click="$emit('select-item', item)"></div>
          <div class="float-left top-tab-item" @click="$emit('select-item', item)">
            <div class="float-left" :class="{'top-tab-background-color-unselect': !selected, 'top-tab-background-color': selected}">{{ item.name }}</div>
          </div>
          <div @click="$emit('close-item', item)" class="float-left" :class="{'tab-cancel': !selected, 'tab-cancel-white': selected}"></div>
        </div>
        <!-- <hr width="0.1px" size="20px" color="red"> -->
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: ['item', 'selected'],
  data() {
    return {
    };
  },
  methods: {
    getTabId() {
      const uuid = this.item.name;
      return `top-tab-${uuid}`;
    },
  },
  beforeDestroy() {
  },
  watch: {
  },
  computed: {
  },
  components: {
  },
};
</script>

<style scoped>
.top-tab {
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
.top-tab-item {
  height: 26px;
  padding-left: 10px;
  padding-right: 3px;
}
.top-tab-item-border {
  /* border: solid 1px gray; */
}
.top-tab-background-color {
  /* background-color:pink; */
  color: white;
}
.top-tab-background-color-unselect {
  /* background-color:transparent; */
  color: #A5ACB3;
}
</style>
