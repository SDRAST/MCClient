<template>
    <div>
        <div class="scrollable-parent">
            <div class="scrollable-child">
            <ul>
                <li v-if="fileName">
                    <label>File Info</label>
                    <ul>
                        <li class="inline">
                            <label>File Name:</label>{{fileName}}
                        </li>
                        <li class="inline">
                            <label>Timestamp:</label>{{timeStamp}}
                        </li>
                    </ul>
                </li>
                <li v-if="sourceName">
                    <label>Source Info</label>
                    <ul>
                        <li class="inline">
                            <label>Name:</label>{{sourceName}}
                        </li>
                        <li class="inline">
                            <label>Az/El:</label>{{AzEl[0]}}°/{{AzEl[1]}}°
                        </li>
                        <li v-if="flux" class="inline">
                            <label>Flux:</label>{{flux}} Jy
                        </li>
                    </ul>
                </li>
                <li v-if="initOffsets[0]">
                    <label>Offsets</label>
                    <ul>
                        <li class="inline">
                            <label>Initial El:</label>{{initOffsets[0]}}
                        </li>
                        <li class="inline">
                            <label>Initial xEl:</label>{{initOffsets[1]}}
                        </li>
                        <li v-for="(elem, idx) in Object.keys(additionalOffsets)" class="inline">
                            <label>{{elem}}:</label>{{additionalOffsets[elem]}}
                        </li>
                    </ul>
                </li>
                <li v-if="boresightType">
                    <label>Boresight Algorithm Parameters</label>
                    <ul>
                        <li class="inline">
                            <label>Type:</label>{{boresightType}}
                        </li>
                        <li v-for="(elem, idx) in Object.keys(boresightParams)" class="inline">
                            <label>{{elem}}:</label>{{boresightParams[elem]}}
                        </li>
                    </ul>
                </li>
            </ul>
            </div>
        </div>
    <hr/>
    <div class="plot-container">
        <div>
            <boresight-report-channel-selector
                ref="channel-selector-el"
                axis="EL"
                :directions="directionsDisplay"
                @channel-selected="onChannelSelected">
            </boresight-report-channel-selector>
            <boresight-report-channel-selector
                ref="channel-selector-xel"
                axis="XEL"
                :directions="directionsDisplay"
                @channel-selected="onChannelSelected">
            </boresight-report-channel-selector>
        </div>
        <div ref="boresight-plot-container">
            <panel :noBorder="true">
                <d3-static-plot ref="boresight-plot"
                    :options="plotOptions"
                    :plotData="plotData"
                    :width="computedWidth"
                    :height="computedHeight"
                    :key="computedRender">
                </d3-static-plot>
            </panel>
        </div>
    </div>
    </div>
</template>

<script>
import moment from "moment"
import * as log from "loglevel"

import TableRow from "./../TableRow.vue"
import Panel from "./../Panel.vue"
import D3StaticPlot from "./../D3StaticPlot.js"
import BoresightReportChannelSelector from "./BoresightReportChannelSelector.vue"

import util from "./../../util.js"

var logger = log.getLogger("BoresightReport")

