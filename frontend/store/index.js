import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    token: localStorage.getItem('user-token') || '',
    status: '',
  },

  getters: {
    isAuthenticated: state => state.token,
    authStatus: state => state.status
  },

  mutations: {
    AUTH_REQUEST: state => {
      state.status = 'loading';
    },

    AUTH_SUCCESS: (state, token) => {
        localStorage.setItem('user-token', token); //sync
        state.token = token;

        state.status = 'success';
    },

    AUTH_ERROR: (state, err) => {
        console.log('Error: ' + err);
        localStorage.removeItem('user-token');
        state.status = 'error';
    },

    AUTH_LOGOUT: state => {
      state.token = undefined;
      localStorage.removeItem('user-token');
    }
  },
  actions: {
    AUTH_REQUEST: async (context, user) => {
        context.commit('AUTH_REQUEST');
        return await axios({ url: 'http://localhost:8000/api/login', data: user, method: 'POST' }).then(resp => {
          context.commit('AUTH_SUCCESS', resp.data.token);
          return { ok: true };
        }).catch(err => {
          context.commit('AUTH_ERROR', err);
          return { ok: false, err: err }
        });
    },

    AUTH_LOGOUT: async context => {
        if (context.state.token) {
          let headers = {};
          if (context.state.token) 
            headers['Authorization'] = `Token ${context.state.token}`;
          
          await axios({ url: 'http://localhost:8000/api/logout', method: 'POST', headers }).then(resp => {
            context.commit('AUTH_LOGOUT');
          }).catch(err => {
            console.error(err);
            context.commit('AUTH_LOGOUT');
          });
        }
    }
  }
});