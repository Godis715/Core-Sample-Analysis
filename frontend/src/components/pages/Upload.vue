<template>
<div>
    <site-header />
    <div id="main-cont-upload">
        <div>
            <h1>Upload core sample for analysis</h1>
        </div>
        <!-- Element, which provide file uploading -->
        <div
            id="upload-cont"
            v-on:click="triggerUpload">

            <input
                type="file"
                id="uploader"
                ref="uploadedFile"
                v-on:change="attachedFileChanged" />
                
            <label for="uploader">Upload</label>

            <span
                id="file-name"
                v-if="!noFileAttached"
            >{{file.name}}</span>
        </div>

        <!-- For showing diffrenet about file uploading messages -->
        <div
            v-if="!noFileAttached"
            id="message-block">
            <Message
                v-for="(msg, index) in messages"
                v-bind:msgData="msg"
                v-bind:key="'msg-' + index" />
        </div>

        <!-- Buttons -->
        <div
            v-if="!noFileAttached"
            id="btns-block">
            <div>
                <button
                    v-on:click="startAnalysis"
                    v-if="!isAnalysed"
                    v-on:disabled="!allowedAnalysis"
                >Start analysis</button>

                <button
                    v-else
                    v-on:disabled="true"
                >Analysing..</button>
            </div>

            <div>
                <button v-on:click="resetView">Reset</button>
            </div>
        </div>

        <div id="info-panel">
            <h2>Files must match these rules:</h2>
            <ul>
                <li>
                    File must be a .zip archive
                </li>
                <li>
                    Structure description of the sample must be situated in a root of the archive in "description.json".<br/>
                    To get detailed information about description structure and explore examples visit <a href="#">FAQ</a>
                </li>
                <li>
                    Archive should contain only that files, that are refernced in description.json.
                </li>
                <li>
                    Sizes of day-light and uv images of same fragments should match.
                </li>
            </ul>
            <h2>Also</h2>
            <ul>
                <li>
                    If the core sample has been already uploaded, service will provide a link to it.
                </li>
            </ul>
        </div>
    </div>
</div>
</template>

<style>
    #main-cont-upload {
        max-width: 500px;
        display: flex;
        margin: auto;
        flex-direction: column;
        text-align: justify;
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
        align-self: center;
        width: 200px;
        height: 100px;
        background-color: whitesmoke;
        outline: 2px dashed #5d5d5d;
        outline-offset: -12px;
        cursor: pointer;
    }

    #upload-cont:hover label {
        text-decoration: underline;
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

    #file-name {
        font-size: 0.8em;
        color: darkgray;
    }

    #info-panel {
        max-width: 500px;
        text-align: justify;
    }

    #info-panel li {
        margin-bottom: 1em;
    }

    .msg {
        font-size: 0.8em;
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
        formData.append('csName', 'core-sample');
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
        name: 'Upload',
        components: { SiteHeader, Message },
        data() {
            return {
                warnings: [],
                errors: [],
                status: 'noFile',
                csId: '',
                isAnalysed: false,
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
                return uploadFile(this.$axios, file).then(resp => {
                    console.log('status ' + resp.status);
                    console.log(resp.data);

                    this.csId = resp.data.csId;
                    console.log(this.csId);
    
                    if (resp.data.warnings.length > 0) {
                        this.status = "warnings";

                        let newMessages = [];
                        for(let i = 0; i < resp.data.warnings.length; ++i) {
                            newMessages.push({
                                type: 'warning',
                                text: resp.data.warnings[i]
                            });
                        }
                        this.messages = newMessages;
                    }
                    else {
                        this.status = "success";
                        this.messages = [{
                            type: 'success',
                            text: 'Successfully uploaded!'
                        }];
                    };
                }).catch(err => {
                    console.log('status ' + err.response.status);
                    console.log(err.response.data.message);

                    // if file has been uploaded before
                    if (err.response.status == 409) {
                        this.status = "alreadyUploaded";
                        this.csId = err.response.data.csId;
                        this.messages = [{
                            text: 'This core sample has been already uploaded',
                            type: 'notification',
                            link: {
                                where: `view/${this.csId}`,
                                text: 'View this sample'
                            }
                        }];
                    } else {
                        this.status = "errors";
                        this.messages = [{
                            text: err.response.data.message,
                            type: 'error'
                        }];
                    }
                });
            },

            /*
                clearing view to default
                deleting file, if it has been uploaded
            */
            resetView() {
                let _status = this.status;
                let _csId = this.csId;

                this.messages = [];
                this.status = "noFile";
                this.statusText = 'No file attached';
                this.csId = '';
                this.isAnalysed = false;
                this.fileName = '';

                this.$refs.uploadedFile.value = '';

                // deleting if uploaded
                if (_csId !== '' && _status !=='alreadyUploaded') {
                    console.log('Deleting');
                    deleteFile(this.$axios, _csId).catch(err => {
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