
<template>
  <div id="root-dialog" class="noselected">
    <div class="dialog-wrap">
      <div class="dialog-cover" @click="$emit('onCancel')"></div>
      <div class="dialog-content" @click="contentClick">
        <!-- <span class="dialog-top-title">{{ title }}</span> -->
        <div class="dialog-top">
          <span class="dialog-top-title">{{ title }}</span>
        </div>
        <div>
          <input id="ide-input-text" @keyup="$emit('check-input', inputText, updateLegalResult)" v-model="inputText" type="text" class="position-absolute dialog-input input-focus" @keyup.enter="$emit('onCreate')"/>
        </div>
        <div class="position-absolute dialog-error"> {{ tips }} </div>
        <div class="position-absolute" style="bottom:0px;">
          <div class="float-left btn-cancel" @click="$emit('onCancel')">
            取消
          </div>
          <span v-if="isLegal">
            <div class="float-left btn-create cursor-pointer" @click="$emit('onCreate')">
              确定
            </div>
          </span>
          <span v-else>
            <div class="float-left btn-create btn-create-opacity">
              确定
            </div>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: {
    title: String,
    text: String,
    tips: String,
  },
  data() {
    return {
      inputText: this.text,
      isLegal: false,
    }
  },
  mounted() {
    const input = document.getElementById('ide-input-text')
    if (input !== null && input !== undefined) {
      input.focus();
    }
    this.$emit('check-input', this.inputText, this.updateLegalResult);
    // document.onkeydown = this.keyEvent;
  },
  methods: {
    updateLegalResult(legal) {
      this.isLegal = legal;
    },
    keyEvent(e) {
      var eCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
      if (eCode === 13) {
        this.$emit('onCreate');
      }
    },
    contentClick() {
      // console.log(`contentClick contentClick`);
      const optionEle = document.getElementsByClassName('option')[0];
      if (optionEle !== undefined) {
        optionEle.style.display = 'none';
      }
    },
  },
  components: {
  },
  computed: {
  },
}
</script>

<style scoped>
.dialog-top {
  width: 100%;
  height: 40px;
  background: #3F4955;
}
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
  width: 356px;
  position: fixed;
  height: 269px;
  top: 20%;
  left: 0px;
  right: 0px;
  margin-left:auto;
  margin-right:auto;
  z-index: 2000;
  background: #303030;
  overflow: hidden;
}
.dialog-close:hover {
  color: #4fc08d;
}
.dialog-input {
  width:288px;
  height:34px;
  top:113px;
  left:34px;
  padding-left: 15px;
  /* background: #2C2C2C; */
  /* background: yellow; */
  color: white;
  background: #303030;
  border: 0;
  outline:none;
  /* border: 0.02 solid #4E4C4C; */
  background-image: url('~@/assets/img/pop/frame01.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 288px 34px;
}
.dialog-error {
  left:35px;
  top:155px;
  width: 288px;
  font-size: 10px;
  /* color: #878787; */
  color: red;
  font-family: 'Gotham-Book';
}
.dialog-input-ext {
  width:252px;
  /* background: green; */
  background-image: url('~@/assets/img/pop/frame02.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 252px 34px;
}
.dialog-select {
  top:113px;
  left:284px;
  width: 46px;
  height: 34px;
  color: white;
  font-family: 'Gotham-Book';
  font-size: 12px;
  color: #FFFFFF;
  letter-spacing: -0.75px;
  padding-left: 5px;
  padding-top: 10px;
  /* opacity: 0; */
  background-image: url('~@/assets/img/pop/frame03_fileselection.svg');
  background-position: center;
  background-repeat: no-repeat;
}
.dialog-select-origin {
  top:113px;
  left:284px;
}
.dialog-select-bg {
  background-image: url('~@/assets/img/pop/frame03_fileselection.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 46px 34px;
}
.dialog-select-size {
  background-size: 46px 34px;
}
/* .select-toparrow {
  top:10px;
  left:32px;
  width: 7px;
  height: 5px;
  background-image: url('~@/assets/img/pop/toparrowbtns.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 7px 5px
}
.select-bottomarrow {
  top:20px;
  left:32px;
  width: 7px;
  height: 5px;
  background-image: url('~@/assets/img/pop/bottomarrowbtns.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 7px 5px
} */
.select-option {
  background: yellow;
}
.opacity0 {
  opacity: 0;
}
.btn-create-opacity {
  opacity: 0.5;
}
.dialog-add {
  width: 100%;
  height: 100px;
  /* background-color: yellow; */
}
.btn-cancel {
  width: 178px;
  height: 40px;
  background: #484848;
  text-align: center;
  font-family: 'Gotham-Book';
  font-size: 14px;
  color: #7B7B7B;
  letter-spacing: -0.88px;
  line-height: 40px;
  cursor: pointer;
}
.btn-create {
  width: 178px;
  height: 40px;
  background: #52BF53;
  text-align: center;
  font-family: 'Gotham-Book';
  font-size: 14px;
  color: #FFFFFF;
  letter-spacing: -0.88px;
  line-height: 40px;
  /* cursor: pointer; */
}
</style>
