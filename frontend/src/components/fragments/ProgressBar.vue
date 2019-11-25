<template>
<div>
    <div
        v-bind:class="'upper-progress-bar ' + barClass" 
    ></div>
</div>
</template>

<style>
    .upper-progress-bar {
        background-color:rgb(36, 170, 54);
        position: fixed;
        height: 0;
        width: 0;
        top: 0;
        left: 0;
    }

    .moving {
        transition: 250ms;
        animation-duration: 1s;
        animation-name: movement;
        height: 2px;
    }

    @keyframes movement {
        from { width: 0; }
        to { width: 100%; }
    }

    .finishing { 
        width: 100%;
        height: 2px; 
    }
</style>

<script>
    export default {
        name: "ProgressBar",
        data() {
            return {
                active: false,
                finishing: false
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
                this.active = false;
                this.finishing = true;
                setTimeout(() => {
                    this.finishing = false;
                }, 500);
            }
        },
        created() {
            this.$root.$on('start-loading', this.load);
        },
        computed: {
            barClass() {
                if (this.active) {
                    return "moving";
                } else if (this.finishing) {
                    return "finishing";
                } else {
                    return "";
                }
            }
        }
    };
</script>