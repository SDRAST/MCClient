<template>
  <collapsable-panel header="Power Meter Monitor">
    <GChart type="LineChart"
            v-bind:data="chartData"
            v-bind:options="chartOptions"/>
    <flux-calibration
        :info="info"
        :socket="socket">
    </flux-calibration>
  </collapsable-panel>
</template>

<script>
import Panel from "./Panel.vue"
import CollapsablePanel from "./CollapsablePanel.vue"
import SocketIOMixin from "./SocketIOMixin.vue"
import FluxCalibration from "./FluxCalibration.vue"
import GChart from "./../../node_modules/vue-google-charts"

import PausableTimer from "../pausable_timer.js"
import util from "./../util.js"

export default{
    mixins:[SocketIOMixin],
    components:{
        "collapsable-panel":CollapsablePanel,
        "flux-calibration":FluxCalibration,
        "panel":Panel
    },
    props:{
      socket: {type: Object, default: null},
      info:   {type: Object, default: null} // added for flux-calibration
    },
    methods:{
        registerSocketHandlers:function(){
            this.socket.on("get_tsys",this.getTsysHandler)
        },
        startTimers: function(){
            var retrieveSimulatedTsysData = (interval)=>{
                var timer = new PausableTimer(()=>{
                    this.tsysData = util.range(0,4).map(i=>10*Math.random())
                },interval)
                timer.start()
                return timer
            }
            var retrieveTsysData = (interval)=>{
                var timer = new PausableTimer(()=>{
                    this.serverCommand("get_tsys",[],{},"")
                }, interval)
                timer.start()
                return timer
            }
            if (this.simulated){
                this.timer = retrieveSimulatedTsysData(this.updateInterval)
            }else{
                this.timer = retrieveTsysData(this.updateInterval)
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
        getTsysHandler: function(data){
            //if (this.chartData === null){
            //    this.initDataTable()
            //}
            var tsys = data.result
            console.log(`getTsysHandler: got ${tsys}`)
            // returns a list of four floats:
            // 70.2952915317727,73.00064425605628,75.43110572416593,73.4556876456517
            if (tsys === null){ return }
            // this creates a new array 'tsysData' from 'tsys' with no
            // operation on each element
            this.tsysData = tsys.map(t=>t)
            var tsysrow = new Array(new Date())
            var i
            for (i = 0; i < this.tsysData.length; i++) {
              tsysrow.push(this.tsysData[i])
            }
            console.log(`getTsysHandler: new row: ${tsysrow}`)
            this.chartData.push(tsysrow)
            //console.log(`getTsysHandler: chartData: ${this.chartData}`)
            if (this.chartData.length > this.maxPlotElements){
              this.chartData.splice(1,1)
            }
        },
        initDataTable(){
            console.log("initDataTable: entered")
            var title = ["Time"]
            console.log(`initDataTable: title row is now ${title}`)
            for (let i = 1; i < 5; i++){
              title.push('PM'.concat((i).toString()))
            }
            console.log(`initDataTable: title row is now ${title}`)
            console.log(`initDataTable: setting title row to ${[title]}`)
            this.chartData = [title]
            console.log(`initDataTable: chart data is now ${this.chartData}`)
            console.log(`initDataTable: chartData is ${this.chartData}`)
        }
    },
    //mounted: function(){
    //    this.initDataTable()
    //},
    data: function(){
        return {
            maxPlotElements: 200,
            colors: [{fill:"#3366cc"}, {fill:"#dc3912"}, {fill:"#ff9900"}, {fill:"#109618"}],
            tsysData: util.range(0,4).map(i=>Math.random()),
            chartData: [['Time', 'PM1', 'PM2', 'PM3', 'PM4']],
            chartOptions: {
              title: 'System Temperature',
              subtitle: '(if calibrated)',
              titlePosition: 'in',
              width: 800,
              height: 400
            },
            // this should probably be set in App and passed as an attribute value
            updateInterval: 10000, // how often to update the power meter data
            timer: null,
        }
    }
}
</script>

<style scoped>
.container {
    display: grid;
    grid-template-columns: 7fr 4fr;
    grid-gap: 0.5rem;
}
</style>
