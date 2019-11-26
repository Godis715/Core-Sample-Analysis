<template>
<div>
    <div
        class="uploader-container"
        v-on:click.prevent="clickUpload">
        <div class="delete-btn-panel">
            <button
                v-show="state === State.fileAttached"
                class="round delete dark-alpha"
                v-on:click.stop="deleteAttached"
            ></button>
        </div>
        <input
            type="file"
            id="uploader-element"
            ref="uploader"
            v-on:change="attachedFileChanged"
            v-bind:disabled="disabled"
            v-on:click.stop
        />
            
        <label
            v-bind:class="labelClass"
            for="uploader-element"
        ></label>
        <span
            align="center"
            id="file-name"
            v-if="state === State.fileAttached"
        >{{file.name}}</span>
        <span
            v-else
            align="center"
        >Click here</span>
    </div>
</div>
</template>

<style>
    :root {
        --upload-cont-indent: 2em;
        --upload-cont-offset: 12px;
    }
    .uploader-container {
        height: 10em;
        width: calc(10em + var(--upload-cont-indent));
        font-size: 1.3em;
        font-weight: 600;
        display: flex;
        flex-direction: column;
        background-color: whitesmoke;
        outline: 2px dashed #5d5d5d;
        outline-offset: calc(0px - var(--upload-cont-offset));
        cursor: pointer;
        padding-bottom: var(--upload-cont-indent);
    }

    .uploader-container label {
        background-size: 4em;
        height: 4em;
        width: 4em;
        opacity: 0.5;
        cursor: pointer;
        margin: auto;
    }

    .uploader-container label.attached { background: var(--attached-file-icon); }

    .uploader-container label.upload { background: var(--upload-file-icon); }

    .uploader-container:hover label { opacity: 1; }
    
    .uploader-container input[type=file] {
        width: 0.1px;
        height: 0.1px;
        opacity: 0;
        position: absolute;
        z-index: -10;
    }

    .uploader-container > .delete-btn-panel {
        height: calc(var(--upload-cont-indent) - var(--upload-cont-offset));
        margin-top: var(--upload-cont-offset);
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        padding-right: var(--upload-cont-offset);
    }

    .uploader-container span {
        word-wrap: break-word;
        margin: 0 calc(20px + var(--upload-cont-offset));
    }
</style>

<script>
    const State = Object.freeze({
        clear: 0,
        fileAttached: 1,
        uploaded: 2,
        notUploaded: 3
    });

    export default {
        name: 'Uploader',
        props: {
            disabled: {
                type: Boolean,
                required: false
            }
        },
        data() {
            return {
                state: State.clear,
                file: undefined,
            };
        },
        methods: {
            attachedFileChanged() {
                let tmpFile = this.$refs.uploader.files[0];
                if (!tmpFile) return;

                this.file = tmpFile;
                this.state = State.fileAttached;

                this.$emit("change", this.file);
            },
            clickUpload() {
                this.$refs.uploader.click();
            },
            deleteAttached() {
                this.state = State.clear;
                this.file = undefined;
                this.$refs.uploader.value = '';
                
                this.$emit("delete-attached");
            }
        },
        computed: {
            labelClass() {
                if (this.state === State.clear)
                    return "upload";
                else if (this.state === State.fileAttached)
                    return "attached";
            },
            State() {
                return State;
            },
            console() {
                return console;
            }
        },
    };
</script>