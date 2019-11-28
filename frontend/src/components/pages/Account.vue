<template>
<div>
    <site-header />

    <div id="main-cont-account">
    <div id="upper-label">
        <span>Uploaded core samples</span>
        <div></div>
    </div>

    <transition-group
        name="cs-info-appearing"
        id="cs-cont">
        <div id="upload-cs" class="cs-info" key="upload">
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
                    v-on:click="requestForDeleting(info.csId, info.csName)"
                    class="round delete dark-alpha"
                ></button>
            </div>

            <div class="cs-stats-panel">
                <multiple-pie-chart 
                    v-if="info.status==='analysed' && !!info.stats"
                    v-bind:size="100"
                    v-bind:chartData="info.stats|convertStatsToChartData"
                />
                <div
                    v-else
                    class="pie-chart-mock"
                ></div>
            </div>
            <div class="info-cont">
                <div>{{info.date|getDate}}</div>
                <div>{{info.date|getTime}}</div>
                <div>Author</div>

                <div
                    v-if="info.status==='notAnalysed'"
                    class="not-analysed-sign"
                    v-on:click="analyseCoreSample(info.csId, index)"
                >Start analysis</div>

                <div
                    v-if="info.status==='inProcess'"
                    class="in-process-sign"
                >Analysing..</div>

                <div
                    v-if="info.status==='analysed'"
                    class="legend">
                    <span class="oil">Oil</span>
                    <span class="carbon">Carbon</span>
                    <span class="rock">Rock</span>
                    <span class="ruin">Ruin</span>
                </div>
            </div>
        </div>
    </transition-group>
    </div>
</div>
</template>

<style>
    #main-cont-account {
        margin: 20px;
    }

    #cs-cont {
        display: flex;
        flex-basis: 100%;
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

    .not-analysed-sign:hover {
        cursor: pointer;
        text-decoration: underline;
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
        transition: 2s;
        margin: 0.4em;
        width: 17em;
        border: 1.3px solid lightgray;
        display: grid;
        grid-template-columns: auto auto;
        grid-template-rows: auto 5fr;
        grid-template-areas: 
            "header header"
            "stats info"
    }

    .cs-header {
        grid-area: header;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        padding: 3px;
        border-bottom: 1px solid lightgray;
        overflow: hidden;
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

    .cs-title {
        padding: 0 0.5em;
        display: block;
        justify-content: center;
        margin: auto;
        font-size: larger;
        font-weight: 600;
        color: rgb(99, 168, 52);
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
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
        border: 2px solid lightgray;
        background-size: 115px 115px;
        background-repeat: no-repeat;
        border-radius: 50%;
    }

    .cs-info .cs-date {
        text-align: right;
        font-size: 0.7em;
    }

    .legend > span {
        display: block;
        text-align: left;
    }
    .legend > span::after {
        display: block;
        content: "";
        height: 10px;
        width: 10px;
        border: 1px solid gray;
        float: left;
        margin-right: 5px;
    }

    .legend > .rock::after {
        background-color: gray;
    }

    .legend > .oil::after {
        background-color: green;
    }

    .legend > .carbon::after {
        background-color: orange;
    }

    .legend > .ruin::after {
        background-color: black;
    }

    .cs-info-appearing-enter-active, .cs-info-appearing-leave-active {
        transition: opacity .25s;
    }

    .cs-info-appearing-enter {
        opacity: 0;
    }

    #upper-label {
        display: flex;
        flex-direction: column;
        font-size: 1.3em;
        margin-bottom: 1em;
    }

    #upper-label > div {
        width: 100%;
        height: 1.3px;
        background-color: lightgray;
    }
</style>

