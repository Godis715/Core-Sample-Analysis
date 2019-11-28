<template>
<header>
    <div
        v-for="(linkName, li) in links"
        v-bind:key="'link-' + li"
        v-bind:class="parentComponentName === linkName ? 'current-page' : ''"
    >
        <router-link
            v-bind:to="{ name: linkName }"
        >{{linkName}}
        </router-link>
    </div>
    <div class="logout-cont">
        <div
            class="nav-btn logout"
            v-on:click="logout"
        >Logout</div>
    </div>
</header>
</template>

<style>
    header {
        display: flex;
        flex-direction: row;
        background-color: rgb(245, 245, 245);
        width: 100%;
        font-size: 1.2em;
        font-weight: 600;
    }

    header > div {
        margin: 0.5em;
        padding: 0.5em 1em;
    }

    a {
        text-decoration: none;
    }

    a:visited, a:not(:visited), .nav-btn {
        color: rgb(160, 160, 160);
        cursor: pointer;
    }

    a:hover, .nav-btn:hover {
        color: gray;
    } 

    .current-page {
        background-color: lightgray;
        height: 100%;
    }

    .current-page > a {
        color: gray;
    }

    .logout-cont {
        align-self: flex-end;
    }

    .nav-btn.logout::before {
        background: var(--logout-icon);
        background-repeat: no-repeat;
        background-size: 20px;
        height: 25px;
        width: 20px;
        content: "";
        display: block;
        float: left;
        margin-right: 10px;
        opacity: 0.4;
    }
    .nav-btn.logout:hover::before {
        opacity: 1;
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
                    "About"
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
        },
        computed: {
            parentComponentName() {
                return this.$parent.$options.name;
            }
        }
    };
</script>