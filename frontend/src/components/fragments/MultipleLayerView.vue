<template>
<div>
    <canvas
        ref="canvas"
        v-bind:width="width"
        v-bind:height="height"
    ></canvas>
</div>
</template>

<script>
import { ImageLayer } from "../layers/imageLayer"
import { MarkupLayer } from "../layers/markupLayer"

export default {
    name: "ViewChannelMultiple",
    props: [
        "res",
        "absWidth",
        "absHeight",
        "layers"
    ],
    methods: {
        redraw() {
            let imgLayer = this.layers.find(ch => ch.type === "img");
            let markupLayer = this.layers.find(ch => ch.type === "line");

            let canvas = this.$refs.canvas;
            let ctx = canvas.getContext("2d");
            ctx.beginPath();
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, this.width, this.height);

            this.$nextTick(() => {
                new Promise((res, rej) => {
                    if (!imgLayer) res();
                    ImageLayer.draw(canvas, imgLayer.data, this.width, this.res, imgLayer.settings).then(res);
                }).then(() => {
                    if (!markupLayer) return;
                    let merged = MarkupLayer.mergeMarkup(markupLayer.data);
                    let multi = MarkupLayer.single2multiTypeLayers(merged);
                    MarkupLayer.draw(canvas, multi, this.width, this.res, markupLayer.settings);
                });
            });

        }
    },
    computed: {
        width() {
            return this.res * this.absWidth;
        },
        height() {
            return this.res * this.absHeight;
        }
    },
    mounted() {
        this.redraw();
    },
    watch: {
        // when res is changed => redraw
        res() {
            this.redraw();
        },

        // watch if at least one of settings component has changed
        layers: {
            deep: true,
            handler() {
                this.redraw();
            }
        }
    }
}
</script>