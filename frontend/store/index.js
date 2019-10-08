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
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status
  },

  mutations: {
    AUTH_REQUEST: state => {
        state.status = 'loading';
    },

    AUTH_SUCCESS: (state, token) => {
        localStorage.setItem('user-token', token); //sync
        axios.defaults.headers.common['Authorization'] = token;
        state.status = 'success';
        state.token = token;
    },

    AUTH_ERROR: (state, err) => {
        localStorage.removeItem('user-token');
        state.status = 'error';
    },

    AUTH_LOGOUT: state => {
        localStorage.removeItem('user-token');
    }
  },
  actions: {
    AUTH_REQUEST: async (context, user) => {
        context.commit('AUTH_REQUEST');
        return await axios({ url: '/login', data: user, method: 'POST' }).then(resp => {
            context.commit('AUTH_SUCCESS', resp.data.token);
        }).catch(err => {
            context.commit('AUTH_ERROR', err);
        });
    },

    AUTH_LOGOUT: async context => {
        context.commit('AUTH_LOGOUT');
    }
  }
});