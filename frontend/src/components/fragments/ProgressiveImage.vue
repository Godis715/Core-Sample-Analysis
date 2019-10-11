<template>
<div v-if="state=='loadingLow'" :style="styleConf" class="preview-col"></div>
<img v-else :src="imgSrc" :style="styleConf"></img>
</template>

<style>
    .preview-col {
        background-color: gray;
    }
</style>

<script>
export default {
    name: 'progressive-img',
    props: ['height', 'width', 'srcLow', 'srcHigh'],
    data() {
        return {
            state: 'loadingLow',
            imgSrc: '',
            styleConf: { height: this.height + 'px', width: this.width + 'px' }
        }
    },

    created() {
        const imgLow = new Image();
        imgLow.src = this.srcLow;

        imgLow.onload = () => {
            this.imgSrc = this.srcLow;
            const imgHigh = new Image();
            imgHigh.src = this.srcHigh;
            this.state = 'loadingHigh';

            imgHigh.onload = () => {
                this.imgSrc = this.srcHigh;
                this.state = 'done';
            };
        };
    }
};
</script>