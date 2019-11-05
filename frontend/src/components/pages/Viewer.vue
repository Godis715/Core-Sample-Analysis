<template>
<div>
    <site-header />
    <setting-group 
        title="Global settings"
        v-bind:settings="settings"
        v-on:setting-changed="settingChanged($event)"
    />

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
import SettingGroup from "../fragments/SettingGroup"

export default {
    name: "Viewer",
    components: {
        SiteHeader,
        ViewChannelMultiple,
        SettingGroup
    },
    data() {
        return {
            markup: undefined,
            channels: undefined,
            resolution: 20,
            settings: [
                {
                    type: "radio",
                    title: "image width fit",
                    options: [
                        {
                            name: "align left",
                            value: "alignLeft"
                        }, 
                        {
                            name: "align right",
                            value: "alignRight"
                        }, 
                        {
                            name: "stretch",
                            value: "stretch"
                        }
                    ]       
                }
            ]
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
    },
    methods: {
        settingChanged(ev) {
            console.log(ev);
            for(let i = 0; i < this.channels.length; ++i) {
                let ch = this.channels[i];
                for (let j = 0; j < ch.layers.length; j++) {
                    let l = ch.layers[j];
                    l.settings.fragmentsWidthFit = ev;
                }
            }
        }
    }
}
</script>

<style>

</style>