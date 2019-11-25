<template>
<canvas
    ref="chartCanvas"
    v-bind:height="actualSize+'px'"
    v-bind:width="actualSize+'px'"
></canvas>
</template>

<script>
    function drawPieSlice(ctx, centerX, centerY, radius, startAngle, endAngle, color ) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(centerX,centerY);
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.closePath();
        ctx.fill();
    }

    export default {
        name: "MultiplePieChart",
        props: {
            chartData: {
                type: Array,
                required: true
            },
            size: {
                type: Number,
                required: true
            }
        },
        data() {
            return {
                actualSize: 0
            }
        },
        methods: {
            redraw() {
                this.clearCanvas();

                let res = window.devicePixelRatio;
                this.actualSize = Math.floor(this.size * res);

                this.$nextTick(() => {
                    this.ctx.scale(res, res);
                    for (let i = 0; i < this.chartData.length; ++i) {
                        let data = this.chartData[i];

                        let angle = 0;
                        let radius = this.size * (1 - i / (this.chartData.length + 1)) / 2;
                        for (let j = 0; j < data.slices.length; ++j) {
                            let slice = data.slices[j];

                            drawPieSlice(this.ctx, this.size / 2, this.size / 2, radius, angle - slice.angle, angle, slice.color);
                            angle -= slice.angle;
                        }
                    }
                    this.ctx.scale(1 / res, 1 / res);
                });
            },

            clearCanvas() {
                this.ctx.fillStyle = "white";
                this.ctx.fillRect(0, 0, this.canvas.clientWidth, this.canvas.clientHeight);
            }
        },
        mounted() {
            this.canvas.style.width = this.size+"px";
            this.canvas.style.height = this.size+"px";
            
            this.$nextTick(this.redraw());
            window.addEventListener("resize", this.redraw, false);

            this.actualSize = Math.floor(window.devicePixelRatio * this.size);
        },
        computed: {
            canvas() {
                return this.$refs.chartCanvas;
            },
            ctx() {
                return this.$refs.chartCanvas.getContext("2d");
            }
        }
    };
</script>