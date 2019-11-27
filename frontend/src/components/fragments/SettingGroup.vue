<template>
    <div v-if="isMounted">
        <h4>{{title}}</h4>
        <div
            v-for="(setting, index) in settings"
            v-bind:key="index"
        >
            <!-- some settings may have not type because of they are in developing 
            so, it is neccessary to check, if type is defined-->
            <component
                v-if="!!setting.type"
                v-bind:is="setting.type | componentName"
                v-bind="setting"
                v-bind:id="`${id}-setting-${index}`"
                v-on:selected-changed="onchanged($event, index)"
            />
        </div>
    </div>
</template>

<script>
import RadioSetting from "./RadioSetting"
import CheckboxSetting from "./CheckboxSetting"
import ColorSetting from "./ColorSetting"
import NumberSetting from "./NumberSetting"

export default {
    name: "SettingGroup",
    components: { 
        RadioSetting,
        CheckboxSetting,
        ColorSetting,
        NumberSetting
    },
    data() {
        return {
            isMounted: false
        }
    },
    props: [
        "title",
        "settings",
        "id"
    ],
    methods: {
        onchanged(ev, index) {
            this.$emit("setting-changed", {
                data: ev.data,
                settingName: ev.settingName,
                targetIndex: index
            });
        }
    },

    mounted() {
        this.isMounted = true;
    },

    filters: {
        componentName(type) {
            return type + "-setting";
        }
    }
}
</script>