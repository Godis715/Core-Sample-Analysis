<template>
<form v-on:change="onchanged">
    <h2>{{title}}</h2>
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
        "default"
    ],
    data() {
        return {
            checked: false
        };
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
        if (this.default !== undefined) {
            this.checked = this.default;
        }
    }
}
</script>