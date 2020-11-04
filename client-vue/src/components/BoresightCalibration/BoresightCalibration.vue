
<template>
    <collapsable-panel :header="header" ref="main-panel">
        <div class="container">
            <div>
            <panel header="Run">
                <boresight-run
                    ref="boresight-run"
                    :axes="axes"
                    @boresight-run="onBoresightToggle">
                </boresight-run>
            </panel>
            </div>
            <div>
            <panel header="Load">
                <boresight-load
                    ref="boresight-load"
                    :filePaths="filePaths"
                    @load="onLoad"
                    @load-most-recent="onLoadMostRecent">
                </boresight-load>
            </panel>
            </div>
            <panel header="Report">
                <boresight-report
                    ref="boresight-report"
                    :analyzerObject="analyzerObject"
                    :linePlotStyles="linePlotStyles"
                    :scatterPlotStyles="scatterPlotStyles"
                    :srAxes="srAxes">
                </boresight-report>
            </panel>
        </div>
    </collapsable-panel>
</template>

<script>
import * as log from "loglevel"

import D3StaticPlot from "./../D3StaticPlot.js"
import CollapsablePanel from "./../CollapsablePanel.vue"
import SpinBox from "./../SpinBox.vue"
import DropDown from "./../DropDown.vue"
import TableRow from "./../TableRow.vue"
import StartStopButton from "./../StartStopButton.vue"
import CheckButton from "./../CheckButton.vue"
import Panel from "./../Panel.vue"
import SocketIOMixin from "./../SocketIOMixin.vue"

import BoresightRun from "./BoresightRun.vue"
import BoresightLoad from "./BoresightLoad.vue"
import BoresightReport from "./BoresightReport.vue"

import util from "./../../util.js"

var logger = log.getLogger("BoresightCalibration")

