<template>
<div>
    <site-header />
    <div id="main">
        <div class="channel-wrapper">
            <view-channel-img
                v-if="!!markup"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
                v-bind:data="markup.dlImages"
                v-bind:settings="channels[0].settings"
                name="DL"
            />
        </div>

        <div class="channel-wrapper">
            <view-channel-img
                v-if="!!markup"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthUV"
                v-bind:data="markup.uvImages"
                v-bind:settings="channels[1].settings"
                name="UV"
            />
        </div>

        <div class="channel-wrapper">
            <view-channel-line-markup
                v-if="!!markup"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
                v-bind:data="markup.markup.oil"
                name="oil"
            />
        </div>

        <div class="channel-wrapper">
            <view-channel-line-markup
                v-if="!!markup"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
                v-bind:data="markup.markup.carbon"
                name="carbon"
            />
        </div>
    </div>
</div>
</template>

<style>
    #main {
        margin-left: 25px;
        margin-bottom: 500px;
        display: flex;
        flex-direction: row;
    }

    .channel-wrapper {
        margin: 3px;
        border: 2px solid gray;
    }
</style>

<script>
import SiteHeader from "../fragments/Header"
import ViewChannelImg from "../fragments/ViewChannelImg"
import ViewChannelLineMarkup from "../fragments/ViewChannelLineMarkup"

export default {
    name: "Viewer",
    components: {
        SiteHeader,
        ViewChannelImg,
        ViewChannelLineMarkup
    },
    data() {
        return {
            markup: undefined,
            resolution: 10,
            channels: [
                {
                    type: "DL",
                    settings: {
                        fragmentsWidthFit: "stretch"
                    }
                },

                {
                    type: "UV",
                    settings: {
                        fragmentsWidthFit: "stretch"
                    }
                }
            ]
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