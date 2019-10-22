<template>
<div>
    <site-header />
    <div>
        <label v-if="status=='noFile'" for="cs-uploader">Upload core sample</label>
        <label v-else for="cs-uploader">Restore core sample</label>
        <input required type="file" id="cs-uploader" ref="csFile" @change="onChanged">

        <div id="err-block" class="message-block" v-if="errors.length>0">
            <div>Core sample wasn't uploaded. Errors occured:</div>
            <div class="block-item" v-for="err in errors">{{err}}</div>
        </div>

        <div class="message-block" v-if="status==='alreadyUploaded'">
            <div class="block-item">
                <div>This core sample has been uploaded before.</div>
                <router-link :to="'/core_sample/'+csId">Link</router-link>
            </div>
        </div>

        <div id="warn-block" class="message-block" v-if="warnings.length>0">
            <div>Core sample was uploaded with warnings: </div>
            <div class="block-item" v-for="warn in warnings">{{warn}}</div>
        </div>

        <!-- start analysis when uploaded without errors -->
        <div v-if="status==='warnings'||status==='success'">
            <router-link :to="{name:'Account'}">Start analysis</router-link>
        </div>
    </div>
</div>
</template>

<style>
    .message-block {
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

    async function uploadFile(axiosInst, file) {
        let formData = new FormData();
        formData.append('archive', file);
        formData.append('csName', 'core-sample');
        let headers =  { headers: { 'Content-Type': 'multipart/form-data' } };

        console.log('Uploading photo...');

        return await axiosInst.post('api/core_sample/upload', formData, headers);
    }
    async function deleteFile (axiosInst, csId) {
        return axiosInst.delete(`api/core_sample/${csId}`);
    }

    export default {
        name: 'Upload',
        components: { SiteHeader },
        data() {
            return {
                warnings: [],
                errors: [],
                status: 'noFile',
                csId: ''
            }
        },
        methods: {
            // uploaded file has changed
            onChanged() {
                let file = this.$refs.csFile.files[0];

                // if file is attached
                if (file) {

                    // deleting if uploaded
                    if (this.csId !== '') {
                        deleteFile(this.$axios, this.csId).catch(err => {
                            console.error(err);
                        });
                    }

                    let uploading = this.upload(file);
                    this.$root.$emit('start-loading', uploading);
                }

                this.warnings = [];
                this.errors = [];
                this.status = "noFile";
                this.csId = '';
            },

            upload(file) {
                return uploadFile(this.$axios, file).then(resp => {
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

                    // if file has been uploaded before
                    if (err.response.status == 409) {
                        this.status = "alreadyUploaded";
                        this.csId = err.response.data.csId;
                    } else {
                        this.errors = [err.response.data.message];
                        this.status = "errors";
                    }
                });
            }
        }
    };
</script>