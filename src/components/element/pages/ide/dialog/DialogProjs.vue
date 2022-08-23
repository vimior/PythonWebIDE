<template>
  <div class="dialog-wrap">
    <div class="dialog-cover" @click="$emit('onCancel')"></div>
    <div class="dialog-content">
      <div class="dialog-top">
        <span class="dialog-top-title">请选择一个项目</span>
        <div class="dialog-close" @click="$emit('onCancel')">
        </div>
      </div>
      <table>
        <tr>
          <th class="dialog-table-head">工程名</th>
          <th class="dialog-table-head">时间</th>
          <th class="dialog-table-head">选项</th>
        </tr>
      </table>
      <div class="dialog-table">
        <table>
          <template v-for="data in ideInfo.projList" :key="data.name">
            <tr @dblclick="$emit('onSelect', data.name)">
              <td>{{ data.name }}</td>
              <td>{{ data.ctime }}</td>
              <td>
                <div class="float-left proj-selected" v-if="ideInfo.currProj.data.name === data.name"></div>
                <div class="float-left proj-open" v-if="ideInfo.currProj.data.name !== data.name" @click="$emit('onSelect', data.name)">打开</div>
                <!-- btn_trash.svg -->
                <div class="proj-icon-trash float-left" v-if="ideInfo.currProj.data.name !== data.name" @click="$emit('onDelete', data.name)"></div>
              </td>
            </tr>
          </template>
        </table>
      </div>
      <div class="dialog-add">
        <div class="dialog-add-content" @click="showCreateProjDialog">
          <span>+</span>
          <span>新建项目</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
    }
  },
  computed: {
    ideInfo() {
      return this.$store.state.ide.ideInfo;
    },
  },
  methods: {
    showCreateProjDialog() {
      this.$emit('setTextDialog', {
        type: 'create-project',
        title: '新建工程名',
        text: '',
        tips: ''
      });
    }
  },
}
</script>

<style scoped>
.dialog-top-title {
  position: absolute;
  left: 24px;
  top: 8px;
  /* height: 67px; */
  font-family: 'Gotham-Medium';
  font-size: 16px;
  color: #FFFFFF;
  letter-spacing: -1px;
  /* background-color: yellow; */
  /* line-height: 16px; */
}
.dialog-content {
  width: 580px;
  position: fixed;
  height: 340px;
  top: 20%;
  left: 0px;
  right: 0px;
  margin-left:auto;
  margin-right:auto;
  z-index: 1999;
  background: #303030;
  overflow: hidden;
}
.dialog-top {
  width: 100%;
  height: 40px;
  background: #3F4955;
}
.dialog-table {
  /* width: 100%; */
  width: 600px;
  height: 140px;
  overflow-y: scroll;
}
.dialog-table-head {
  width: 194px;
  height: 66px;
  /* font-family: 'Gotham-Medium'; */
  font-size: 16px;
  color: #FFFFFF;
  letter-spacing: -1px;
  text-align: center;
  line-height: 16px;
}
.dialog-table td {
  width: 194px;
  height: 40px;
  /* font-family: 'Gotham-Book'; */
  font-size: 12px;
  color: #FFFFFF;
  padding-left: 50px;
  letter-spacing: -0.38px;
  /* text-align: center; */
  line-height: 12px;
}
.dialog-table tr:hover {
  background: rgba(255, 255, 255, 0.1);
}
.dialog-table tr:hover td {
  /* color: black; */
  font-size: 13px;
}
.dialog-close {
  position: absolute;
  right: 10px;
  top: 10px;
  width: 20px;
  height: 20px;
  text-align: center;
  cursor: pointer;
  background-position: center;
  background-image: url('~@/assets/img/pop/icon_close.svg');
  background-size: 10px 11px;
  background-repeat: no-repeat;
}
.dialog-close:hover {
  color: #4fc08d;
}
.dialog-add {
  width: 100%;
  height: 100px;
  /* background-color: yellow; */

}
.dialog-add-content {
  position: absolute;
  bottom: 16px;
  left: 0;
  right: 0;
  margin: auto;
  /* background-color: yellow; */
  width: 496px;
  height: 26px;
  font-family: 'Gotham-Book';
  text-align: center;
  line-height: 10px;
  letter-spacing: -0.5px;
  color: #FFFFFF;
  padding-top: 8px;
  border:1px dashed #5C5C5C;
  cursor: pointer;
}
.proj-icon-trash {
  margin-left: 20px;
  width: 30px;
  height: 30px;
  background-image: url('~@/assets/img/pop/btn_trash.svg');
  background-size: 8px 10px;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
}
.proj-open {
  font-family: 'Gotham-Book';
  font-size: 12px;
  color: #FFFFFF;
  letter-spacing: -0.38px;
  line-height: 26px;
  height: 26px;
  margin-left: 10px;
  cursor: pointer;
}
.proj-selected {
  width: 30px;
  height: 30px;
  margin-left: 10px;
  background-image: url('~@/assets/img/pop/icon_select.svg');
  background-size: 16px 16px;
  background-repeat: no-repeat;
  background-position: center;
}
</style>
