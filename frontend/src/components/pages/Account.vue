<template>
<div>
    <site-header />

    <div id="cs-cont">
        <div id="upload-cs" class="cs-info">Upload</div>
        <div
            v-for="(info, index) in samplesInfo"
            v-bind:key="'cs-' + index"
            v-bind:class="'cs-info ' + getClassByStatus(info.status)"
        >
            <div class="cs-name">{{info.csName}}</div>
            <div class="cs-date">{{info.date}}</div>

            <button v-on:click="redirectToCSView(info)">Open</button>
            <button
                v-if="info.status==='notAnalysed'||info.status==='error'"
                v-on:click="analyseCoreSample(info.csId, index)">Analyse</button>
            <button v-on:click="deleteCoreSample(info.csId)">Delete</button>
        </div>
    </div>
</div>
</template>

<style>
    #cs-cont {
        display: flex;
        flex-wrap: wrap;
    }

    .cs-info {
        border-radius: 8px;
        padding: 0.8em;
        margin: 0.4em;
    }

    #upload-cs {
        display: flex;
        vertical-align: middle;
        justify-content: center;
    }

    .cs-info .cs-name {
        font-weight: bolder;
    }

    .cs-info .cs-date {
        font-size: smaller;
        text-align: right;
    }

    .cs-info .cs-status {
        margin-top: 1em;
    }

    .cs-info.analysed {
        background-color: whitesmoke;
        cursor: pointer;
    }

    .cs-info.not-analysed {
        background-color: rgb(240, 240, 145);
        cursor: pointer;
    }

    .cs-info.in-process {
        background-color: rgb(199, 239, 255);
        cursor: pointer;
    }

    .cs-info.error {
        background-color: pink;
    }
</style>

<script>
    import SiteHeader from "../fragments/Header.vue";

    export default {
        name: "Account",
        components: { SiteHeader },
        data() {
            return {
                samplesInfo: [],
            }
        },

        methods: {
            getClassByStatus(status) {
                return status === "analysed" ? "analysed" :
                    status === "notAnalysed" ? "not-analysed" :
                    status === "inProcess" ? "in-process" :
                    "error";
            },

            redirectToCSView(info) {
                if (info.status === "error") return;
                this.$router.push(`view/${info.csId}`);
            },

            refreshInProcess() {                
                let csIds = [];
                this.samplesInfo.forEach(info => {
                    if (info.status === 'inProcess') {
                        csIds.push(info.csId);
                    }
                });

                this.$axios.put('api/core_sample/status', csIds).then(resp => {
                    this.samplesInfo.forEach((info, index) => {
                        console.log(resp.data.statuses);
                        if (resp.data.statuses[info.csId]) {
                            console.log("Before: " + JSON.stringify(this.samplesInfo));

                            let sample = this.samplesInfo[index];
                            sample.status = resp.data.statuses[info.csId];

                            this.$set(this.samplesInfo, index, sample);
                            console.log("After: " + JSON.stringify(this.samplesInfo));
                        }
                    });
                    if (this.samplesInfo.some(info => info.status === "inProcess")) {
                        console.log('Wow');
                        this.startRefresh();
                    }
                }).catch(err => {
                    console.error(err.response);
                });
            },

            deleteCoreSample(csId) {
                this.samplesInfo = this.samplesInfo.filter(info => info.csId !== csId);
                this.$axios.delete(`api/core_sample/${csId}/delete`).then(() => {
                    console.log('Deleted');
                }).catch(err => {
                    console.error(err);
                });
            },

            startRefresh() {
                this.refreshTimeout = setTimeout(this.refreshInProcess.bind(this), 2000);
            },

            analyseCoreSample(csId, index) {
                this.$axios.put(`api/core_sample/${csId}/analyse`).then(resp => {
                    console.log("start analysing..");

                    let sample = this.samplesInfo[index];
                    sample.status = 'inProcess';
                    this.$set(this.samplesInfo, index, sample);

                    this.startRefresh();
                }).catch(err => {
                    console.error(err);

                    let sample = this.samplesInfo[index];
                    sample.status = 'error';
                    this.$set(this.samplesInfo, index, sample);
                });
            }
        },

        created() {
            this.$axios.get('api/core_sample').then(resp => {
                console.log(resp.data);

                let samplesInfo = resp.data;
                samplesInfo.forEach(info => {
                    info.date = info.date.substring(0, 10);
                });

                this.samplesInfo = samplesInfo;

                let has_NotAnalysed = samplesInfo.some(info => info.status === 'inProcess');
                if (has_NotAnalysed) {
                    this.startRefresh();
                }

            }).catch(err => {
                console.log(err);
            })
        },

        destroyed() {
            if (this.refreshTimeout)
                clearTimeout(this.refreshTimeout);
        }
    };
</script>