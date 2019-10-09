<template>
  <div id="app">
    <progress-bar></progress-bar>
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios'
import ProgressBar from './components/fragments/ProgressBar.vue';

export default {
  name: 'App',
  components: { ProgressBar }, 
  created() {
    // checking, if server didn't accept the token
    axios.interceptors.response.use(undefined, async err => {
      if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
        this.$store.dispatch('AUTH_LOGOUT');
        this.$router.push('/login');
      }
      throw err;
    });

    // append token to all headers
    const token = localStorage.getItem('user-token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = token;
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
