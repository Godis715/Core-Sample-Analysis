<template>
<div id="cs-cont">
    <div id="dl-col">
        <!-- check if array with image refs is not empty then show images
             else just show background -->
        <div v-for="(n, index) in dlImgsLow.length" :style="dlImgsLow[index].size">
            <img v-if="dlImgs[index]" :src="dlImgs[index].src" class="cs-frag">
            <div v-else class="cs-frag-mock"></div>
        </div>
    </div>

    <div id="uv-col">
        <div v-for="(n, index) in uvImgsLow.length" :style="uvImgsLow[index].size">
            <img v-if="uvImgs[index]" :src="uvImgs[index].src" class="cs-frag">
            <div v-else class="cs-frag-mock"></div>
        </div>
    </div>
</div>
</template>

<style>
    #cs-cont {
        display: flex;
        flex-direction: row;
    }

    .cs-frag {
        width: 100px;
    }

    .cs-frag-mock {
        height: 100%;
        width: 100%;
        background-color: gray;
    }

    img {
        max-width: 100%;
        height: 100%;
        vertical-align: bottom;
    }
</style>

<script>
export default {
    name: 'progressive-cs-viewer',
    // refs on images in low and high resolution
    props: ['dlImgsLow', 'uvImgsLow', 'dlImgsHigh', 'uvImgsHigh'],
    data() {
        return {
            // images to show
            dlImgs: [],
            uvImgs: []
        }
    },

    created() {
        for(let i = 0; i < this.dlImgsLow.length; ++i) {
            this.dlImgsLow[i].render = () => this.$set(this.dlImgs, i, this.dlImgsLow[i]);
            this.dlImgsHigh[i].render = () => this.$set(this.dlImgs, i, this.dlImgsHigh[i]);
            this.uvImgsLow[i].render = () => this.$set(this.uvImgs, i, this.uvImgsLow[i]);
            this.uvImgsHigh[i].render = () => this.$set(this.uvImgs, i, this.uvImgsHigh[i]);
        }

        var lowImgs = this.dlImgsLow.concat(this.uvImgsLow);
        this.loadImages(lowImgs).then(() => {
            console.log('loaded!')
            var highImgs = this.dlImgsHigh.concat(this.uvImgsHigh);
            this.loadImages(highImgs);
        });
    },

    methods: {
        loadImages(imgs) {
            function loadImage(imgSrc) {
                return new Promise((resolve, reject) => {
                    var img = new Image();
                    img.src = imgSrc;
                    img.onload = () => resolve();    
                });
            }

            var promises = [];
            for(let i = 0; i < imgs.length; ++i) {
                var prom = loadImage(imgs[i].src).then(() => {
                    imgs[i].render();
                });
                promises.push(prom);
            }

            return Promise.all(promises);
        }
    }
};
</script>