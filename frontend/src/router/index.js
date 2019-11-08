import Vue from 'vue'
import Router from 'vue-router'
// importing pages
import About from '@/components/pages/About'
import Account from '@/components/pages/Account'
import FAQ from '@/components/pages/FAQ'
import Login from '@/components/pages/Login'
import Search from '@/components/pages/Search'
import Upload from '@/components/pages/Upload'
import Viewer from '@/components/pages/Viewer'
import { store } from '@/../store'

Vue.use(Router)

const ifNotAuthenticated = (to, from, next) => {
  // cheking if has NOT auth token
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next('/');
};

const ifAuthenticated = (to, from, next) => {
  // checking if has auth token
  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next('/login');
}

export default new Router({
  mode: 'history',
  routes: [
    {
      // there are button "upload core sample"
      // and also information about previous uploads
      path: '/',
      redirect: '/account'
    },

    // user can view this two pages even if he is not authenticated
    {
      path: '/about',
      name: 'About',
      component: About
    },

    {
      path: '/faq',
      name: 'FAQ',
      component: FAQ
    },

    // only for not-authenticated users
    {
      path: '/login',
      name: 'Login',
      component: Login,
      // checks if user is NOT authenticated
      // if he IS -> redirect to '/'
      beforeEnter: ifNotAuthenticated
    },

    // only for authenticated users:
    {
      path: '/account',
      name: 'Account',
      component: Account,
      // this function checks, if user is authenticated
      // if NOT -> redirect to login page
      beforeEnter: ifAuthenticated
    },

    {
      path: '/search',
      name: 'Search',
      component: Search,
      beforeEnter: ifAuthenticated
    },

    {
      path: '/upload',
      name: 'Upload',
      component: Upload,
      beforeEnter: ifAuthenticated
    },

    {
      path: '/view/:csId',
      name: 'Viewer',
      component: Viewer,
      beforeEnter: ifAuthenticated
    }
  ]
})
