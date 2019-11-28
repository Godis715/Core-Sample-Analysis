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
    <div id="viewer-root">
        <div id="main-cont-viewer">
            <div
                v-for="(col, colIndex) in columns"
                v-bind:key="colIndex"
                v-bind:class="'column-wrapper '+((settingToShow === colIndex)?'selected':'')">
                <div class="column-wrapper-header">
                    <button class="show-settings-btn smooth-rect dark-alpha" v-on:click="showSettingList(colIndex)">...</button>
                    <button class="delete round dark-alpha"></button>
                </div>
                <!-- Component, which combines and draws layers. -->
                <multiple-layer-view
                    v-bind:layers="col.layers"
                    v-bind:res="resolution"
                    v-bind:absHeight="absHeight"
                    v-bind:absWidth="absWidthDL"
                    class="column" />
            </div>
        </div>
        <div 
            id="setting-menu"
            ref="settingMenu"
            >
            <div
                v-on:close-menu="closeMenu">
                <div>
                    <h2>Global settings</h2>
                    <setting-group
                        v-on:setting-changed="settingChanged($event, settingToShow, layerIndex)"
                        v-bind:settings="[
                            {
                                settingName: 'resolution',
                                value: 30,
                                title: 'Resolution',
                                type: 'number',
                                default: 30,
                                min: 5,
                                max: 50,
                            }
                        ]"
                        v-bind:key="'global-settings'"
                        id="global-settings"
                        class="setting-group"
                    />
                </div>
                <div 
                    v-if="settingToShow > -1"
                    v-show="showMenu">
                    <h2>{{`Column ${settingToShow+1}`}}</h2>
                    <setting-group
                        v-for="(layer, layerIndex) in columns[settingToShow].layers"
                        v-on:setting-changed="settingChanged($event, settingToShow, layerIndex)"
                        v-bind:settings="layer.settings | createSettingList"
                        v-bind:title="layer.id"
                        v-bind:key="layer.id"
                        v-bind:id="layer.id"
                        class="setting-group"
                    />
                </div>
                
            </div>
        </div>
    </div>
</div>
</template>

<style>
    #viewer-root {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

    #main-cont-viewer {
        display: flex;
        flex-direction: row;
    }

    #setting-menu {
        min-width: 15em;
        max-height: 500px;
        border: 1.3px solid lightgray;
        height: fit-content;
        padding: 0 1em 5em 1em;
        margin: 5px;
        overflow-y: auto;
        position: sticky;
        top: 5px;
    }

    .setting-group {
        border: 1.3px solid lightgray;
        padding: 0 0.8em 0.8em 0.8em;
    }

    .setting-group:not(:last-child) {
        margin-bottom: 1em;
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

    .column-wrapper.selected {
        border: 1.3px solid rgb(17, 187, 17);
        outline: 1px solid rgb(17, 187, 17);
    }

    .column-wrapper-header {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
    }

    .column {
        margin: 0 10px 10px 10px;
        outline: 2px solid rgb(128, 128, 128);
    }

    .show-settings-btn {
        height: 20px;
        margin: 5px;
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
            resolution: 25,
            settingToShow: -1,
            showMenu: false,
            colSettingToShow: undefined
        }
    },
    created() {
        // id of displaying core sample
        let csId = this.$route.params.csId;

        // getting information to display
        this.$axios.get(`api/core_sample/${csId}/markup/`).then(resp => {
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
                this.settingToShow = -1;
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
    mounted() {
        
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