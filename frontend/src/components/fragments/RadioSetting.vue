<template>
<form v-on:change="onchanged">
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
        "options",
        "settingName",
        "value"
    ],
    data() {
        return {
            selected: undefined
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
        console.log(`${this.settingName}:${this.value}`);
        this.selected = this.value;
    },

    watch: {
        value() {
            this.selected = this.value;
        }
    }
}
</script>