export default {
    mixins:[SocketIOMixin],
    components:{
        "collapsable-panel":CollapsablePanel,
        "d3-static-plot":D3StaticPlot,
        "drop-down": DropDown,
        "spin-box": SpinBox,
        "table-row":TableRow,
        "start-stop-button":StartStopButton,
        "check-button":CheckButton,
        "panel":Panel,
        "boresight-run": BoresightRun,
        "boresight-load": BoresightLoad,
        "boresight-report": BoresightReport
    },
    props:{
        sourceForObservation: {type:Object, default:()=>{return null}},
        info: {type:Object, default:()=>{return {}}}
    },
    methods:{
        onBoresightToggle(value){
            if (value){
                this.startBoresight()
            }else{
                this.stopBoresight()
            }
        },
        onLoad(filePath){
            // logger.debug(`BoresightCalibration.onLoad: ${filePath}`)
            this.serverCommand(
                "get_boresight_analyzer_object",
                [filePath],{},
                "get_boresight_analyzer_object_handler"
            )
        },
        onLoadMostRecent(){
            // logger.debug(`BoresightCalibration.onLoadMostRecent`)
            this.serverCommand(
                "get_most_recent_boresight_analyzer_object",
                [],{},
                "get_most_recent_boresight_analyzer_object_handler"
            )
        },
        startBoresight(){
            logger.debug("BoresightCalibration.startBoresight")
            // this.$refs["boresight-plot"].clearPlot()
            var initOffsets = [
                this.$refs["boresight-run"].initEL,
                this.$refs["boresight-run"].initXEL
            ]
            logger.debug(`BoresightCalibration.startBoresight: ${JSON.stringify(initOffsets)}`)
            var params = {}
            if (this.sourceForObservation !== null){
                params["src_name_or_dict"] = this.sourceForObservation.name
            }
            logger.debug(`BoresightCalibration.startBoresight: ${JSON.stringify(params)}`)
            var attrs = {} // added by TBHK 2019-06-08
            if (this.$refs["boresight-run"].type === "scanning"){
                var scanningParams = Object.assign(params, {
                    "iterations": this.$refs["boresight-run"].iter,
                    "rate": this.$refs["boresight-run"].rate,
                    "sample_rate": this.$refs["boresight-run"].sampleRate,
                    "settle_time": this.$refs["boresight-run"].settleTime,
                    "limit": this.$refs["boresight-run"].limit,
                    "two_direction": this.$refs["boresight-run"].$refs["two-direction"].showCheck,
                    // added by TBHK on 2019-06-08
                    "attrs": Object.assign(attrs, {
                      "simulation": this.$refs["boresight-run"].$refs["simulate"].showCheck
                    })
                })
                logger.debug("BoresightCalibration.startBoresight: scanningParams")
                logger.debug(scanningParams)
                logger.debug(scanningParams.attrs)
                this.startScanningBoresight(initOffsets, scanningParams)
            }else if (this.$refs["boresight-run"].type === "stepping"){
                var steppingParams = Object.assign(params, {
                    "iterations": this.$refs["boresight-run"].iter,
                    "n_points": this.$refs["boresight-run"].nPoints,
                    "integration_time": this.$refs["boresight-run"].integrationTime,
                    "two_direction": this.$refs["boresight-run"].$refs["two-direction"].showCheck
                })
                logger.debug("BoresightCalibration.startBoresight: steppingParams")
                logger.debug(steppingParams)
                this.startSteppingBoresight(initOffsets, steppingParams)
            }
        },
        startScanningBoresight(initOffsets, options){
            delete options["iterations"]
            logger.debug(`BoresightCalibration.startScanningBoresight:initOffsets: ${JSON.stringify(initOffsets)}`)
            logger.debug(`BoresightCalibration.startScanningBoresight:options: ${JSON.stringify(options)}`)
            this.serverCommand("scanning_boresight",
                               initOffsets, options,
                               "boresight_handler")
        },
        startSteppingBoresight(initOffsets, options){
            delete options["iterations"]
            this.serverCommand("stepping_boresight",
                               initOffsets, options,
                               "boresight_handler")
        },
        stopBoresight(){
            logger.debug("BoresightCalibration.stopBoresight")
        },
        boresightHandler(data){
            // logger.debug(`boresightHandler`)
            var results = data.args[0]
            if ("status" in results){
                var msg = `BoresightCalibration.boresightHandler: ${results.status}`
                logger.debug(msg)
                if (results["status"] === "done"){
                    this.$refs["boresight-run"].runButton.text = "Run"
                    this.analyzerObject = results["analyzer_obj"]
                }
            }
            if ("axis" in results){
                if ("offset" in results){
                  // offsets are in millideg
                  var offset = results.offset.toFixed(2)
                  logger.debug(`boresight_handler: received offset is ${offset}`)
                  if ("tsys" in results){
                    var tsys   = results.tsys.map(x=>x.toFixed(2))
                    var msg    = `boresight: axis: ${results.axis}, offset: ${offset}, tsys: ${tsys}`
                  } else {
                    var msg    = `boresight: axis: ${results.axis}, offset: ${offset}`
                  }
                } else {
                  var msg    = `boresight: axis: ${results.axis}`
                }
                bus.$emit("status:change", msg)
            }
            if ("done" in results){
                if (results.done){
                    bus.$emit("status:change", "boresight: done")
                }
            }
        },
        processBoresightResults(fits, tsysData){
            // logger.debug(`processBoresightResults`)
            var plotData = []
            var calculatedOffsets = {}
            this.axes.forEach((axis)=>{
                if ("corrected_offset" in tsysData[axis]["right"]){
                    var offsets = tsysData[axis]["right"]["corrected_offset"]
                }else{
                    var offsets = tsysData[axis]["right"]["offset"]
                }
                var smoothOffsets = offsets.map(i=>i)
                var tsysChan0 = tsysData[axis]["right"]["tsys"].map((t)=>t[0])
                var fitsAxis = fits[axis]["right"]["popt"]
                calculatedOffsets[axis] = fitsAxis[1]
                var gaussFit = smoothOffsets.map((x)=>util.gaussFunction(x, fitsAxis))
                plotData.push({
                    x:smoothOffsets,
                    y:gaussFit,
                    options:Object.assign(this.linePlotStyles[axis],{type:"line"})
                })
                plotData.push({
                    x:offsets,
                    y:tsysChan0,
                    options:Object.assign(this.scatterPlotStyles[axis],{type:"scatter"})
                })
            })
            return [plotData, calculatedOffsets]
        },
        getBoresightFilePaths(){
            logger.debug(`BoresightCalibration.getBoresightFilePaths`)
            this.serverCommand(
                "get_boresight_file_paths",
                [],{},
                "get_boresight_file_paths_handler",
            )
        },
        getBoresightFilePathsHandler(data){
            //logger.debug(`BoresightCalibration.getBoresightFilePathsHandler`)
            var filePaths = data.args[0]
            logger.debug(`BoresightCalibration.getBoresightFilePathsHandler: ${filePaths}`)
            this.filePaths = filePaths
        },
        getBoresightAnalzerObject(filePath){
            logger.debug("BoresightCalibration.getBoresightAnalzerObject")
            this.serverCommand(
                "get_boresight_analyzer_object",
                [filePath],{},
                "get_boresight_analyzer_object_handler"
            )
        },
        getBoresightAnalzerObjectHandler(data){
            logger.debug(`BoresightCalibration.getBoresightAnalzerObjectHandler`)
            var analyzerObject = data.args[0]
            if (analyzerObject === null){
                analyzerObject = Object.assign({}, this.defaultAnalyzerObject())
                bus.$emit("status:change", "Couldn't load file")
            }
            // logger.debug(`getBoresightAnalzerObjectHandler: ${JSON.stringify(analyzerObject)}`)
            this.analyzerObject = analyzerObject
        },
        getMostRecentBoresightAnalzerObjectHandler(data){
            logger.debug(`BoresightCalibration.getMostRecentBoresightAnalzerObjectHandler`)
            var analyzerObject = data.args[0]
            if (analyzerObject === null){
                analyzerObject = Object.assign({}, this.defaultAnalyzerObject())
                bus.$emit("status:change", "Couldn't load file")
            }
            // logger.debug(`BoresightCalibration.getMostRecentBoresightAnalzerObjectHandler: $`)
            // logger.debug(`getMostRecentBoresightAnalzerObjectHandler: ${JSON.stringify(analyzerObject["data"]["el"]["right"])}`)
            this.analyzerObject = analyzerObject
        },
        getBoresightScoreHandler(data){
            logger.debug(`getBoresightScoreHandler`)
            var score = data.args[0]
        },
        registerSocketHandlers(){
            this.socket.on("boresight_handler", this.boresightHandler)
            this.socket.on("get_boresight_analyzer_object_handler",
                this.getBoresightAnalzerObjectHandler)
            this.socket.on("get_most_recent_boresight_analyzer_object_handler",
                this.getMostRecentBoresightAnalzerObjectHandler)
            this.socket.on("get_boresight_file_paths_handler",
                this.getBoresightFilePathsHandler)
            this.socket.on("get_boresight_score_handler",
                this.getBoresightScoreHandler)
        },
        getInitialData(){
            logger.debug("BoresightCalibration.getInitialData")
            this.getBoresightFilePaths()
        },
        defaultAnalyzerObject(){
            var defaultObj = {
                "meta_data":{},
                "data":{}
            }
            return defaultObj
        }
    },
    computed:{
        header(){
            var headerText = ["Boresight"]
            if (this.sourceForObservation !== null){
                if ("formatted" in this.sourceForObservation){
                    headerText.push(this.sourceForObservation.formatted)
                }
            }
            return headerText.join(" ")
        }
    },
    mounted(){
        this.$refs["main-panel"].show = true
        this.$refs["main-panel"]
            .$refs["start-stop"]
            .$on("start-stop-toggle", this.onBoresightToggle)
    },
    data:function(){
        return {
            types: ["scanning", "stepping"],
            axes: ["el", "xel"],
            srAxes: ["X", "Y", "Z", "XT", "YT"],
            filePaths: {},
            analyzerObject: {"meta_data": {},"data": {}},
            calculatedOffsets:{"el": 0,"xel": 0},
            plotData: [],
            linePlotStyles: {
                "el":{
                    stroke: "#3366cc",
                    "stroke-width": 1.5,
                },
                "xel":{
                    stroke: "#dc3912",
                    "stroke-width": 1.5,
                }
            },
            scatterPlotStyles: {
                "el":{
                    fill: "#3366cc"
                },
                "xel":{
                    fill: "#dc3912"
                }
            },
        }
    }
}

</script>

<style scoped>
.container {
    display: grid;
    grid-template-columns: 0.5fr 0.5fr 1.0fr;
    grid-gap: 0.5rem;
}
</style>
