<template>
  <div>
    <collapsable-panel header="Spectrometer Calibration" ref="panel">
        <div class="container">
            <label>ROACH</label>
            <label>ADC Gain</label>
            <label>RMS</label>
            <label>Setup</label>
        </div>
        <div v-for="(item, idx) in ROACHNames" :key="idx" class="container">
            <label>{{item}}</label>
            <spin-box-with-accept :init-value="10"
                                  @input-spin-box-accept="setADCGain(idx,
                                  $event)"></spin-box-with-accept>
            <label>{{formatRMS(rms[idx])}}</label>
            <drop-down :contents="calibrationActions"
                       @drop-down-click="delegateCalibration(idx, ...arguments)"></drop-down>
        </div>
        <div>
            <label>Rest Frequency</label>
            <drop-down :contents="restFrequencies"
                     @drop-down-click="selectLine($event)"></drop-down>
        </div>
    </collapsable-panel>
  </div>
</template>

<script>
import Vue from "vue"

import util from "./../util.js"

import CollapsablePanel from "./CollapsablePanel.vue"
import TableRow from "./TableRow.vue"
import SpinBoxWithAccept from "./SpinBoxWithAccept.vue"
import DropDown from "./DropDown.vue"
import SocketIOMixin from "./SocketIOMixin.vue"

