<template>
<div>
    <site-header v-once/>
    <!--
        Workspace consists of columns, which display
        information about the core sample. Also it has
        setting panel on the top the workspace.

        Each column is a combination of different layers.
        Each layer has its own properties (they are named as settings in code).
        This properties can be changed in setting panel.
    -->

    <draggable-menu
        v-if="settingToShow > -1"
        v-show="showMenu"
        v-bind:title="`Column ${settingToShow+1}`"
        v-on:close-menu="closeMenu"
    >
        <template>
            <div>
            <setting-group
                v-for="(layer, layerIndex) in columns[settingToShow].layers"
                v-on:setting-changed="settingChanged($event, settingToShow, layerIndex)"
                v-bind:settings="layer.settings | createSettingList"
                v-bind:key="layer.id"
                v-bind:id="layer.id"
                class="setting-group"
            />
            </div>
        </template>
    </draggable-menu>

    <div id="main">
        <div
            v-for="(col, colIndex) in columns"
            v-bind:key="colIndex"
            class="column-wrapper"
        >
            <div class="column-wrapper-header">
                <button class="show-settings-btn" v-on:click="showSettingList(colIndex)">...</button>
                <button class="close-column-btn">x</button>
            </div>
            <!-- Component, which combines and draws layers. -->
            <multiple-layer-view
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
        margin-top: 25px;
        display: flex;
        flex-direction: row;
    }

    .setting-group {
        background-color: white;
        padding: 5px;
        padding-right: 2em;
        padding-bottom: 1em;
        margin: 5px 5px 0 5px;
    }

    .setting-group:first-child {
        margin-top: 0;
    }

    .column-wrapper {
        padding-top: 0;
        background-color: whitesmoke;
        border: 1.3px solid lightgray;
        margin: 5px;
    }

    .column-wrapper-header {
        background-color: lightgray;
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
    }

    .column {
        margin: 10px;
        outline: 2px solid gray;
    }

    .show-settings-btn {
        border: none;
        outline: none;
        cursor: pointer;
        background: darkgray;
        color: white;
        text-align: center;
        margin: 5px;
        border-radius: 10%;
    }

    .close-column-btn {
        border: none;
        border-radius: 50%;
        outline: none;
        cursor: pointer;
        background: darkgray;
        color: white;
        text-align: center;
        margin: 5px;
        margin-left: 0;
    }
</style>

<script>
import MultipleLayerView from "../fragments/MultipleLayerView"
import { SettingDetails } from '../layers/settingDetails'
import SettingGroup from "../fragments/SettingGroup"
import { MarkupLayer } from "../layers/markupLayer"
import { ImageLayer } from "../layers/imageLayer"
import DraggableMenu from "../fragments/DraggableMenu"
import SiteHeader from "../fragments/Header"

export default {
    name: "Viewer",
    components: {
        SiteHeader,
        MultipleLayerView,
        SettingGroup,
        DraggableMenu
    },
    data() {
        return {
            markup: undefined,
            columns: [],
            resolution: 15,
            settingToShow: -1,
            showMenu: false,
            colSettingToShow: undefined
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
                            id: "layer-1",
                            type: "img",
                            data: this.markup.dlImages,
                            settings: { ...ImageLayer.defaultSettings },
                        },

                        {
                            id: "layer-2",
                            type: "line",
                            data: {
                                oil: this.markup.markup.oil,
                            },
                            settings: { ...MarkupLayer.defaultSettings }
                        }
                    ]
                },

                {
                    layers: [
                        {
                            id: "layer-1",
                            type: "img",
                            data: this.markup.uvImages,
                            settings: { ...ImageLayer.defaultSettings },
                        },

                        {
                            id: "layer-2",
                            type: "line",
                            data: {
                                oil: this.markup.markup.oil,
                                carbon: this.markup.markup.carbon
                            },
                            settings: { ...MarkupLayer.defaultSettings }
                        }
                    ]
                },

                {
                    layers: [
                        {
                            id: "layer-1",
                            type: "line",
                            data: {
                                oil: this.markup.markup.oil,
                                carbon: this.markup.markup.carbon
                            },
                            settings: { ...MarkupLayer.defaultSettings }
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
        }
    },
    methods: {
        settingChanged(ev, columnIndex, layerIndex) {
            this.$set(this.columns[columnIndex].layers[layerIndex].settings, ev.settingName, ev.data);
        },

        showSettingList(colIndex) {
            if (this.showMenu && this.settingToShow === colIndex) {
                this.showMenu = false;
            } else {
                this.settingToShow = colIndex;
                this.showMenu = true;
            }
        },

        closeMenu() {
            this.showMenu = false;
        }
    },
    filters: {
        createSettingList(settings) {
            let settingList = [];
            let settingNames = Object.keys(settings);
            for(let i = 0; i < settingNames.length; ++i) {
                let name = settingNames[i];
                settingList.push({
                    ...SettingDetails[name],
                    settingName: name,
                    value: settings[name]
                });
            }
            return settingList;
        }
    }
}
</script>

<style>

</style>