<template>
<form v-on:change="onchanged">
    <h2>{{title}}</h2>
    <div 
        v-for="(item, index) in options"
        v-bind:key="index"
    >
        <input
            type="radio"
            name="radio"
            v-bind:value="item.value"
            v-model="selected"
     />
        <label>{{item.name}}</label>
    </div>
</form>
</template>

<script>
export default {
    name: "RadioSetting",
    props: [
        "title",
        "options"
    ],
    data() {
        return {
            selected: ""
        };
    },
    methods: {
        onchanged() {
            this.$emit("selected-changed", this.selected);
        }
    }
}
</script>