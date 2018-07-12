<template>
  <div id="root-menu" class="noselected">
    <div class="base-header-wrapper com-header-wrapper">
      <div>
        <span class="back-title"> {{ backTitle }} </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'base-common-top-menu',
  props: ['backTitle'],
  data() {
    return {
    }
  },
  mounted() {
  },
  beforeDestroy() {
  },
  methods: {
  },
  components: {
  },
  computed: {
  },
  watch: {
  },
}
</script>

<style scoped lang="scss">
.base-header-wrapper {
  background: #F8F8F8;
  display: flex;
  justify-content: space-between;
  align-items: center;
  .back-title {
    margin-left: 1rem;
    font-family: 'Gotham-Bold';
    font-size: 18px;
    color: #444;
    letter-spacing: -1px;
  }
}
</style>
