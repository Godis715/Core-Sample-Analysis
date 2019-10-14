<template>
  <div id="app">
    <progress-bar></progress-bar>
    <router-view/>
  </div>
</template>

<script>
import ProgressBar from './components/fragments/ProgressBar.vue';

export default {
  name: 'App',
  components: { ProgressBar }, 
  created() {
    // checking, if server didn't accept the token
    this.$axios.interceptors.response.use(response => response, async err => {
      if (err.response.status === 401) {
        this.$store.dispatch('AUTH_LOGOUT').then(() => {
          this.$router.push('/login');
        });
      }

      throw err;
    });

    // append token to all headers
    const token = localStorage.getItem('user-token');
    if (token) {
      this.$axios.defaults.headers['Authorization'] = `Token ${token}`;
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
}

body {
  margin: 0;
}
</style>
