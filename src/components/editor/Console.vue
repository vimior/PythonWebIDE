<template>
  <div class="console-div">
    <textarea
      :id="'console-'+item.id"
      type="textarea"
      class="console-area"
      v-model="item.output">
    </textarea>
  </div>
</template>

<script>
export default {
  props: {
    item: Object,
  },
  mounted() {
    document.getElementById('console-' + this.item.id).style.width = `${window.innerWidth - 205}px`;
    window.addEventListener('resize', this.resize);
  },
  methods: {
    resize() {
      document.getElementById('console-' + this.item.id).style.width = `${window.innerWidth - 205}px`;
    }
  }
}
</script>

<style scoped>
.console-div {
  position: fixed;
  width: 100%;
  height: 210px;
  left: 200px;
  bottom: 0px;
}
.console-area {
  background: #313131;
  /* width: 70%; */
  color: white;
  /* width: 200px; */
  border: 0;
  height: 200px;
  /* height: 100%; */
  /* bottom: 10px; */
  overflow-y: auto;
  /* overflow-x: auto;
  overflow-y: auto; */
}
</style>


