<template>
<div>
    <site-header></site-header>
    <div>
        <label for="cs-uploader">Upload core sample</label>
        <input required type="file" id="cs-uploader" ref="csFile" @change="onChanged">
        <div id="err-block" v-if="errors.length>0">
            <div>Errors: </div>
            <div class="block-item" v-for="err in errors">{{err}}</div>
        </div>
        <div id="warn-block" v-if="warnings.length>0">
            <div>Warnings: </div>
            <div class="block-item" v-for="warn in warnings">{{warn}}</div>
        </div>
    </div>
</div>
</template>

<style>
    #err-block, #warn-block {
        font-size: 0.8em;
        padding: 5px;
        width: fit-content;
    }

    #err-block {
        background-color: pink;
        color:rgb(131, 34, 34);
    }

    #warn-block {
        background-color:khaki;
        color:rgb(116, 97, 34);
    }
    div > .block-item {
        padding-top: 1em;
    }
    div > .block-item::before {
        content: "- ";
    }
</style>

<script>
    import SiteHeader from '../fragments/Header.vue';

    export default {
        name: 'Upload',
        components: { SiteHeader },
        data() {
            return {
                warnings: [],
                errors: []
            }
        },
        methods: {
            onChanged() {
                this.warnings = [];
                this.errors = [];

                let file = this.$refs.csFile.files[0];
                if (!file) return;

                this.upload(file);
            },
            upload(file) {
                let formData = new FormData();
                formData.append('archive', file);
                formData.append('csName', 'core-sample');

                this.$axios.post('api/core_sample/upload', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then(resp => {
                    console.log(resp.status);
                    console.log(resp.data);

                    this.warnings = resp.data.warnings;
                    
                }).catch(err => {
                    console.error(err.response.status);
                    console.error(err.response.data.message);

                    this.errors = [err.response.data.message];
                });
            }
        }
    };
</script>