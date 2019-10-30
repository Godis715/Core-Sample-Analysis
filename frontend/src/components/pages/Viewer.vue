<template>
<div>
    <site-header />
    <div id="main">

        <div v-for="(ch, index) in channels" v-bind:key="index">
            <view-channel-img
                v-if="!!markup && ch.type==='DL'"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
                v-bind:data="markup.dlImages"
                v-bind:settings="ch.settings"
            />
            <view-channel-img
                v-else-if="!!markup && ch.type==='UV'"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthUV"
                v-bind:data="markup.uvImages"
                v-bind:settings="ch.settings"
            />
            <view-channel-line-markup
                v-else-if="!!markup && ch.type==='oil'"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
                v-bind:data="markup.markup.oil"
                v-bind:settings="ch.settings"
            />
            <view-channel-line-markup
                v-else-if="!!markup && ch.type==='carbon'"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
                v-bind:data="markup.markup.carbon"
                v-bind:settings="ch.settings"
            />
            <view-channel-line-markup
                v-else-if="!!markup && ch.type==='ruin'"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
                v-bind:data="markup.markup.ruin"
                v-bind:settings="ch.settings"
            />
            <view-channel-line-markup
                v-else-if="!!markup && ch.type==='rock'"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
                v-bind:data="markup.markup.rock"
                v-bind:settings="ch.settings"
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
                },
                
                {
                    type: "oil",
                    settings: {
                        backgroundColor: "white",
                        color: "red"
                    }
                },

                {
                    type: "carbon",
                    settings: {
                        backgroundColor: "cyan",
                        color: "white"
                    }
                },

                {
                    type: "rock",
                    settings: {
                        backgroundColor: "black",
                        color: "green"
                    }
                },

                {
                    type: "ruin",
                    settings: {
                        backgroundColor: "black",
                        color: "white"
                    }
                },

                {
                    type: "DL",
                    settings: {
                        fragmentsWidthFit: "alignLeft"
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