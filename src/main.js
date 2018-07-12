// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui';
import VueI18n from 'vue-i18n';
import 'element-ui/lib/theme-chalk/index.css';
import GlobalUtil from '@/store/core/global_util';
window.GlobalUtil = GlobalUtil;
import store from './store';
import App from './App'
import router from './router'
require('@/assets/css/common.css');

Vue.use(ElementUI);
Vue.use(VueI18n);

Vue.config.productionTip = false

const i18n = new VueI18n({
  locale: 'en',
  silentTranslationWarn: true,
  messages: {
    en: require('@/assets/i18n/en'),
    cn: require('@/assets/i18n/cn'),
  },
});

/* eslint-disable no-new */
new Vue({
  i18n,
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
