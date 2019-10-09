<template>
<div>
    <div class="moving" v-if="active"></div>
</div>
</template>

<style>
    .moving {
        animation-duration: 2s;
        animation-name: movement;
        height: 2px;
        position: fixed;
        background-color: gray;
        top: 0;
        left: 0;
    }

    @keyframes movement {
        from { width: 0; }
        to { width: 100%; }
    }
</style>

<script>
    export default {
        name: 'progress-bar',
        data() {
            return {
                active: false
            }
        },
        methods: {
            load(somePromise) {
                this.start();
                return somePromise.then(this.stop).catch(this.stop);
            },

            start() {
                this.active = true;
            },

            stop() {
                this.active = false
            }
        },
        created() {
            this.$root.$on('start-loading', this.load);
        }
    };
</script>