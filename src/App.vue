<template>
  <div id="app" class="app-root">
    <!-- <img src="./assets/logo.png"> -->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    window.GlobalUtil.store = this.$store;
    this.$store.dispatch('openWebsocket');
  },
}
</script>

<style scoped lang="scss">
.app-root {
  display: flex;
}

.app-panel {
  position: absolute;
  z-index: 90000;
  background: black;
  top: 60px;
  width: 60px;
  height: 600px;
  color: white;
  .app-home {
    width: 100%;
    height: 40px;
    cursor: pointer;
  }
  .app-ctrl {
    width: 100%;
    height: 40px;
    cursor: pointer;
  }
  .app-blockly {
    width: 100%;
    height: 40px;
    cursor: pointer;
  }
  .app-ide {
    width: 100%;
    height: 40px;
    cursor: pointer;
  }
  .app-paint {
    width: 100%;
    height: 40px;
    cursor: pointer;
  }
  .app-recording {
    width: 100%;
    height: 40px;
    cursor: pointer;
  }
  .app-menu {
    position: absolute;
    width: 100%;
    height: 40px;
    bottom: 0px;
    cursor: pointer;
  }
}

.app-menu-bg-selected {
  background: gray;
}
