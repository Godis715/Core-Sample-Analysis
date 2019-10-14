<template>
<div>
    <site-header></site-header>
    <div>
        <label for="cs-uploader">Upload core sample</label>
        <input required type="file" id="cs-uploader" ref="csFile" @change="onChanged">
        <div v-if="status==='warnings'">Continue</div>
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
                errors: [],
                status: 'no-file'
            }
        },
        methods: {
            onChanged() {
                let file = this.$refs.csFile.files[0];
                if (!file) return;

                console.log(this.status);
                if (this.status === 'warnings' || this.status === 'success') {
                    console.log('Deleteing previous core sample before uploading..');
                    this.$axios.delete(`api/core_sample/${this.csId}`).then(resp => {
                        console.log('Successfully deleted');
                        this.upload(file);
                    }).catch(err => {
                        console.log(err);
                    });
                } else {
                    this.upload(file);
                }

                this.warnings = [];
                this.errors = [];
                this.status = "no-file";
            },
            upload(file) {
                let formData = new FormData();
                formData.append('archive', file);
                formData.append('csName', 'core-sample');

                console.log('Uploading photo...');
                this.$axios.post('api/core_sample/upload', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then(resp => {
                    console.log('status ' + resp.status);
                    console.log(resp.data);

                    this.warnings = resp.data.warnings;
                    this.csId = resp.data.csId;
                    console.log(this.csId);

                    if (this.warnings.length > 0) this.status = "warnings";
                    else this.status = "success";
                    
                }).catch(err => {
                    console.log('status ' + err.response.status);
                    console.log(err.response.data.message);

                    this.errors = [err.response.data.message];
                    this.status = "errors";
                });
            }
        }
    };
</script>