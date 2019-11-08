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
        },

        // watch if at least one of settings component has changed
        settings: {
            deep: true,
            handler() {
                this.redraw();
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
    }
};