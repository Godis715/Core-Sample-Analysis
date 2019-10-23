<template>
    <div :class="getClass">
        <div>
            <span>{{msgData.text}}</span>
            <div>
                <router-link v-if="msgData.link" :to="msgData.link.where">{{msgData.link.text}}</router-link>
            </div>
        </div>
    </div>
</template>

<style>

</style>

<script>
    export default {
        name: 'Message',
        props: ['msgData'],
        computed: {
            getClass() {
                return 'msg ' + 
                    (this.msgData.type === 'notification' ? 'notif-msg' :
                    this.msgData.type === 'warning' ? 'warn-msg' :
                    this.msgData.type === 'error' ? 'error-msg' :
                    this.msgData.type === 'success' ? 'success-msg' : '');
            }
        }
    };
</script>