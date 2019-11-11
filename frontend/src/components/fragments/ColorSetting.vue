<template>
<form v-if="isMounted" v-on:change="onchanged">
    <h4>{{title}}</h4>
    <div class="color-setting-cont">
    <div
        v-for="(color, index) in allColors"
        v-bind:key="index">
        <input
            v-bind:id="`${id}-color-${index}`"
            v-model="selectedColor"
            v-bind:value="color"
            type="radio"
            name="color-radio"
            class="color"
        />
        <label v-bind:style="`background-color:${color}`" v-bind:for="`${id}-color-${index}`"></label>
    </div>
    </div>
</form>
</template>

<style>
    input[type="radio"].color {
        width: 0;
        opacity: 0;
        position: absolute;
    }

    input[type="radio"].color ~ label {
        height: 20px;
        width: 20px;
        display: block;
    }

    input[type="radio"].color:checked ~ label {
        outline: 2px solid rgb(47, 66, 85);
        outline-offset: -2px;
    }

    .color-setting-cont {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
</style>

<script>
export default {
    name: "ColorSetting",
    props: [
        "title",
        "options",
        "settingName",
        "value",
        "id"
    ],
    data() {
        return {
            selectedColor: undefined,
            allColors: [
                "black",
                "gray",
                "white",
                "cyan",
                "magenta",
                "yellow",
                "red",
                "green",
                "blue"
            ],
            isMounted: false
        }
    },
    methods: {
        onchanged() {
            this.$emit("selected-changed", {
                data: this.selectedColor,
                settingName: this.settingName
            });
        }
    },

    created() {
        this.selectedColor = this.value;
    },

    mounted() {
        this.isMounted = true;
    },

    watch: {
        value() {
            this.selectedColor = this.value;
        }
    }
}
</script>