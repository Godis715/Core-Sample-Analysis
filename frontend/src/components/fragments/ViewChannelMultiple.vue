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
import { imgCh } from "../channels/imgCh"
import { lineMarkupCh } from "../channels/lineMarkupCh"

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
            let imgChnl = this.layers.find(ch => ch.type === "img");
            let lineChnl = this.layers.find(ch => ch.type === "line");

            let canvas = this.$refs.canvas;
            let ctx = canvas.getContext("2d");
            ctx.beginPath();
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, this.width, this.height);

            if (imgChnl)
                imgCh.draw(canvas, imgChnl.data, this.width, this.res, imgChnl.settings);

            if (lineChnl) {
                let merged = lineMarkupCh.mergeMarkup(lineChnl.data);
                let multi = lineMarkupCh.single2multiTypeLayers(merged);
                lineMarkupCh.draw(canvas, multi, this.width, this.res, lineChnl.settings);
            }
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