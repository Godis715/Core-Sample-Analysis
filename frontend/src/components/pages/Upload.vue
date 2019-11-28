<template>
<div>
    <site-header />
    <div id="upload-interface-container">
        <div class="first-col">
            <uploader
                v-on:change="attachedFileChanged($event)"
                v-on:delete-attached="deleteAttached"
                v-bind:disabled="state === State.fileIsUploading"
            />
            <div>
                <button
                    v-bind:disabled="state !== State.fileAttached || csName===''"
                    v-on:click="startUploading"
                    class="usual upload-btn"
                >Upload</button>
            </div>
        </div>

        <div class="second-col">
            <span v-bind:class="explanationClass+' explanation'">{{stateExplanation}}</span>
            <div class="delimiter"></div>

            <div 
                class="cs-name-input-block">
                <input
                    type="text"
                    required
                    id="cs-name-input"
                    ref="csNameInput"
                    v-model="csName"
                    v-bind:disabled="state !== State.fileAttached"
                />
                <label for="cs-name-input">Core sample name</label>
            </div>

            <div
                v-if="state === State.uploadedWarnings"
                class="warning-block">
                <div
                    v-for="(msg, index) in warningMessages"
                    v-bind:key="'warning-'+index">
                    <div>{{ `${index+1}. ${msg}` }}</div>
                    <div
                        v-if="index !== warningMessages.length - 1"
                        class="delimiter"
                    ></div>
                </div>
            </div>

            <div
                v-else-if="state === State.notUploadedErrors"
                class="error-block">
                <div
                    v-for="(msg, index) in errorMessages"
                    v-bind:key="'error-'+index">
                    <div>{{ `${index+1}. ${msg}` }}</div>
                    <div
                        v-if="index !== errorMessages.length - 1"
                        class="delimiter"
                    ></div>
                </div>
            </div>

            <div 
                v-else-if="state === State.notUploadedDuplicate"
                class="original-link-block">
                <div>Original could be found here: 
                    <router-link
                        v-bind:to="`view/${this.originalId}/`"
                    >Open original</router-link>.
                </div>
            </div>
        </div>
    </div>

</div>
</template>

<style>
    #upload-interface-container {
        display: flex;
        flex-direction: row;
        margin: 2em;
    }

    #upload-interface-container > .second-col {
        margin-left: 1em;
    }

    #upload-interface-container input[type="text"] {
        font-size: 1em;
        padding: 5px;
    }

    #upload-interface-container .delimiter {
        height: 1.3px;
        background-color: lightgray;
        width: 100%;
        margin-bottom: 1em;
    }

    #upload-interface-container .upload-btn {
        font-size: 1.3em;
        font-weight: 600;
        background-color: var(--base-green);
        color: white;
        width: 100%;
        margin-top: 1em;
    }

    #upload-interface-container .upload-btn:disabled {
        cursor: unset;
        background-color: lightgray;
        color: gray;
    }

    #upload-interface-container .explanation {
        font-size: 1.3em;
        font-weight: 600;
    }

    #upload-interface-container .explanation.warnings::before {
        content: "";
        background-size: 20px;
        height: 20px;
        width: 20px;
        display: inline-block;
        background-image: var(--warning-icon);
        margin-right: 10px;
    }
    #upload-interface-container .explanation.errors {
        color: rgb(119, 25, 25);
    }
    #upload-interface-container .explanation.errors::before {
        content: "";
        background-size: 20px;
        display: inline-block;
        height: 20px;
        width: 20px;
        background-image: var(--error-icon);
        margin-right: 10px;
    }

    #upload-interface-container .warning-block,
    #upload-interface-container .error-block {
        margin-top: 1em;
        max-height: 200px;
        overflow-y: auto;
        border: 1px solid lightgray;
        padding: 0.5em;
    }

    #upload-interface-container .warning-block {
        background-color: rgb(255, 255, 182);
    }

     #upload-interface-container .error-block {
        background-color: rgb(255, 173, 173);
    }

    #upload-interface-container .warning-block > *:not(:first-child),
    #upload-interface-container .error-block > *:not(:first-child),
    #upload-interface-container .original-link-block 
    {
        margin-top: 0.5em;
    }
    
</style>

<script>
    import SiteHeader from '../fragments/Header';
    import Message from '../fragments/Message';
    import Uploader from '../fragments/Uploader';

    const State = Object.freeze({
        noFile: 0,
        fileAttached: 1,
        fileIsUploading: 6,
        uploadedSucces: 2,
        uploadedWarnings: 3,
        notUploadedErrors: 4,
        notUploadedDuplicate: 5
    });

    export default {
        name: "Upload",
        components: {
            SiteHeader,
            Message,
            Uploader
        },
        data() {
            return {
                state: State.noFile,
                csName: "",
                file: undefined
            }
        },
        methods: {
            attachedFileChanged(file) {
                this.state = State.fileAttached;
                this.file = file;
                this.csName = this.file.name;
                this.$nextTick(() => this.$refs.csNameInput.focus());
                console.log("File attached");
            },
            deleteAttached() {
                this.csName = "";
                this.file = undefined;
                this.state = State.noFile;
                console.log("Attached file deleted");
            },
            startUploading() {
                this.state = State.fileIsUploading;
                
                let formData = new FormData();
                formData.append('archive', this.file);
                formData.append('csName', this.csName);
                let headers = { 
                        headers: { 'Content-Type': 'multipart/form-data' }
                    };

                this.$axios.post('api/core_sample/upload', formData, headers).then(resp => {
                    let result = resp.data;
                    console.log(result);
                    if (result.warnings.length > 0) {
                        this.warningMessages = result.warnings;
                        this.state = State.uploadedWarnings;
                    } else {
                        this.state = State.uploadedSucces;
                    }
                }).catch(err => {
                    console.log(err.response);
                    if (err.response.status == 409) {
                        this.originalId = err.response.data.csId;
                        this.state = State.notUploadedDuplicate;
                    } else {
                        this.state = State.notUploadedErrors;
                        this.errorMessages = [err.response.data.message];
                    }
                });
            }
        },
        computed: {
            State() {
                return State;
            },

            stateExplanation() {
                if (this.state === State.noFile)
                    return "Attach core sample. Required extension is .zip";
                else if (this.state === State.fileAttached)
                    return "Enter name of core sample";
                else if (this.state === State.uploadedSucces)
                    return "Core sample successfully uploaded";
                else if (this.state === State.uploadedWarnings)
                    return "Core sample uploaded with some warnings";
                else if (this.state === State.notUploadedErrors)
                    return "Core wasn't uploaded. Some errors occured";
                else if (this.state === State.notUploadedDuplicate) 
                    return "This core sample was already uploaded";
                else if (this.state === State.fileIsUploading)
                    return "File is uploading now...";
            },

            explanationClass() {
                if (this.state === State.uploadedSucces)
                    return "success";
                else if (this.state === State.uploadedWarnings)
                    return "warnings";
                else if (this.state === State.notUploadedErrors ||
                        this.state === State.notUploadedDuplicate)
                    return "errors";
                return "";
            }
        },

        beforeRouteLeave(to, from, next) {
            if (this.state === State.fileAttached) {
                let leave = confirm("You haven't upload the file. Leave anyway?");
                if (leave) {
                    next();
                } else {
                    next(false);
                }
            } else {
                next();
            }
        }
    };
</script>