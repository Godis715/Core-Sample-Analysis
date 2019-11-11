<template>
    <div>
        <h4>{{title}}</h4>
        <div
            v-for="(s, index) in settings"
            v-bind:key="index"
        >
            <radio-setting
                v-if="s.type==='radio'"
                v-bind:title="s.title"
                v-bind:settingName="s.settingName"
                v-bind:options="s.options"
                v-bind:value="s.value"
                v-on:selected-changed="onchanged($event, index)"
            />

            <checkbox-setting 
                v-if="s.type==='checkbox'"
                v-bind:title="s.title"
                v-bind:settingName="s.settingName"
                v-bind:options="s.options"
                v-bind:value="s.value"
                v-on:selected-changed="onchanged($event, index)"
            />
        </div>
    </div>
</template>

<script>
import RadioSetting from "./RadioSetting"
import CheckboxSetting from "./CheckboxSetting"

export default {
    name: "SettingGroup",
    components: { 
        RadioSetting,
        CheckboxSetting
    },
    props: [
        "title",
        "settings"
    ],
    methods: {
        onchanged(ev, index) {
            this.$emit("setting-changed", {
                data: ev.data,
                settingName: ev.settingName,
                targetIndex: index
            });
        }
    }
}
</script>