<script>
    import SiteHeader from "../fragments/Header";
    import MultiplePieChart from "../fragments/MultiplePieChart";

    export default {
        name: "Account",
        components: {
            SiteHeader,
            MultiplePieChart
        },
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

            refreshChartData(csIds) {
                return this.$axios.put("api/core_sample/statistics/", csIds).then(resp => {
                    for (let csId in resp.data) {
                        let stats = resp.data[csId];
                        let csInfo = this.samplesInfo.find(i => i.csId === csId);
                        this.$set(csInfo, "stats", stats);
                    }
                });
            },

            refreshInProcess() {                
                let csIds = [];
                this.samplesInfo.forEach(info => {
                    if (info.status === 'inProcess') {
                        csIds.push(info.csId);
                    }
                });

                this.$axios.put('api/core_sample/status/', csIds).then(resp => {
                    let analysed = [];
                    this.samplesInfo.forEach((info, index) => {
                        if (resp.data.statuses[info.csId]) {
                            let sample = this.samplesInfo[index];
                            sample.status = resp.data.statuses[info.csId];
                            sample.date = new Date(sample.date);

                            this.$set(this.samplesInfo, index, sample);

                            if (resp.data.statuses[info.csId] === "analysed") {
                                analysed.push(info.csId);
                            }
                        }
                    });
                    if (this.samplesInfo.some(info => info.status === "inProcess")) {
                        this.startRefresh();
                    }
                    if (analysed.length > 0) {
                        this.refreshChartData(analysed).catch(err => {
                            console.error(err);
                        });
                    }
                }).catch(err => {
                    console.error(err.response);
                });
            },

            requestForDeleting(csId, name) {
                let nameToValidate = prompt("To delete core sample, enter the first 3 letters of its name", undefined);
                let requiredStr = name.substring(0, 3);
                if (!nameToValidate) return;

                if (nameToValidate === requiredStr) {
                    this.deleteCoreSample(csId);
                } else {
                    alert("Entered letters are not correct! Operation canceled");
                }
            },

            deleteCoreSample(csId) {
                this.samplesInfo = this.samplesInfo.filter(info => info.csId !== csId);
                this.$axios.delete(`api/core_sample/${csId}/delete/`).then(() => {
                    console.log('Deleted');
                }).catch(err => {
                    console.error(err);
                });
            },

            startRefresh() {
                this.refreshTimeout = setTimeout(this.refreshInProcess.bind(this), 2000);
            },

            analyseCoreSample(csId, index) {
                this.$axios.put(`api/core_sample/${csId}/analyse/`).then(resp => {
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
            },

            refreshStatsFor(samplesInfo) {

            }
        },

        created() {
            this.$axios.get('api/core_sample/').then(resp => {
                let samplesInfo = resp.data;
                for (let i = 0; i < samplesInfo.length; ++i) {
                    samplesInfo[i].date = new Date(samplesInfo[i].date);
                }
                this.samplesInfo = samplesInfo;

                let has_NotAnalysed = samplesInfo.some(info => info.status === 'inProcess');
                if (has_NotAnalysed) {
                    this.startRefresh();
                }
            }).then(() => {
                let csIds = [];
                this.samplesInfo.forEach(info => {
                    if (info.status === "analysed")
                        csIds.push(info.csId);
                });
                console.log("getting stats");
                return this.refreshChartData(csIds);
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
                let ds = date.toDateString().split(" ");
                let d = `${ds[2]} ${ds[1]} ${ds[3]}`;
                return d;
            },

            getTime(date) {
                let ts = date.toTimeString().slice(0, 5);
                return ts;
            },

            convertStatsToChartData(stats) {
                const pn = Object.freeze(["oil", "carbon", "rock"]);
                const pl = Object.freeze({
                    oil: {
                        high: "#00fd13",
                        low: "#15da48",
                        notDefined: "#115a27"
                    },
                    carbon: {
                        high: "#ff4700",
                        low: "#ffa500",
                        notDefined: "#671f09"
                    },
                    rock: {
                        mudstone: "black", 
                        sandstone: "#b3a590",
                        siltstone: "gray",
                        other: "pink"
                    }
                });

                let chartData = [];
                for (let i = 0; i < pn.length; ++i) {
                    let paramName = pn[i];
                    let pStats = stats[paramName];
                    let classes = pl[paramName];
                    let slices = [];
                    for (let className in classes) {
                        slices.push({
                            angle: 2 * Math.PI * pStats[className],
                            color: classes[className]
                        });
                    }
                    chartData[i] = {
                        slices: slices
                    };
                }
                return chartData;
            }
        }
    };
</script>