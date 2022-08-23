<template>
  <div>
    <markdown-editor v-if="isMarkdown"
      :codeItem="codeItem"
      :codeItemIndex="codeItemIndex">
    </markdown-editor>
    <code-editor v-else
      :codeItem="codeItem"
      :consoleLimit="consoleLimit"
      @run-item="$emit('run-item')"
      :codeItemIndex="codeItemIndex">
    </code-editor>
  </div>
</template>

<script>
import CodeEditor from './editor/CodeEditor';
import MarkdownEditor from './editor/MarkdownEditor';

export default {
  props: {
    codeItem: Object,
    codeItemIndex: Number,
    consoleLimit: Boolean,
  },
  data() {
    return {
    }
  },
  computed: {
    isMarkdown() {
      return this.codeItem.path.endsWith('.md');
    },
  },
  components: {
    CodeEditor,
    MarkdownEditor
  }
}
</script>