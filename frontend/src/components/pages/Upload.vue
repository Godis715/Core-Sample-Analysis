<template>
<div>
    <site-header />
    <div id="main-cont">
        <div id="upload-cont">
            <input type="file" id="uploader" ref="uploadedFile" @change="onChanged">
            <label for="uploader">Upload</label>

            <span id="file-name" v-if="!noFileAttached">{{fileName}}</span>
        </div>
        <!-- div id="status">{{statusText}}</div -->
        <div v-if="!noFileAttached" id="message-block">
            <Message v-for="(msg, index) in messages" :msgData="msg" :key="index" />
        </div>
        <div v-if="!noFileAttached" id="btns-block">
            <div>
                <button @click="startAnalysis" v-if="!isAnalysed" :disabled="!allowedAnalysis">Start analysis</button>
                <button v-else :disabled="true">Analysing..</button>
            </div>
            <div>
                <button @click="resetView">Reset</button>
            </div>
        </div>
    </div>
</div>
</template>

<style>
    #main-cont {
        margin: 1em;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    #main-cont > *:not(:last-child) {
        margin-bottom: 1em;
    }
    #btns-block {
        display: flex;
        flex-direction: row;
    }

    #upload-cont {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 200px;
        height: 100px;
        background-color: whitesmoke;
        outline: 2px dashed #5d5d5d;
        outline-offset: -12px;
    }
    
    #upload-cont input[type=file] {
        width: 0.1px;
        height: 0.1px;
        opacity: 0;
        position: absolute;
        z-index: -10;
    } 

    #message-block {
        max-height: 100px;
        overflow-y: auto;
    }

    #upload-cont label {
        display: block;
        cursor: pointer;
    }  

    #upload-cont label:hover {
        text-decoration: underline;
    }

    #file-name {
        font-size: 0.8em;
        color: darkgray;
    }

    .msg {
        font-size: 0.8em;
        width: fit-content;
    }

    .error-msg {
        color:rgb(131, 34, 34);
    }

    .warn-msg {
        color:rgb(116, 97, 34);
    }

    .notif-msg {
        color: rgb(30, 34, 94);
    }

    div > .block-item {
        padding-top: 1em;
    }
    div > .block-item::before {
        content: "- ";
    }
    .enabled-btn {
        background-color: rgb(86, 175, 86);
    }
    .disabled-btn {
        background-color: gray;
    }

    #btns-block button {
        background-color: whitesmoke;
        border: none;
        padding: 0.3em 0.5em;
        font-size: 0.8em;
    }

    #btns-block button:first-child {
        margin-right: 1em;
    }

    button:not([disabled="disabled"]) {
        cursor: pointer;
    }
</style>

<script>
    import SiteHeader from '../fragments/Header.vue';
    import Message from '../fragments/Message.vue';

    async function uploadFile(axiosInst, file) {
        let formData = new FormData();
        formData.append('archive', file);
        formData.append('csName', 'core-sample');
        let headers =  { headers: { 'Content-Type': 'multipart/form-data' } };

        console.log('Uploading photo...');

        return await axiosInst.post('api/core_sample/upload', formData, headers);
    }
    async function deleteFile (axiosInst, csId) {
        return axiosInst.delete(`api/core_sample/delete/${csId}`)
        .catch(err => {
            console.log(err);
        });
    }
    async function analyseCoreSample(axiosInst, csId) {
        return axiosInst.put(`api/core_sample/analyse/${csId}`);
    }

    export default {
        name: 'Upload',
        components: { SiteHeader, Message },
        data() {
            return {
                warnings: [],
                errors: [],
                status: 'noFile',
                csId: '',
                isAnalysed: false,
                messages: [],
                // statusText: 'No file attached',
                fileName: ''
            }
        },
        methods: {
            // uploaded file has changed
            onChanged() {
                let file = this.$refs.uploadedFile.files[0];
                // if file is attached
                if (file) {
                    this.fileName = file.name;
                    let uploading = this.upload(file);
                    this.$root.$emit('start-loading', uploading);
                } else {
                    this.fileName = '';
                    this.messages = [];
                    this.status = "noFile";
                    // this.statusText = 'No file attached';
                    this.csId = '';
                }
            },

            upload(file) {
                return uploadFile(this.$axios, file).then(resp => {
                    console.log('status ' + resp.status);
                    console.log(resp.data);

                    this.csId = resp.data.csId;
                    console.log(this.csId);
    
                    if (resp.data.warnings.length > 0) {
                        this.status = "warnings";
                        // this.statusText = "Uploaded with warnings:";

                        let newMessages = [];
                        for(let i = 0; i < resp.data.warnings.length; ++i) {
                            newMessages.push({
                                type: 'warning',
                                text: resp.data.warnings[i]
                            });
                        }
                        this.messages = newMessages;
                    }
                    else this.status = "success";
                }).catch(err => {
                    console.log('status ' + err.response.status);
                    console.log(err.response.data.message);

                    // if file has been uploaded before
                    if (err.response.status == 409) {
                        this.status = "alreadyUploaded";
                        this.csId = err.response.data.csId;
                        // this.statusText = 'Core sample wasn\' uploaded';
                        this.messages = [{
                            text: 'This core sample has been already uploaded',
                            type: 'notification',
                            link: {
                                where: `core_sample/${this.csId}`,
                                text: 'View this sample'
                            }
                        }];
                    } else {
                        this.status = "errors";
                        // this.statusText = 'Some errors occured:';
                        this.messages = [{
                            text: err.response.data.message,
                            type: 'error'
                        }];
                    }
                });
            },

            resetView() {
                this.messages = [];
                this.status = "noFile";
                this.statusText = 'No file attached';
                this.csId = '';
                this.isAnalysed = false;
                this.fileName = '';

                this.$refs.uploadedFile.value = '';

                // deleting if uploaded
                if (this.csId !== '' && this.status !=='alreadyUploaded') {
                    deleteFile(this.$axios, this.csId).catch(err => {
                        console.error(err);
                    });
                }
            },

            startAnalysis() {
                if (!this.csId || this.status === 'alreadyUploaded') return;
                analyseCoreSample(this.$axios, this.csId).then(resp => {
                    console.log(resp);
                    this.isAnalysed = true;
                }).catch(err => {
                    console.error(err);
                    console.log(err.response);
                });
            }
        },

        computed: {
            noFile() {
                return this.status === 'noFile';
            },
            hasErrors() {
                return this.status === 'errors';
            },
            hasWarnings() {
                return this.status === 'warnings';
            },
            alreadyUploaded() {
                return this.status === 'alreadyUploaded';
            },
            allowedAnalysis() {
                return this.status === 'warnings' || this.status === 'success';
            },
            noFileAttached() {
                return this.status === 'noFile';
            }
        }
    };
</script>