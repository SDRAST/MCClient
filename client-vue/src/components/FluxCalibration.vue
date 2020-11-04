<template>
    <collapsable-panel header="T<sub>sys</sub> Calibration"
                       ref="panel" :startStop="true">
    <!-- <panel :header="formatDataDir()" size="medium" :noPad="true" :noBorder="true"></panel> -->
    <label v-show="status !== ''">{{status}}</label>
    <div class="tsys-calibration-container">
        <div ref="tsys-calibration-plot-container">
            <d3-static-plot ref="tsys-calibration-plot"
                            :plotData="plotData"
                            :width="computedWidth"
                            :height="computedHeight"
                            :key="computedRender"></d3-static-plot>
        </div>
    </div>
    </collapsable-panel>
</template>

<script>
import D3StaticPlot from "./D3StaticPlot.js"
import CollapsablePanel from "./CollapsablePanel.vue"
import Panel from "./Panel.vue"
import SocketIOMixin from "./SocketIOMixin.vue"

import testTsysCalibrationData from "./../../test/testTsysCalibrationData.js"

export default {
    mixins:[SocketIOMixin],
    components:{
        "collapsable-panel":CollapsablePanel,
        "panel":Panel,
        "d3-static-plot":D3StaticPlot
    },
    props:{
        info: {type:Object, default:()=>{return null}}
    },
    methods:{
        testPlot: function(){
            this.tsysCalibrationHandler(testTsysCalibrationData)
        },
        formatDataDir: function(){
            if (this.info !== null){
                if ("data_dir" in this.info){
                    return `Data Directory: <code>${this.info.data_dir}</code>`
                }
            }else{
                return ""
            }
        },
        startTsysCalibration: function(){
            console.log("TsysCalibration.startTsysCalibration called")
            this.serverCommand("tsys_calibration",[],{},"tsys_calibration_handler")
        },
        stopTsysCalibration: function(){
            console.log("TsysCalibration.stopTsysCalibration")
        },
        reRenderTsysCalibrationPlot: function(width, height){
            this.computedWidth = width
            this.computedHeight = height
            if (this.computedRender == 0){
                this.computedRender = 1
            }else{
                this.computedRender = 0
            }
        },
        onResize: function(){
            var renderedWidth = this.$refs["tsys-calibration-plot-container"].offsetWidth
            this.reRenderTsysCalibrationPlot(renderedWidth, renderedWidth)
        },
        onToggleTsysCalibration: function(value){
            if (value){
                this.startTsysCalibration()
            }else{
                this.stopTsysCalibration()
            }
        },
        tsysCalibrationHandler: function(data){
            console.log("TsysCalibration.tsysCalibrationHandler called")
            var response = data.args[0]
            this.status = response.status
            bus.$emit("status:change", `tsys calibration: ${response.status}`)
            if ("results" in response){
                // in the component referred to as "panel", invoke the component
                // referred to as "start-stop" method toggleDisplay
                this.$refs["panel"].$refs["start-stop"].toggleDisplay()
                var [plotData, tsysFactors] = this.processTsysCalibrationResults(response.results)
            }
        },
        processTsysCalibrationResults: function(results){
            return [[{x:[], y:[], options:{}}],[results["tsys_factors"]]]
        },
        registerSocketHandlers: function(){
            this.socket.on("tsys_calibration_handler", this.tsysCalibrationHandler)
        }
    },
    mounted: function(){
        this.onResize()
        this.$refs["panel"].show = false
        this.$refs["panel"].$refs["start-stop"].$on("start-stop-toggle", this.onToggleTsysCalibration)
        window.addEventListener('resize', this.onResize)
        this.registerSocketHandlers()
    },
    data:function(){
        return {
            computedWidth:100,
            computedHeight:100,
            computedRender:0,
            plotData: [],
            status:"",
            "testTsysCalibrationData": testTsysCalibrationData
        }
    }
}

</script>

<style scoped>
.tsys-calibration-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 0.5rem;
}

</style>
