<template>
    <collapsable-panel header="Antenna Monitor">
        <div class="container">
            <label>Azimuth </label>
            <div class="right-justify-content">
                <code>{{AzimuthAngle}}</code>
            </div>
            <label>Elevation</label>
            <div class="right-justify-content">
                <code>{{ElevationAngle}}</code>
            </div>
            <label>Predicted Azimuth</label>
            <div class="right-justify-content">
                <code>{{AzimuthPredictedAngle}}</code>
            </div>
            <label>Predicted Elevation</label>
            <div class="right-justify-content">
                <code>{{ElevationPredictedAngle}}</code>
            </div>
            <hr class="full-row"/>
            <label>EL Pos. Offset</label>
            <div class="right-justify-content">
                <code>{{ElevationPositionOffset}}</code>
            </div>
            <label>XEL Pos. Offset</label>
            <div class="right-justify-content">
                <code>{{CrossElevationPositionOffset}}</code>
            </div>
            <label>EL Rate</label>
            <div class="right-justify-content">
                <code>{{ElevationAccumulatedRateOffset}}</code>
            </div>
            <label>XEL Rate</label>
            <div class="right-justify-content">
                <code>{{CrossElevationAccumulatedRateOffset}}</code>
            </div>
        </div>
    </collapsable-panel>
</template>


<script>
import TableRow from "./TableRow.vue"
import CollapsablePanel from "./CollapsablePanel.vue"
import SocketIOMixin from "./SocketIOMixin.vue"

import PausableTimer from "./../pausable_timer.js"

export default {
    mixins:[SocketIOMixin],
    components: {
        "collapsable-panel": CollapsablePanel,
        "table-row":TableRow
    },
    methods:{
        toCode: function(elem){
            return `<code>${elem}</code>`
        },
        registerSocketHandlers: function(){
            this.socket.on("hdwr_handler",this.hdwrHandler)
        },
        hdwrHandler: function(data){
            var monitorData = data.args[0]
            // monitorData might be null if getting results from a simulated APC
            if (monitorData === null){
                return
            }
            bus.$emit("antenna-monitor:monitor-data", monitorData)
            Object.keys(monitorData).forEach((monitorItem)=>{
                this[monitorItem] = monitorData[monitorItem]
            })
        },
        startTimers: function(){
            var updateTime = 10000 // was 5000
            var retrieveAntennaData = (interval)=>{
                var timer = new PausableTimer(()=>{
                    this.serverCommand("hdwr",[
                        "Antenna","get","AzimuthAngle",
                        "ElevationAngle","AzimuthPredictedAngle",
                        "ElevationPredictedAngle","ElevationPositionOffset",
                        "CrossElevationPositionOffset","ElevationAccumulatedRateOffset",
                        "CrossElevationAccumulatedRateOffset"],{},"hdwr_handler")
                },interval)
                timer.start()
                return timer
            }
            var retrieveSimulatedAntennaData = (interval)=>{
                var timer = new PausableTimer(()=>{},interval)
                timer.start()
                return timer
            }
            if (this.simulated){
                this.timer = retrieveSimulatedAntennaData(updateTime)
            }else{
                this.timer = retrieveAntennaData(updateTime)
            }
        },
        pauseTimers(){
            if (this.timer !== null){
                this.timer.pause()
            }
        },
        unPauseTimers(){
            if (this.timer !== null){
                this.timer.unpause()
            }
        },
    },
    mounted:function(){
    },
    data: function(){
        return {
            AzimuthAngle: 0.0,
            ElevationAngle: 0.0,
            AzimuthPredictedAngle: 0.0,
            ElevationPredictedAngle: 0.0,
            ElevationPositionOffset: 0.0,
            CrossElevationPositionOffset: 0.0,
            ElevationAccumulatedRateOffset: 0.0,
            CrossElevationAccumulatedRateOffset: 0.0,
            timer: null
        }
    }
}
</script>


<style scoped>
.align-right{
    text-align:right;
}

.container {
    display: grid;
    grid-template-columns: 1fr 0.3fr;
    grid-template-rows: repeat(8, 0.5fr);
}

.full-row {
    grid-column: 1 / 3;
}

.right-justify-content {
    text-align: right;
}

</style>
