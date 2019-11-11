<template>
<form v-if="isMounted" v-on:change="onchanged">
    <h4>{{title}}</h4>
    <div 
        v-for="(item, index) in options"
        v-bind:key="index"
    >
        <input
            type="radio"
            name="radio"
            v-bind:value="item.value"
            v-model="selected"
            v-bind:id="`${id}-input-${index}`"
     />
        <label v-bind:for="`${id}-input-${index}`">{{item.name}}</label>
    </div>
</form>
</template>

<script>

export default {
    name: "RadioSetting",
    props: [
        "title",
        "options",
        "settingName",
        "value",
        "id"
    ],
    data() {
        return {
            selected: undefined,
            isMounted: false
        }
    },
    methods: {
        onchanged() {
            this.$emit("selected-changed", {
                data: this.selected,
                settingName: this.settingName
            });
        }
    },

    created() {
        this.selected = this.value;
    },

    mounted() {
        this.isMounted = true;
    },

    watch: {
        value() {
            this.selected = this.value;
        }
    }
}
</script>