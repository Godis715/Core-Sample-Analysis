export const viewChannelMixin = {
    props: [
        "res",
        "absWidth",
        "absHeight",
        "data",
        "settings"
    ],
    mounted() {
        this.redraw();
    },
    watch: {
        // when res is changed => redraw
        res() {
            this.redraw();
        }
    },
    computed: {
        width() {
            return this.res * this.absWidth;
        },
        height() {
            return this.res * this.absHeight;
        }
    }
};