<template>
<div>
    <site-header />
    <div id="main">
        <view-channel-img
            v-if="!!markup"
            v-bind:res="resolution"
            v-bind:absHeight="absHeight"
            v-bind:absWidth="absWidthDL"
            v-bind:data="markup.dlImages"
        ></view-channel-img>

        <view-channel-img
            v-if="!!markup"
            v-bind:res="resolution"
            v-bind:absHeight="absHeight"
            v-bind:absWidth="absWidthUV"
            v-bind:data="markup.uvImages"
        ></view-channel-img>
    </div>
</div>
</template>

<style>
    #main {
        display: flex;
        flex-direction: row;
    }
</style>

<script>
import SiteHeader from "../fragments/Header"
import ViewChannelImg from "../fragments/ViewChannelImg"

export default {
    name: "Viewer",
    components: { SiteHeader, ViewChannelImg },
    data() {
        return {
            markup: undefined,
            resolution: 20
        }
    },
    created() {
        let csId = this.$route.params.csId;
        this.$axios.get(`api/core_sample/${csId}/markup`).then(resp => {
            console.log("Markup is got");
            this.markup = resp.data;
        }).catch(err => {
            console.error(err);
        });
    },
    computed: {
        // it is the same for all channels
        // it can be found from, for example, dlImages
        absHeight() {
            return this.markup.dlImages.reduce((acc, img) => acc + (img.bottom - img.top), 0);
        },
        absWidthDL() {
            let width = 0;
            let imgs = this.markup.dlImages;
            for (let i = 0; i < imgs.length; ++i) {
                let currWidth = (imgs[i].width / imgs[i].height) * (imgs[i].bottom - imgs[i].top);
                if (currWidth > width)
                    width = currWidth;
            }
            console.log("Abswidth is "+width);
            return width;
        },
        absWidthUV() {
            let width = 0;
            let imgs = this.markup.uvImages;
            for (let i = 0; i < imgs.length; ++i) {
                let currWidth = (imgs[i].width / imgs[i].height) * (imgs[i].bottom - imgs[i].top);
                if (currWidth > width)
                    width = currWidth;
            }
            return width;
        },
    }
}
</script>

<style>

</style>