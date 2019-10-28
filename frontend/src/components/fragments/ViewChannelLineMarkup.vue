<template>
<div>
    <div
        v-if="classLabel!==''"
        class="class-label"
        v-bind:style="`left:${left};width:${Math.floor(width)-10}px`"
    >{{classLabel}}</div>
    <canvas
        ref="canvas"
        v-bind:width="width"
        v-bind:height="height"
        ClipToBounds="True"
    ></canvas>
</div>
</template>

<style>
    .class-label {
        position: fixed;
        background-color: cadetblue;
        padding: 5px;
        top: 0;
        font-size: 20px
    }
</style>

<script>
import { viewChannelMixin } from "../mixins/ViewChannelMixin"

export default {
    name: "ViewChannelLineMarkup",
    mixins: [viewChannelMixin],
    data() {
        return {
            left: 0,
            classLabel: "",
        }
    },
    methods: {
        redraw() {
            let layers = this.data;
            console.log(layers);
            let canvas = this.$refs.canvas;
            let ctx = canvas.getContext("2d");

            setTimeout(() => {
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(0, 0, this.width, this.height);

                ctx.fillStyle = "#000000";
                for (let i = 0; i < layers.length; ++i) {
                    let topPx = layers[i].top * this.res;
                    ctx.beginPath();
                    ctx.moveTo(0, topPx);
                    ctx.lineTo(this.width, topPx);
                    ctx.stroke();

                    let fontSize = 20;
                    ctx.font = `${fontSize}px Arial`;
                    ctx.fillText(layers[i].class, 0, topPx + fontSize);
                }
            }, 250);
        }
    },
    created() {
        window.addEventListener("scroll", ev => {
            let canvas = this.$refs.canvas;
            if (!canvas) return;

            this.left = canvas.offsetLeft;

            // cross browser
            let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            let canvasTop = canvas.offsetTop;

            let onCanvasY = scrollTop - canvasTop;
            if (onCanvasY < 0) {
                this.classLabel = "";
                return;
            }

            let layers = this.data;
            for (let i = 0; i < layers.length; ++i) {
                let topPx = layers[i].top * this.res;
                let bottomPx = layers[i].bottom * this.res;
                if (onCanvasY >= topPx && onCanvasY < bottomPx) {
                    console.log(layers[i].class);
                    this.classLabel = layers[i].class;
                    break;
                }
            }
        });
    }
}
</script>