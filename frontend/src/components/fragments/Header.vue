<template>
<header>
    <div><router-link :to="{name:'Account'}">Account</router-link></div>
    <div><router-link :to="{name:'Upload'}">Upload</router-link></div>
    <div><router-link :to="{name:'Search'}">Search</router-link></div>
    <div><router-link :to="{name:'FAQ'}">FAQ</router-link></div>
    <div><router-link :to="{name:'Search'}">About</router-link></div>
    <div><div class="nav-btn" v-on:click="logout">Logout</div></div>
</header>
</template>

<style>
    header {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        background-color: rgb(245, 245, 245);
        width: 100%;
        font-size: 0.8em;
    }

    header > div {
        margin: 1em 1em;
    }

    a {
        text-decoration: none;
    }

    a:visited, .nav-btn {
        color: rgb(173, 173, 173);
        cursor: pointer;
    }

    a:hover, .nav-btn:hover {
        color: rgb(53, 53, 53);
    } 
</style>

<script>
    export default {
        name: 'site-header',
        methods: {
            logout() {
                let logoutProm = this.$store.dispatch('AUTH_LOGOUT').then(() => {
                    this.$router.push('/login');
                }).catch(err => {
                    console.log(err);
                });

                this.$root.$emit('start-loading', logoutProm);
            }
        }
    };
</script>