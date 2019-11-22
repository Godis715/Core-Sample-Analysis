<template>
<div>
    <site-header />

    <div id="main">
    <div>
        <h1>Uploaded core samples</h1>
    </div>

    <div id="cs-cont">
        <div id="upload-cs" class="cs-info">
            <div>Upload</div>
        </div>

        <div
            v-for="(info, index) in samplesInfo"
            v-bind:key="'cs-' + index"
            v-bind:class="'cs-info ' + getClassByStatus(info.status)"
        >
            <div class="cs-header">
                <div
                    class="cs-title"
                    v-on:click="redirectToCSView(info)"
                >{{info.csName}}</div>
                <button
                    v-on:click="deleteCoreSample(info.csId)"
                    class="round delete dark-alpha"
                ></button>
            </div>

            <div class="cs-stats-panel">
                <div class="pie-chart-mock"></div>
            </div>
            <div class="info-cont">
                <div>{{info.date|getDate}}</div>
                <div>{{info.date|getTime}}</div>
                <div>Author</div>

                <div
                    v-if="info.status==='notAnalysed'"
                    class="not-analysed-sign"
                >Not analysed</div>

                <div
                    v-if="info.status==='inProcess'"
                    class="in-process-sign"
                >Analysing..</div>
            </div>

            <div class="btn-panel">
                <button
                    class="usual green"
                    v-if="info.status==='notAnalysed'||info.status==='error'"
                    v-on:click="analyseCoreSample(info.csId, index)"
                >Analyse</button>
            </div>
        
        </div>
    </div>
    </div>
</div>
</template>

<style>
    #main {
        margin: 20px;
    }

    #cs-cont {
        display: flex;
        flex-wrap: wrap;
    }

    #upload-cs {
        display: flex;
        flex-direction: column;
        justify-content: center;
        vertical-align: middle;
    }

    #upload-cs > div {
        margin: auto;
    }

    .not-analysed-sign:before {
        content: "";
        display: block;
        width: 20px;
        height: 20px;
        float: left;
        margin-right: 5px;
        background: var(--warning-icon);
        background-size: 20px 20px;
    }

    .in-process-sign:before {
        content: "";
        display: block;
        background: var(--loading-icon);
        width: 20px;
        height: 20px;
        background-size: 20px 20px;
        float: left;
        margin-right: 5px;
        
        animation: 0.5s linear 0s infinite loading-icon;
    }

    @keyframes loading-icon { from { transform: rotate(0deg); } to { transform: rotate(360deg); }  }

    .cs-info {
        margin: 0.4em;
        min-width: 10em;
        min-height: 5em;
        border: 1.3px solid lightgray;
        display: grid;
        width: auto;
        grid-template-columns: auto auto;
        grid-template-rows: auto 5fr auto;
        grid-template-areas: 
            "header header"
            "stats info"
            "btns btns"
    }

    .cs-header {
        grid-area: header;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        padding: 3px;
        border-bottom: 1px solid lightgray;
    }

    .info-cont {
        padding: 0.5em;
        grid-area: info;
        text-align: right;
        font-size: 1em;
    }

    .cs-stats-panel {
        grid-area: stats;
        padding: 0.5em;
    }

    .btn-panel {
        grid-area: btns;
        display: flex;
        justify-content: flex-end;
    }

    .cs-title {
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin: auto;
        font-size: larger;
        font-weight: 600;
        color: rgb(99, 168, 52);
    }

    .cs-info.analysed .cs-title:hover {
        text-decoration: underline;
        cursor: pointer;
    }

    .cs-info.analysed .pie-chart-mock {
        height: 7em;
        width: 7em;
        background-color:rgb(99, 168, 52);
        border-radius: 50%;
    }

    .cs-info:not(.analysed) .pie-chart-mock {
        height: 7em;
        width: 7em;
        background: repeating-linear-gradient(45deg, white ,white 4px, lightgray 2px, lightgray 6px);
        border: 2px solid lightgray;
        background-size: 115px 115px;
        background-repeat: no-repeat;
        border-radius: 50%;
    }

    .cs-info .cs-date {
        text-align: right;
        font-size: 0.7em;
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
                if (info.status !== "analysed") return;
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
                            sample.date = new Date(sample.date);

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
                for (let i = 0; i < samplesInfo.length; ++i) {
                    samplesInfo[i].date = new Date(samplesInfo[i].date);
                }
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
        },

        filters: {
            getDate(date) {
                console.log(date);
                let ds = date.toDateString().split(" ");
                let d = `${ds[2]} ${ds[1]} ${ds[3]}`;
                return d;
            },

            getTime(date) {
                let ts = date.toTimeString().slice(0, 5);
                return ts;
            }
        }
    };
</script>