export default {
    props:{
        linePlotStyles: {type: Object, default: ()=>{return {}}},
        scatterPlotStyles: {type: Object, default: ()=>{return {}}},
        analyzerObject: {type: Object, default: ()=>{return {"meta_data":{}, "data":{}}}},
        srAxes: {type: Array, default: ()=>{
            return ["X","Y","Z","XT","YT"]
        }}
    },
    components:{
        "d3-static-plot":D3StaticPlot,
        "boresight-report-channel-selector":BoresightReportChannelSelector,
        "panel":Panel,
        "table-row":TableRow
    },
    mounted:function(){
        this.onResize()
        // this.$refs["channel-selector-el"].directions.right.show = false
        window.addEventListener('resize', this.onResize)
    },
    methods:{
        toggleRender(){
            if (this.computedRender === 0){
                this.computedRender = 1
            }else{
                this.computedRender = 0
            }
        },
        reRenderBoresightPlot: function(width, height){
            this.computedWidth = width
            this.computedHeight = height
            this.toggleRender()
        },
        onResize: function(){
            var renderedWidth = this.$refs["boresight-plot-container"].offsetWidth
            this.reRenderBoresightPlot(renderedWidth, renderedWidth)
        },
        updatePlotData(){
            var plotData = []
            Object.keys(this.selectedChannels).forEach((axis)=>{
                var axisObj = this.selectedChannels[axis]
                Object.keys(axisObj).forEach((dir)=>{
                    var chanObj = axisObj[dir]
                    Object.keys(chanObj).forEach((chan)=>{
                        if (! chanObj[chan]){
                            return
                        }
                        let axisDirData = this.analyzerObject["data"][axis][dir]
                        let chanData = axisDirData["channels"][chan]
                        let offsets = axisDirData["offset_data"]
                        let tsysData = chanData["tsys_data"]
                        let fitParams = chanData["fit"]["popt"]
                        let gaussFit = offsets.map(
                            x=>util.gaussFunction(x, fitParams)
                        )
                        plotData.push({
                            x:offsets,
                            y:gaussFit,
                            options:Object.assign(this.linePlotStyles[axis],{type:"line"})
                        })
                        plotData.push({
                            x:offsets,
                            y:tsysData,
                            options:Object.assign(this.scatterPlotStyles[axis],{type:"scatter"})
                        })
                    })
                })
            })
            this.$refs["boresight-plot"].clearPlot()
            this.plotData = plotData
        },
        onChannelSelected(axis, dir, channel, show){
            axis = axis.toLowerCase()
            logger.debug(`onChannelSelected: ${axis}, ${dir}, ${channel}`)
            // logger.debug(`onChannelSelected: ${JSON.stringify(this.analyzerObject["data"])}`)
            // logger.debug(`onChannelSelected: ${JSON.stringify(this.analyzerObject["data"][axis])}`)
            // logger.debug(`onChannelSelected: ${JSON.stringify(this.analyzerObject["data"][axis][dir])}`)
            var plotData = []
            this.selectedChannels[axis][dir][channel] = show
            var singleAxisObj = this.analyzerObject["data"][axis][dir]
            if (singleAxisObj !== null){
                var offset = singleAxisObj.channels[channel]["fit"]["popt"][1]
                var score = singleAxisObj.channels[channel]["fit"]["score"]
                console.log(score[0])
                this.$refs[`channel-selector-${axis}`]
                    .channelsToDisplay[dir][channel].offset = offset.toFixed(2)
                this.$refs[`channel-selector-${axis}`]
                    .channelsToDisplay[dir][channel].score = score[0]
                this.updatePlotData()
            }
        }
    },
    computed:{
        fileName(){
            return this.analyzerObject["meta_data"]["file_name"]
        },
        timeStamp(){
            var timeStamp = this.analyzerObject["meta_data"]["timestamp"]
            var date = moment.utc(timeStamp, "YYYY-DDD-HHhmmmsss")
            var dateFormatted = date.format("dddd, DD of MMMM, YYYY, HH:mm:ss")
            return dateFormatted
        },
        filePath(){
            return this.analyzerObject["meta_data"]["file_path"]
        },
        boresightType(){
            return this.analyzerObject["meta_data"]["boresight_type"]
        },
        boresightParams(){
            var params = [
                "sample_rate",
                "limit",
                "integration_time",
                "rate",
            ]
            var boresightParams = {}
            params.forEach((p)=>{
                if (p in this.analyzerObject["meta_data"]){
                    boresightParams[p] = this.analyzerObject["meta_data"][p]
                }
            })
            return boresightParams
        },
        AzEl(){
            return util.formatRad([
                this.analyzerObject["meta_data"]["az"],
                this.analyzerObject["meta_data"]["el"],
            ])
        },
        RaDec(){
            return util.formatRad([
                this.analyzerObject["meta_data"]["RAJ2000"],
                this.analyzerObject["meta_data"]["DECJ2000"],
            ])
        },
        flux(){
            return this.analyzerObject["meta_data"]["flux"]
        },
        sourceName(){
            return this.analyzerObject["meta_data"]["name"]
        },
        initOffsets(){
            return [
                this.analyzerObject["meta_data"]["initial_el"],
                this.analyzerObject["meta_data"]["initial_xel"]
            ].map((v)=>{
                if (v === undefined){
                    return ""
                }
                return v.toFixed(2)
            })
        },
        additionalOffsets(){
            var offsets = {}
            this.srAxes.forEach((axis)=>{
                if (axis in this.analyzerObject["meta_data"]){
                    offsets[axis] = this.analyzerObject["meta_data"][axis].toFixed(2)
                }
            })
            return offsets
        },
        directionsDisplay(){
            var display = {
                right:{
                    show: false,
                    display: "Right"
                },
                left:{
                    show: false,
                    display: "Left"
                }
            }
            Object.keys(display).forEach((dir)=>{
                if (this.analyzerObject["data"]["el"] === undefined){
                    return
                }
                if (dir in this.analyzerObject["data"]["el"]){
                    if (this.analyzerObject["data"]["el"][dir] !== null){
                        display[dir].show = true
                    }
                }
            })
            return display
        },
        selectedChannels: function(){
            var selected = {}
            Object.keys(this.analyzerObject["data"]).forEach((axis)=>{
                selected[axis] = {}
                let axisObj = this.analyzerObject["data"][axis]
                Object.keys(axisObj).forEach((dir)=>{
                    selected[axis][dir] = {}
                    let singleAxisObj = this.analyzerObject["data"][axis][dir]
                    if (singleAxisObj !== null){
                        let chanObj = singleAxisObj.channels
                        Object.keys(chanObj).forEach((chan)=>{
                            selected[axis][dir][chan] = false
                        })
                    }
                })
            })
            return selected
        }
    },
    watch: {
        analyzerObject(){
            this.toggleRender()
        }
    },
    data: function(){
        return {
            computedHeight:100,
            computedWidth:100,
            computedRender:0,
            plotData:[],
            plotOptions: {
                margin:{top:0,right:40,bottom:40,left:60},
                xLabel:"Offset (mdeg)",
                yLabel:"Tsys (K)",
                axisLabelFontSize:"12px"
            },
            convert: 180. / Math.PI,
        }
    }
}

</script>

<style scoped>

.plot-container {
    display: grid;
    grid-template-columns: 2fr 3fr;
    grid-gap: 0.5rem;
}

.inline {
    display: flex;
    justify-content: start;
}

.inline label {
    padding-right: 0.5rem;
}

</style>
