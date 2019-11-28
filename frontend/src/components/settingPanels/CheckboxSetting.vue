<template>
<form v-on:change="onchanged">
    <h4>{{title}}</h4>
    <div>
        <input
            v-model="checked"
            type="checkbox"
            name="checkbox"
        />
        <label>Enabled</label>
    </div>
</form>
</template>

<script>
export default {
    name: "CheckboxSetting",
    props: [
        "title",
        "options",
        "settingName",
        "value"
    ],
    data() {
        return {
            checked: undefined
        }
    },
    methods: {
        onchanged() {
            this.$emit("selected-changed", {
                data: this.checked,
                settingName: this.settingName
            });
        }
    },

    created() {
        this.checked = this.value;
    },

    watch: {
        value() {
            this.checked = this.value;
        }
    }
}
</script>