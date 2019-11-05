<template>
    <div>
        <h1>{{title}}</h1>
        <div
            v-for="(s, index) in settings"
            v-bind:key="index"
        >
            <radio-setting
                v-if="s.type==='radio'"
                v-bind:title="s.title"
                v-bind:options="s.options"
                v-on:selected-changed="onchanged($event)"
            />
        </div>
    </div>
</template>

<script>
import RadioSetting from "./RadioSetting.vue"

export default {
    name: "SettingGroup",
    components: { RadioSetting },
    props: [
        "title",
        "settings"
    ],
    methods: {
        onchanged(ev) {
            this.$emit("setting-changed", ev);
        }
    }
}
</script>