<template>
<div>
    <site-header></site-header>
    <div><router-link :to="{name:'Upload'}">Upload</router-link></div>
</div>
</template>

<script>
    import SiteHeader from '../fragments/Header.vue';

    export default {
        name: 'Account',
        components: { SiteHeader },
        data() {
            return {

            }
        }
    };
</script>