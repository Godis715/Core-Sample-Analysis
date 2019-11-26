// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import {store} from '../store'

import axios from 'axios';
Vue.prototype.$axios = axios.create({
  baseURL: `${process.env.API_URL}:${process.env.API_PORT}/`
});

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  axios,
  components: { App },
  template: '<App/>'
})