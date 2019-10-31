<template>
<div>
    <site-header />
    <div id="main">
        <div
            v-for="(ch, index) in channels"
            v-bind:key="index"
        >
            <view-channel-multiple
                v-if="!!ch"
                v-bind:layers="ch.layers"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
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
import ViewChannelMultiple from "../fragments/ViewChannelMultiple"


export default {
    name: "Viewer",
    components: {
        SiteHeader,
        ViewChannelMultiple
    },
    data() {
        return {
            markup: undefined,
            channels: undefined,
            resolution: 20
        }
    },
    created() {
        let csId = this.$route.params.csId;
        this.$axios.get(`api/core_sample/${csId}/markup`).then(resp => {
            this.markup = resp.data;
            this.channels = [
                {
                    layers: [
                        {
                            type: "img",
                            settings: {
                                fragmentsWidthFit: "stretch"
                            },
                            data: this.markup.dlImages
                        },

                        {
                            type: "line",
                            settings: {
                                lineColor: "white",
                                fontColor: "white"
                            },
                            data: {
                                oil: this.markup.markup.oil,
                            }
                        }
                    ]
                },

                {
                    layers: [
                        {
                            type: "img",
                            settings: {
                                fragmentsWidthFit: "stretch"
                            },
                            data: this.markup.uvImages
                        },

                        {
                            type: "line",
                            settings: {
                                lineColor: "white",
                                showText: false
                            },
                            data: {
                                oil: this.markup.markup.oil,
                                carbon: this.markup.markup.carbon
                            }
                        }
                    ]
                },

                {
                    layers: [
                        {
                            type: "line",
                            settings: {
                                lineColor: "black",
                                fontColor: "red"
                            },
                            data: {
                                oil: this.markup.markup.oil,
                                carbon: this.markup.markup.carbon
                            }
                        }
                    ]
                }
            ];
             
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