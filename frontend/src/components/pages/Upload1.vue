<template>
<div>
    <site-header />
    <div id="main-cont-upload">
        <h1>Upload core sample for analysis</h1>
        <!-- Element, which provide file uploading -->
        

        <div id="upload-form">
            <div
                id="upload-cont"
                v-on:click="triggerUpload">

                <input
                    type="file"
                    id="uploader"
                    ref="uploadedFile"
                    v-on:change="attachedFileChanged" />
                    
                <label
                    v-bind:class="labelClass"
                    for="uploader"
                ></label>

                <span
                    id="file-name"
                    v-if="!noFileAttached"
                >{{console.log(file)}}</span>
            </div>

            <div>
                <span class="state">{{stateText}}</span>
                <div class="delimeter"></div>
                <div v-if="allowedAnalysis">
                    <input type="text" />
                    <label for="filename">Core sample name</label>
                </div>

                <div
                    v-if="!noFileAttached"
                    id="message-block">
                    <Message
                        v-for="(msg, index) in messages"
                        v-bind:msgData="msg"
                        v-bind:key="'msg-' + index" />
                </div>
            </div>
        </div>

        <div
            v-if="!noFileAttached"
            id="btns-block"
        >
            <div>
                <button 
                    v-if="!alreadyUploaded"
                    v-on:click="resetView"
                >Reset</button>
            </div>
        </div>
        <!-- For showing diffrenet about file uploading messages -->
        

        <!-- Buttons -->
        
    </div>
</div>
</template>

<style>
    #main-cont-upload {
        max-width: 750px;
        margin: 0 auto;
        flex-direction: column;
    }

    #main-cont > *:not(:last-child) {
        margin-bottom: 1em;
    }
    
    #btns-block {
        display: flex;
        flex-direction: row;
    }

    #upload-cont {
        font-size: 1.3em;
        font-weight: 600;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 10em;
        height: 10em;
        background-color: whitesmoke;
        outline: 2px dashed #5d5d5d;
        outline-offset: -12px;
        cursor: pointer;
        padding: 0 12px;
        margin-right: 1em;
    }

    #upload-cont > button.delete {
        align-self: flex-end;
    }

    #upload-cont label {
        background-size: 4em;
        height: 4em;
        width: 4em;
        opacity: 0.5;
    }

    #upload-cont label.attached {
        background: var(--attached-file-icon);
    }

    #upload-cont label.upload {
        background: var(--upload-file-icon);
    }

    #upload-cont:hover label {
        opacity: 1;
    }
    
    #upload-cont input[type=file] {
        width: 0.1px;
        height: 0.1px;
        opacity: 0;
        position: absolute;
        z-index: -10;
    } 

    #upload-form {
        display: flex;
        flex-direction: row;
    }
    
    #upload-form .state {
        font-size: 1.3em;
    }

    #upload-form .delimeter {
        width: 100%;
        height: 1.3px;
        background-color: lightgray;
        margin-bottom: 1em;
    }

    #message-block {
        margin-top: 1em;
        max-height: 100px;
        overflow-y: scroll;
        border: 1.3px solid lightgray;
    }

    #upload-cont label {
        display: block;
        cursor: pointer;
    }  

    #file-name {
        font-size: 0.8em;
        font-weight: 400;
        color: darkgray;
    }

    .msg {
        font-size: 1em;
        width: fit-content;
    }

    .error-msg { color:rgb(131, 34, 34); }

    .warn-msg { color:rgb(116, 97, 34); }

    .notif-msg { color: rgb(30, 34, 94); }

    .success-msg { color: rgb(16, 161, 23); }

    div > .block-item { padding-top: 1em; }
    
    div > .block-item::before { content: "- "; }
    
    .enabled-btn { background-color: rgb(86, 175, 86); }

    .disabled-btn { background-color: gray; }

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
        formData.append('csName', file.name);
        let headers =  { headers: { 'Content-Type': 'multipart/form-data' } };

        console.log('Uploading photo...');

        return await axiosInst.post('api/core_sample/upload', formData, headers);
    }
    async function deleteFile (axiosInst, csId) {
        return axiosInst.delete(`api/core_sample/${csId}/delete`)
        .catch(err => {
            console.log(err);
        });
    }
    async function analyseCoreSample(axiosInst, csId) {
        return axiosInst.put(`api/core_sample/${csId}/analyse`);
    }

    export default {
        name: '',
        components: { SiteHeader, Message },
        data() {
            return {
                uploadResult: undefined,
                warnings: [],
                errors: [],
                status: 'noFile',
                csId: '',
                messages: []
            }
        },
        methods: {
            attachedFileChanged() {
                let file = this.$refs.uploadedFile.files[0];

                // if file is attached
                if (file) {
                    this.file = file;
                    let uploading = this.upload(file);
                    this.$root.$emit('start-loading', uploading);
                    return;
                }
            },

            // redirecting click from upload container to input-file
            triggerUpload() {
                this.$refs.uploadedFile.click();
            },

            upload(file) {
                this.uploadResult = {};
                return uploadFile(this.$axios, file).then(resp => {
                    console.log('status ' + resp.status);
                    console.log(resp.data);

                    this.uploadResult.csId = resp.data.csId;
                    console.log(this.csId);
    
                    if (resp.data.warnings.length > 0) {
                        this.uploadResult.status = "warnings";

                        let newMessages = [];
                        for(let i = 0; i < resp.data.warnings.length; ++i) {
                            newMessages.push({
                                type: 'warning',
                                text: resp.data.warnings[i]
                            });
                        }
                        this.uploadResult.messages = newMessages;
                    }
                    else {
                        this.uploadResult.status = "success";
                        this,uploadResult.messages = [{
                            type: 'success',
                            text: 'Successfully uploaded!'
                        }];
                    };
                }).catch(err => {
                    console.log('status ' + err.response.status);
                    console.log(err.response.data.message);

                    // if file has been uploaded before
                    if (err.response.status == 409) {
                        this.uploadResult = {
                            status: "alreadyUploaded",
                            csId: err.response.data.csId,
                            messages: [{
                                text: 'This core sample has been already uploaded',
                                type: 'notification',
                                link: {
                                    where: `view/${this.csId}`,
                                    text: 'View this sample'
                                }
                            }]
                        }
                    } else {
                        this.uploadResult = {
                            status: "errors",
                            messages: [{
                                text: err.response.data.message,
                                type: 'error'
                            }]
                        };
    
                    }
                });
            },

            /*
                clearing view to default
                deleting file, if it has been uploaded
            */
            resetView() {
                if (!this.uploadResult) return;

                this.result = undefined;
                this.$refs.uploadedFile.value = '';

                // deleting if uploaded
                if (this.uploadResult.csId && this.uploadResult.status !=='alreadyUploaded') {
                    console.log('Deleting');
                    deleteFile(this.$axios, _csId).catch(err => {
                        console.error(err);
                    });
                }
            },
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
            },

            labelClass() {
                return this.noFile ? "upload" : "attached";
            },

            stateText() {
                return this.noFile ? "No file attached" :
                    this.allowedAnalysis ? "File uploaded" :
                    "Some errors occured";
            }
        }
    };
</script>