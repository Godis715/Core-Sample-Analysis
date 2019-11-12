<template>
<form v-if="isMounted" v-on:change="onchanged">
    <h4>{{title}}</h4>
    <div>
        <input
            type="number"
            v-bind:max="max"
            v-bind:min="min"
            v-model="number"
            v-bind:id="`${id}-number`"
        />
        <label v-bind:for="`${id}-number`">px</label>
    </div>
</form>
</template>

<script>

export default {
    name: "NumberSetting",
    props: {
        title: {
            type: String,
            required: true
        },
        settingName: {
            type: String,
            required: true
        },
        value: {
            type: Number,
            required: true
        },
        max: {
            type: Number,
            required: true
        },
        min: {
            type: Number,
            required: true
        },
        id: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            number: undefined,
            isMounted: false
        }
    },
    methods: {
        onchanged() {
            this.$emit("selected-changed", {
                data: parseInt(this.number),
                settingName: this.settingName
            });
        }
    },

    created() { this.number = this.value; },
    mounted() { this.isMounted = true; },
    watch: {
        value() {
            this.number = this.value;
        }
    }
}
</script>