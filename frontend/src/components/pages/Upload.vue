<template>
<div>
    <site-header></site-header>
    <div><router-link :to="{name:'Account'}">Account</router-link></div>
</div>
</template>

<script>
    import SiteHeader from '../fragments/Header.vue';

    export default {
        name: 'Upload',
        components: { SiteHeader },
        data() {
            return {
            }
        }
    };
</script>