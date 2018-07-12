
<template>
  <div id="root-dialog" class="noselected">
    <div class="dialog-wrap">
      <div class="dialog-cover" @click="closeMyself"></div>
      <div class="dialog-content" @click="contentClick">
        <span class="top-title">{{ model.ideModel.dialogTitle }}</span>
        <div>
          <input id="ide-input-text" v-model="model.ideModel.dialogInputText" type="text" class="position-absolute dialog-input input-focus" />
        </div>
        <div class="position-absolute dialog-error"> {{ model.ideModel.dialogTips }} </div>
        <div class="position-absolute" style="bottom:0px;">
          <div class="float-left btn-cancel" @click="closeMyself">
            Cancel
          </div>
          <span v-if="checkInput">
            <div class="float-left btn-create cursor-pointer" @click="oncreate">
              OK
            </div>
          </span>
          <span v-else>
            <div class="float-left btn-create btn-create-opacity">
              OK
            </div>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

const path = require('path')

export default {
  data() {
    return {
      model: window.GlobalUtil.model,
    }
  },
  mounted() {
    const input = document.getElementById('ide-input-text')
    if (input !== null && input !== undefined) {
      input.focus();
    }
    document.onkeydown = this.keyEvent;
  },
  methods: {
    keyEvent(e) {
      var eCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
      if (eCode === 13) {
        this.oncreate();
      }
    },
    contentClick() {
      // console.log(`contentClick contentClick`);
      const Option = document.getElementsByClassName('option')[0];
      if (Option !== undefined) {
        Option.style.display = 'none';
      }
    },
    closeMyself() {
      this.model.ideModel.showFileDialog = false;
      if (this.model.ideModel.selectNode !== null) {
        this.model.ideModel.projElTree.setCurrentNode(this.model.ideModel.selectNode);
      }
    },
    oncreate() {
      const text = this.model.ideModel.dialogInputText;
      if (this.model.ideModel.dialogType === 'create-file') {
        this.model.ideModel.createFile(text);
      }
      else if (this.model.ideModel.dialogType === 'rename-file') {
        this.model.ideModel.renameFile(text);
      }
      else if (this.model.ideModel.dialogType === 'create-folder') {
        this.model.ideModel.createFolder(text);
      }
      else if (this.model.ideModel.dialogType === 'rename-folder') {
        this.model.ideModel.renameFolder(text);
      }
      else if (this.model.ideModel.dialogType === 'create-project') {
        if (this.hasRunProgram()) {
          this.$confirm('Are you stop all program and create a new project?', 'Warning', {
            confirmButtonText: 'Stop and create',
            cancelButtonText: 'Cancel',
            type: 'warning',
          }).then(() => {
            this.stopAll();
            this.model.ideModel.consoleItems = [];
            this.model.ideModel.createProject(text);
          }).catch(() => {
            console.log('canceled create project');
          })
        }
        else {
          this.model.ideModel.consoleItems = [];
          this.model.ideModel.createProject(text);
        }
      }
      else if (this.model.ideModel.dialogType === 'rename-project') {
        this.model.ideModel.renameProject(text);
      }
      this.model.ideModel.showProjsDialog = false;
      this.model.ideModel.showFileDialog = false;
      this.model.ideModel.showDeleteDialog = false;
    },
    hasRunProgram() {
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === true) {
          return true;
        }
      }
      return false;
    },
    stopAll() {
      for (let i = 0; i < this.model.ideModel.consoleItems.length; i++) {
        if (this.model.ideModel.consoleItems[i].run === true) {
          this.model.ideModel.stopPythonProgram(this.model.ideModel.consoleItems[i].id);
        }
      }
    },
  },
  components: {
  },
  computed: {
    checkInput() {
      // const isFileStr = window.GlobalUtil.isFileStr(this.model.ideModel.dialogInputText);
      const text = this.model.ideModel.dialogInputText;
      const dialogType = this.model.ideModel.dialogType;
      let isLegal = this.model.utilModel.checkStrIsLegal(text, dialogType === 'create-file' || dialogType === 'rename-file');
      if (isLegal !== true && isLegal !== false) {
        this.model.ideModel.dialogTips = isLegal;
        isLegal = false;
      }
      if (!isLegal) {
        return false;
      }

      if (dialogType === 'create-project' || dialogType === 'rename-project') {
        const isHasProj = this.model.ideModel.isHasProj(text);
        return isLegal && !isHasProj;
      }
      else if (dialogType === 'create-file' || dialogType === 'rename-file' || dialogType === 'create-folder' || dialogType === 'rename-folder') {
        const isRpeat = this.model.ideModel.isRepeatFile(text, dialogType === 'create-file' || dialogType === 'create-folder');
        return isLegal && !isRpeat;
      }
    },
  },
}
</script>

<style scoped>
.top-title {
  position: absolute;
  left: 24px;
  top: 25px;
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
  z-index: 10;
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
  background-image: url('./../../../assets/img/pop/frame01.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 288px 34px;
}
.dialog-error {
  left:35px;
  top:155px;
  width: 288px;
  font-size: 10px;
  color: #878787;
  font-family: 'Gotham-Book';
}
.dialog-input-ext {
  width:252px;
  /* background: green; */
  background-image: url('./../../../assets/img/pop/frame02.svg');
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
  background-image: url('./../../../assets/img/pop/frame03_fileselection.svg');
  background-position: center;
  background-repeat: no-repeat;
}
.dialog-select-origin {
  top:113px;
  left:284px;
}
.dialog-select-bg {
  background-image: url('./../../../assets/img/pop/frame03_fileselection.svg');
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
  background-image: url('./../assets/img/pop/toparrowbtns.svg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: 7px 5px
}
.select-bottomarrow {
  top:20px;
  left:32px;
  width: 7px;
  height: 5px;
  background-image: url('./../assets/img/pop/bottomarrowbtns.svg');
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
