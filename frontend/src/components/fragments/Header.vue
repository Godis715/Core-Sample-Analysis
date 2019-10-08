<template>
<header>
    <div><router-link :to="{name:'Account'}">Account</router-link></div>
    <div><router-link :to="{name:'Search'}">Upload</router-link></div>
    <div><router-link :to="{name:'Search'}">Search</router-link></div>
    <div><router-link :to="{name:'FAQ'}">FAQ</router-link></div>
    <div><router-link :to="{name:'Search'}">About</router-link></div>
    <div><button type="button" v-on:click="logout">Logout</button></div>
</header>
</template>

<script>
    export default {
        name: 'site-header',
        methods: {
            logout() {
                this.$store.dispatch('AUTH_LOGOUT').then(() => {
                    this.$router.push('/login');
                });
            }
        }
    };
</script>