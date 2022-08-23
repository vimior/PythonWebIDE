<template>
  <div>
    <!-- <div class="file-path">/{{ ideInfo.currProj.data.name + codeItem.path }}</div> -->
    <mavon-editor :style="{height: height + 'px'}"
      class="v-markdown-editor"
      :toolbarsBackground="'#2B2B2B'"
      :modelValue="codeItemContent"
      :externalLink="false"
      :toolbars="toolbars"
      @change="mdChanged"
    ></mavon-editor>
    <div class="float-clear"></div>
  </div>
</template>

<script>
// mavon-editor
import { mavonEditor } from 'mavon-editor';
import 'mavon-editor/dist/css/index.css';
import * as types from '../../../../../store/mutation-types';
import 'mavon-editor/dist/markdown/github-markdown.min.css';

export default {
  props: {
    codeItem: Object,
    codeItemIndex: Number,
  },
  data () {
    return {
      externalLink: {
        markdown_css: function () {
          return require('mavon-editor/dist/markdown/github-markdown.min.css');
        },
      },
      toolbars: {
        'bold': true,
        'italic': true,
        'header': true,
        'underline': true,
        'strikethrough': true,
        'mark': true,
        'superscript': true,
        'subscript': true,
        'quote': true,
        'ol': true,
        'ul': true,
        'link': true,
        'imagelink': true,
        'code': true,
        'table': true,
        'undo': true,
        'redo': true,
        'trash': true,
        'save': true,
        'alignleft': true,
        'aligncenter': true,
        'alignright': true,
        'navigation': true,
        'subfield': true,
        'fullscreen': false,
        'readmodel': true,
        'htmlcode': true,
        'help': true,
        'preview': true
      }
    }
  },
  mounted() {
  },
  computed: {
    ideInfo() {
      return this.$store.state.ide.ideInfo;
    },
    height() {
      return this.ideInfo.codeHeight + (this.ideInfo.consoleItems.length === 0 ? 30 : 250);
    },
    codeItemContent: {
      get() {
        return this.codeItem.content;
      },
      set(value) {
        this.$store.commit('ide/setCodeItemContent', {index: this.codeItemIndex, content: value}); 
      }
    }
  },
  components: {
    mavonEditor,
  },
  methods: {
    mdChanged(value, render) {
      // this.$store.commit('ide/setCodeItemContent', {index: this.codeItemIndex, content: value});
      this.$store.dispatch(`ide/${types.IDE_WRITE_FILE}`, {
        filePath: this.codeItem.path,
        fileData: value,
        complete: false,
        line: 0,
        column: 0
      });
    },
  }
}
</script>

<style>
.v-note-wrapper {
  position: relative;
  min-width: 200px;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  z-index: 1500;
  text-align: left;
  border: 1px solid #f2f6fc;
  border-radius: 4px;
}
</style>

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
</style>
