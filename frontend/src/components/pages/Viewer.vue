<template>
<div>
    <site-header />
    <!--
        Workspace consists of columns, which display
        information about the core sample. Also it has
        setting panel on the top the workspace.

        Each column is a combination of different layers.
        Each layer has its own properties (they are named as settings in code).
        This properties can be changed in setting panel.
    -->
    <div id="setting-panel">
        <div
            v-for="(col, colIndex) in columns"
            v-bind:key="colIndex"
        >
            
        </div>    
    </div>

    <div id="main">
        <div
            v-for="(col, colIndex) in columns"
            v-bind:key="colIndex"
            v-on:contextmenu.prevent="showSettingList(colIndex)"
        >
            <div
                v-if="settingToShow==colIndex"
                class="setting-list"
            >
                <setting-group
                    v-for="(layer, layerIndex) in col.layers"
                    v-bind:key="layerIndex"
                    v-bind:settings="layer.type | createSettingList"
                    v-on:setting-changed="settingChanged($event, colIndex, layerIndex)"
                />
            </div>

            <!-- Component, which combines and draws layers. -->
            <multiple-layer-view
                v-if="!!col"
                v-bind:layers="col.layers"
                v-bind:res="resolution"
                v-bind:absHeight="absHeight"
                v-bind:absWidth="absWidthDL"
                class="column"
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

    .column {
        outline: 2px solid lightgray;
    }

    .setting-list {
        position: absolute;
        left: 700px;
    }
</style>

<script>
import MultipleLayerView from "../fragments/MultipleLayerView"
import { SettingDetails } from '../layers/settingDetails'
import SettingGroup from "../fragments/SettingGroup"
import { MarkupLayer } from "../layers/markupLayer"
import { ImageLayer } from "../layers/imageLayer"
import SiteHeader from "../fragments/Header"

export default {
    name: "Viewer",
    components: {
        SiteHeader,
        MultipleLayerView,
        SettingGroup
    },
    data() {
        return {
            markup: undefined,
            columns: undefined,
            resolution: 20,
            settingToShow: undefined
        }
    },
    created() {
        // id of displaying core sample
        let csId = this.$route.params.csId;

        // getting information to display
        this.$axios.get(`api/core_sample/${csId}/markup`).then(resp => {
            this.markup = resp.data;
            this.columns = [
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
                                showText: false,
                                fontColor: "red"
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
        // it is the same for all columns
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
        settingChanged(ev, columnIndex, layerIndex) {
            console.log(ev);

            this.$set(this.columns[columnIndex].layers[layerIndex].settings, ev.settingName, ev.data);
        },

        showSettingList(colIndex) {
            console.log(colIndex);

            if (this.settingToShow === colIndex) {
            this.settingToShow = undefined;
            } else {
                this.settingToShow = colIndex;
            }
        }
    },

    filters: {
        createSettingList(type) {
            let settingNames =
                (type === "img") ? ImageLayer.settingsList :
                (type === "line") ? MarkupLayer.settingsList : [];

            let settings = [];
            for(let i = 0; i < settingNames.length; ++i) {
                let name = settingNames[i];
                settings.push({
                    ...SettingDetails[name],
                    settingName: name
                });
            }

            return settings;
        }
    }
}
</script>

<style>

</style>