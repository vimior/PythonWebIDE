<template>
  <div>
    <div class="file-path">/{{ model.ideModel.curProjTree.name + item.path }}</div>
    <codemirror
      v-model="item.content"
      style="width:100%;"
      id="codemirror-id"
      :options="editorOptions"
      ref="codeEditor">
    </codemirror>
    <div class="float-clear"></div>
  </div>
</template>

<script>
import { codemirror, CodeMirror } from 'vue-codemirror';
// import { codemirror2, CodeMirror2 } from 'vue-codemirror';
import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/monokai.css';
import 'codemirror/addon/hint/show-hint';
import 'codemirror/addon/hint/show-hint.css';
import 'codemirror/addon/hint/javascript-hint';
import 'codemirror/mode/python/python';
import 'codemirror/addon/selection/active-line';
import 'codemirror/addon/edit/matchbrackets';
import 'codemirror/addon/edit/closebrackets';
import 'codemirror/addon/fold/foldgutter';
import 'codemirror/addon/fold/foldgutter.css';
import 'codemirror/addon/display/fullscreen';
import 'codemirror/addon/display/fullscreen.css';
import PythonHint from '@/assets/lib/python-hint';
import '@/assets/codemirror/theme/monokai-sublime.css';

export default {
  props: {
    item: Object,
    // showConsole: Boolean,
  },
  data () {
    return {
      text: 'hello',
      complete_prefix: '',
      model: window.GlobalUtil.model,
      editorOptions: {
        mode: {
          name: 'python',
          version: 3,
          singleLineStringErrors: false,
        },
        tabSize: 4,
        theme: 'monokai',
        extraKeys: {
          Tab: function(cm) {
            var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
            cm.replaceSelection(spaces);
          },
          // Tab: (cm) => {
          //   const cursor = this.codemirror.getCursor();
          //   const line = this.codemirror.getLine(cursor.line);
          //   let list = line.split(' ');
          //   list = list[list.length - 1].split('.');
          //   const self = this;
          //   self.complete_prefix = list[list.length - 1];
          //   self.model.ideModel.autocompletePython(self.codemirror.getValue(), cursor.line, cursor.ch, (dict) => {
          //     const completeDatas = dict.data;
          //     // console.log(`completeDatas = ${JSON.stringify(completeDatas)}`);
          //     const prefix = [];
          //     if (self.complete_prefix !== '.' && self.complete_prefix !== '*' && self.complete_prefix !== '?' && self.complete_prefix !== '+') {
          //       prefix.push(self.complete_prefix);
          //     }
          //     let allDatas = PythonHint.concat(completeDatas).concat(prefix);
          //     allDatas = self.model.ideModel.uniqueArr(allDatas);
          //     CodeMirror.registerHelper('hintWords', 'python', allDatas);
          //     cm.showHint({ hint: CodeMirror.hint.anyword })
          //   });
          // },
          // F11键切换全屏
          F11: (cm) => {
            console.log('F11');
            cm.setOption('fullScreen', !cm.getOption('fullScreen'));
          },
          // Esc键退出全屏
          Esc: (cm) => {
            console.log('Esc');
            cm.setOption('fullScreen', !cm.getOption('fullScreen'));
            // if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
          },
        },
        styleSelectedText: true,
        styleActiveLine: true,
        highlightSelectionMatches: { showToken: /\w/, annotateScrollbar: true },
        lineNumbers: true,
        line: true,
        lineWrapping: true,
        smartIndent: true,
        indentUnit: 4,
        showCursorWhenSelecting: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        foldGutter: true,
        gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
      }
    }
  },
  mounted() {
    this.$emit('update-item', this.item.path, this.codemirror);
    // this.codemirror.setSize('auto', this.model.ideModel.consoleItems.length === 0 ?  window.innerHeight - 120 : window.innerHeight - 355);
  },
  computed: {
    codemirror() {
      return this.$refs.codeEditor.codemirror;
    },
  },
  watch: {
    'item.content': {
      handler(curVal, oldVal) {
        const self = this;
        const cursor = self.codemirror.getCursor();
        const line = self.codemirror.getLine(cursor.line);
        let list = line.split(' ');
        list = list[list.length - 1].split('.');
        self.complete_prefix = list[list.length - 1];
        if (cursor.ch === 0 || !self.complete_prefix || self.complete_prefix.endsWith(':') || self.complete_prefix.endsWith(')')) {
          this.model.ideModel.writeFile(this.item.path, curVal, false);
          return;
        }
        this.model.ideModel.writeFile(this.item.path, curVal, true, cursor.line, cursor.ch, (dict) => {
          const completeDatas = dict.data;
          // console.log(`completeDatas = ${JSON.stringify(completeDatas)}`);
          const prefix = [];
          if (self.complete_prefix !== '.' && self.complete_prefix !== '*' && self.complete_prefix !== '?' && self.complete_prefix !== '+') {
            prefix.push(self.complete_prefix);
          }
          let allDatas = PythonHint.concat(completeDatas).concat(prefix);
          allDatas = self.model.ideModel.uniqueArr(allDatas);
          CodeMirror.registerHelper('hintWords', 'python', allDatas);
          self.codemirror.showHint({ hint: CodeMirror.hint.anyword })
        });
        // self.model.ideModel.autocompletePython(self.codemirror.getValue(), cursor.line, cursor.ch, (dict) => {
        //   const completeDatas = dict.data;
        //   // console.log(`completeDatas = ${JSON.stringify(completeDatas)}`);
        //   const prefix = [];
        //   if (self.complete_prefix !== '.' && self.complete_prefix !== '*' && self.complete_prefix !== '?' && self.complete_prefix !== '+') {
        //     prefix.push(self.complete_prefix);
        //   }
        //   let allDatas = PythonHint.concat(completeDatas).concat(prefix);
        //   allDatas = self.model.ideModel.uniqueArr(allDatas);
        //   CodeMirror.registerHelper('hintWords', 'python', allDatas);
        //   self.codemirror.showHint({ hint: CodeMirror.hint.anyword })
        // });
        self.model.ideModel.projElTree.setCurrentKey(self.model.ideModel.selectFilePath)
        self.model.ideModel.selectNode = this.model.ideModel.projElTree.getCurrentNode();
      }
    }
  },
  components: {
    codemirror,
  },
  methods: {
    // onEditorCodeChange(newCode) {
    //   console.log('editor change', newCode);
    //   this.model.ideModel.projElTree.setCurrentKey(this.model.ideModel.selectFilePath)
    //   this.model.ideModel.selectNode = this.model.ideModel.projElTree.getCurrentNode();
    // },
  }
}
</script>

<style scoped>
.file-path {
  color: lightblue;
  font-size: 12px;
  background-color: rgba(255, 250, 226, 1.0);
  width: 100%;
  background: #2E3032;
  color: #50E3C2;
  font-family: 'Gotham-Book';
}
.CodeMirrorOveride {
  border: 1px solid #eee;
  height: 10px;
}
</style>
