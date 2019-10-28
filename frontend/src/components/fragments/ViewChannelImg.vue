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
import { viewChannelMixin } from "../mixins/ViewChannelMixin"

export default {
    name: "ViewChannelImg",
    mixins: [viewChannelMixin],
    methods: {
        redraw() {
            let frags = this.data;

            let canvas = this.$refs.canvas;
            let ctx = canvas.getContext("2d");

            for (let i = 0; i < frags.length; ++i) {
                let img = new Image();
                img.src = "http:\\\\localhost:8000\\static\\core_sample\\" + frags[i].src;

                let dHeight = (frags[i].bottom - frags[i].top) * this.res;
                
                let dWidth =  frags[i].width * this.res * (frags[i].bottom - frags[i].top) / frags[i].height;

                let dy = frags[i].top * this.res;

                switch(this.settings.fragmentsWidthFit) {
                    case "alignLeft":
                    img.onload = () => ctx.drawImage(img, 0, dy, dWidth, dHeight);
                    break;

                    case "alignRight":
                    img.onload = () => ctx.drawImage(img, this.width - dWidth, dy, this.width, dHeight);
                    break;

                    case "stretch":
                    img.onload = () => ctx.drawImage(img, 0, dy, this.width, dHeight);
                    break;
                }
            }
        }
    }
}
</script>>