<template>
<div>
    <site-header></site-header>
    <progressive-cs-viewer
        :dlImgsLow="dlLow"
        :uvImgsLow="uvLow"
        :dlImgsHigh="dlHigh"
        :uvImgsHigh="uvHigh"
    ></progressive-cs-viewer>
</div>
</template>

<script>
    import SiteHeader from '../fragments/Header.vue';
    import ProgressiveCSViewer from '../fragments/ProgressiveCSViewer.vue';

    export default {
        name: 'Account',
        components: { SiteHeader, 'progressive-cs-viewer': ProgressiveCSViewer },
        data() {
            return {
                dlLow: [
                    { 
                        src: 'https://vk.com/doc257617715_519686473?hash=fe739cd68b31871ae4&dl=6e1d321a1277722745',
                        size: { height: '500px', width: '50px' }
                    },

                    { 
                        src: '',
                        size: { height: '', width: '' }
                    }
                ],
                uvLow: [

                ],
                dlHigh: [

                ],
                uvHigh: [

                ]
            }
        }
    };
</script>