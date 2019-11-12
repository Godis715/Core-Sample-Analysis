<template>
<header>
    <div
        v-for="(linkName, li) in links"
        v-bind:key="'link-' + li">
        <router-link
            v-bind:to="{ name: linkName }"
        >{{linkName}}
        </router-link>
    </div>
    <div>
        <div
            class="nav-btn"
            v-on:click="logout"
        >Logout</div>
    </div>
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
        data() {
            return {
                links: [
                    "Account",
                    "Upload",
                    "Search",
                    "FAQ",
                    "Search"
                ]
            };
        },
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