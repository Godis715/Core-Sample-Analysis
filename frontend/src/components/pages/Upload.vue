<template>
<div>
    <site-header />
    <div>
        <div>
            <uploader
                v-on:change="attachedFileChanged($event)"
                v-on:delete-attached="deleteAttached"
            />
        </div>
        <div>
            <button
                class="usual upload-btn"
            >Upload</button>
        </div>
    </div>

</div>
</template>

<style>

</style>

<script>
    import SiteHeader from '../fragments/Header';
    import Message from '../fragments/Message';
    import Uploader from '../fragments/Uploader';

    export default {
        name: "Upload",
        components: {
            SiteHeader,
            Message,
            Uploader
        },
        methods: {
            attachedFileChanged(file) {
                console.log("File attached");
            },
            deleteAttached() {
                console.log("Attached file deleted");
            }
        }
    };
</script>