<template>
<div>
    <site-header></site-header>
    <div>
        <input type="file" id="cs-uploader" ref="csFile" @change="onChanged">
        <label for="cs-uploader">Upload core sample</label>
        <div v-if="error!==''">{{error}}</div>
        <ul v-if="warnings.length>0">
            <li v-for="warn in warnings">{{warn}}</li>
        </ul>
    </div>
</div>
</template>

<script>
    import SiteHeader from '../fragments/Header.vue';

    export default {
        name: 'Upload',
        components: { SiteHeader },
        data() {
            return {
                warnings: [],
                error: ''
            }
        },
        methods: {
            onChanged() {
                this.warnings = [];
                this.error = '';

                this.upload();
            },
            upload() {
                let file = this.$refs.csFile.files[0];

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
                    console.log(err.message);
                    this.error = err.message;
                });
            }
        }
    };
</script>