export default {
    mixins:[SocketIOMixin],
    components:{
        "collapsable-panel":CollapsablePanel,
        "table-row":TableRow,
        "spin-box-with-accept":SpinBoxWithAccept,
        "drop-down":DropDown
    },
    props: {
        ROACHNames: {
            type: Array,
            default: util.range(1,5).map((i)=>`sao64k-${i}`)
        }
    },
    methods:{
        formatRMS: function(rmsVal){
            // format with two decimal places
            return parseFloat(rmsVal).toFixed(2)
        },
        getADCRMSHandler(data){
            // process return from 'get_ADC_rms' command
            //console.log(`getADCRMSHandler: received ${Object.keys(data)}`)
            //console.log(`getADCRMSHandler: args = ${data.args}`)
            console.log(`getADCRMSHandler: args[0] = ${data.args[0]}`)
            var [roachName, rms] = data.args[0]
            //console.log(`getADCRMSHandler: ${roachName}, ${rms}`)
            var index = parseInt(roachName[roachName.length - 1]) - 1
            Vue.set(this.rms, index, rms)
        },
        getADCRMS(roach){
            // send 'get_ADC_rms' command to server
            // done at the end of 'setADCgain'
            var roachName = this.ROACHNames[roach]
            console.log(`SpectrometerCalibration: SpectrometerCalibration.getADCRMS: roach ${roach}, ${roachName}`)
            this.serverCommand(
                "hdwr", ["Backend", "get_ADC_rms", roachName], {},
                "get_ADC_rms_handler"
            )
        },
        setADCGain(roach, val){
            // send 'rf_gain_set' command to server
            var roachName = this.ROACHNames[roach]
            console.log(`SpectrometerCalibration: setADCGain: roach ${roach}, ${roachName}, ${val}`)
            this.serverCommand(
                "hdwr", ["Backend", "rf_gain_set", roachName, 0, 0, val], {},
                "rf_gain_set_handler"
            )
            this.getADCRMS(roach)
        },
        selectLine(value){
            var selection = value
            console.log(`SpectrometerCalibration:selectLine: ${selection}`)
            this.serverCommand("set_rest_freq",[selection],{},"")
        },
        calibrateADC(roach){
            // send 'calibrate' command to server to ROACH to configure ADC
            // not clear if it is needed
            console.log(`SpectrometerCalibration: calibrateADC: ${roach}`)
            this.serverCommand(
                "hdwr", ["Backend", "calibrate", roach], {}, "calibrate_handler"
            )
        },
        initializeADC(roach){
            // send 'initialize' server command to ROACH
            // not needed; done during ROACH hw initialization
            console.log(`SpectrometerCalibration: initializeADC: ${roach}`)
            this.serverCommand(
                "hdwr", ["Backend", "initialize", roach], {}, "initialize_handler"
            )
        },
        setFFTShift(roach){
            // done during ROACH initialization from value in firmware spreadsheet
            // probably not needed
            console.log(`SpectrometerCalibration: setFFTShift: ${roach}`)
            this.serverCommand(
                "hdwr", ["Backend", "fft_shift_set", roach, this.fftVal], {}, "fft_shift_set_handler"
            )
        },
        syncVectorAccumulator(roach){
            // done automatically when the accumulation time is set
            console.log(`SpectrometerCalibration: syncVectorAccumulator: ${roach}`)
            this.serverCommand(
                "hdwr", ["Backend", "sync_start", roach], {}, "sync_start_handler"
            )
        },
        delegateCalibration(roach, value, idx){
            // maps buttons to actions
            console.log(`SpectrometerCalibration: delegateCalibration: ${roach} ${value} ${idx}`)
            var roachName = this.ROACHNames[roach]
            this.calibrationMapping[value](roachName)
        },
        getSpectraData(data){
          var spectra = data.args[0]
          console.log(`SpectrometerCalibration: getSpectraData ${spectra[0]}`)
          this.chartData = spectra
        },
        registerSocketHandlers(){
            this.socket.on("calibrate_handler",     ()=>{console.log("calibrateADCHandler: called")})
            this.socket.on("initialize_handler",    ()=>{console.log("initializeADCHandler: called")})
            this.socket.on("fft_shift_set_handler", ()=>{console.log("setFFTShiftHandler: called")})
            this.socket.on("sync_start_handler",    ()=>{console.log("syncVectorAccumulatorHandler: called")})
            this.socket.on("rf_gain_set_handler",   ()=>{console.log("rfGainSetHandler: called")})
            this.socket.on("get_ADC_rms_handler", this.getADCRMSHandler)
        },
        getInitialData(){
          console.log('SpectrometerCalibration.getInitialData: called')
        }
    },
    mounted:function(){
        this.$refs["panel"].show = true
    },
    data: function(){
        return {
            fftVal: 63,
            rms: this.ROACHNames.map(i=>0),
            calibrationActions: [
                {value: "calibrate", display: "Calibrate ADC"},
                {value: "initialize", display: "Initialize ADC"},
                {value: "set-fft-shift", display: "Set FFT Shift"},
                {value: "sync-vec-accum",  display: "Sync Vector Accumulators"}
            ],
            calibrationMapping: {
                "calibrate": this.calibrateADC,
                "initialize": this.initializeADC,
                "set-fft-shift":this.setFFTShift,
                "sync-vec-accum": this.syncVectorAccumulator
            },
            restFrequencies: [
              {display:"H\u2082O 6\u2081,\u2086-5\u2082,\u2083",
               value:22235.120},
              {display:"NH\u2083 1\u2081-1\u2081",
               value:23694.470},
              {display:"C\u2083H\u2082 1\u2081,\u2080-1\u2080,\u2081",
               value:18343.144},
              {display:"CH\u2083OH 2\u2081,\u2081-3\u2080,\u2083",
               value:19967.396},
              {display:"CCS N,J=1,2-0,1",
               value:22344.030},
              {display:"H 69\u03B1 (19.6)",
               value:19591.121},
              {display:"H 68\u03B1 (20.4)",
               value:20461.776},
              {display:"H 67\u03B1 (21.4)",
               value:21384.795},
              {display:"H 66\u03B1 (22.4)",
               value:22364.177},
              {display:"H 65\u03B1 (23.4)",
               value:23404.290},
              {display:"H 64\u03B1 (24.5)",
               value:24509.915}
            ]
        }
    }
}
</script>

<style scoped>

.container{
    display: grid;
    grid-template-columns: 0.2fr 0.3fr 0.1fr 0.4fr;
    grid-gap: 0.5rem;
}

</style>
