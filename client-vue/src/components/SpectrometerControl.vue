<template>
  <collapsable-panel :header="header">
    <div class="specctrl-container">
      <div class="controls">
         <div class="spinboxes">
            <div class="label-row">
                <label>Scans</label>
                <spin-box ref="cycles-spin-box"
                    :init-value="n_scans"
                    :increment="1"
                    @spin-box-value="n_scans=$event">
                </spin-box>
            </div>
            <div class="label-row">
                <label>Spectra/scan</label>
                <spin-box ref="time-per-scan-spin-box"
                    :init-value="timePerScan"
                    :increment="1"
                    @spin-box-value="timePerScan=$event">
                </spin-box>
            </div>
            <div class="label-row">
                <label>Time/spectrum (s)</label>
                <spin-box ref="integration-time-spin-box"
                    :init-value="integrationTime"
                    :increment="1"
                    @spin-box-value="integrationTime=$event">
                </spin-box>

            </div>
         </div>
         <div class="start-stop">
              <button class="full-row u-full-width start-scanning"
                      @click="onStartClick">Start</button>
              <button
                class="full-row u-full-width stop-scanning"
                @click="onStopClick">
                Stop Scanning
              </button>
         </div>
      </div>
    </div>
    <div>
            <span>Observ. Mode: {{ modePicked }}</span>
            <div class="obs-modes">
              <input type="radio" id="pssw" value="PSSW" v-model="modePicked">
              <label for="pssw">PSSW</label>
              <input type="radio" id="pbsw" value="PBSW" v-model="modePicked">
              <label for="pbsw">PBSW</label>
              <input type="radio" id="bmsw" value="BMSW" v-model="modePicked">
              <label for="bmsw">BMSW</label>
              <input type="radio" id="tlpw" value="TLPW" v-model="modePicked">
              <label for="tplw">TLPW</label>
            </div>
    </div>
    <GChart type="LineChart"
            v-bind:data="chartData"
            v-bind:options="chartOptions"/>
    <div class="last-spectrum">
        <button v-on:click="lastSpectrum">Display last spectrum</button>
        <span>Currently displaying scan {{ lastScan }} record {{ lastRecord }}</span>
    </div>
    <div class="plot-control-container">
        <div class="label-row">
          <label>Average 2<SUP>N</SUP></label>
          <spin-box ref="num-chans-spin-box"
              :init-value="log_n_avg"
              :increment="1"
              @spin-box-value="log_n_avg=$event">
          </spin-box>
        </div>
        <div class="label-row">
           <label>Center</label>
           <spin-box ref="center-chan-spin-box"
              :init-value="mid_chan"
              :increment="1"
              @spin-box-value="mid_chan=$event">
           </spin-box>
        </div>
    </div>
  </collapsable-panel>
</template>

<script>
import * as log from "loglevel"

import SpinBox from "./SpinBox.vue"
import CollapsablePanel from "./CollapsablePanel.vue"
// this is used to interact with the socket
import SocketIOMixin from "./SocketIOMixin.vue"
import GChart from "./../../node_modules/vue-google-charts"

var logger = log.getLogger("SpectrometerControl")

export default {
  mixins:[SocketIOMixin],
  props:{
    socket: {type: Object, default: null}
  },
  components: {
    "spin-box": SpinBox,
    "collapsable-panel": CollapsablePanel
  },
  methods: {
    onStartClick(){
        logger.debug("SpectrometerControl.onStartClick")
        bus.$emit("status:change", "starting spectral scans")
        this.startScans()
    },
    onStopClick(){
        // it takes two clicks within 0.4 s to stop the scans
        this.clicks += 1
        if (this.clicks === 1){
            this.timer = setTimeout(()=>{
                this.clicks = 0
                bus.$emit("status:change", "double click to stop scans")
            }, this.delay)
        }else{
            clearTimeout(this.timer)
            this.clicks = 0
            bus.$emit("status:change", "stopping scans")
            this.$emit("scanning", false)
        }
    },
    saveFits() {
      // request the last set of spectra recorded
      console.log(`SpectrometerControl: saveFits called`)
      // handled by 'saveFitsHandler'
      this.serverCommand("save_FITS", [], {}, "save_fits_handler")
      console.log(`SpectrometerControl:saveFits: save_FITS() called`)
    },
    saveFitsHandler(data){
      // handles the response from 'save_fits_handler' event
      logger.debug("SpectrometerControl.saveFitsHandler called")
      var results = data.args[0]
      console.log(`SpectrometerControl.saveFitsHandler received ${Object.keys(results)}`)
      this.fileName = results["status"]
      console.log(`SpectrometerControl.saveFitsHandler: saved to ${this.fileName}`)
    },
    lastSpectrum(){
      // for server method 'last_scan'
      console.log(`SpectrometerControl: lastSpectrum called`)
      // handled by 'saveFitsHandler
      this.serverCommand("last_scan", [], {}, "last_spectrum_handler")
    },
    lastSpectrumHandler(data){
      // handles the response from '' event
      var time = new Date().toISOString()
      logger.debug(`SpectrometerControl.lastSpectrumHandler called at ${time}`)
      var results = data.args[0]
      if ("scan" in results){
        this.lastScan = results["scan"]
        console.log(`SpectrometerControl.lastSpectrumHandler: scan ${this.lastScan}`)
      }
      if ("record" in results){
        this.lastRecord = results["record"]
        console.log(`SpectrometerControl.lastSpectrumHandler: record ${this.lastRecord}`)
      }
      if ("table" in results){
        this.chartData = results["table"]
        console.log(`SpectrometerControl.scansHandler: chartData: ${this.chartData}`)
      }
      bus.$emit("status:change", `fetched scan ${this.lastScan} record ${this.lastRecord}`)
      console.log(`SpectrometerControl.lastSpectrumHandler: ${JSON.stringify(results)}`)
    },
    startScans(){
        // this starts the spectrometers; spectra are handled
        // by 'scansHandler'
        var time = new Date().toISOString()
        logger.debug(`SpectrometerControl.startScans at ${time}`)
        this.$emit("scanning", true)
        var options = {
            n_scans:   this.n_scans,
            n_spectra: this.timePerScan,
            int_time:  this.integrationTime,
            log_n_avg: this.log_n_avg,
            mid_chan:  this.mid_chan
        }
        this.serverCommand(
            // this is handled by 'scansHandler'
            "start_spec_scans", [], options, "spec_scan_handler"
        )
    },
    scansHandler(data){
        // this handles the response from 'start_spec_scan'
        var time = new Date().toISOString()
        logger.debug(`SpectrometerControl.scansHandler called at ${time}`)
        var results = data.args[0]
        console.log(`SpectrometerControl.scansHandler: ${JSON.stringify(results)}`)
        if ("left" in results){
            // report scans left on status line
            logger.debug("SpectrometerControl.scansHandler: processing 'left'")
            bus.$emit("status:change",
                      `${results.left} scans left`)
        }
        if (results.done){
          logger.debug("SpectrometerControl.scansHandler: processing 'done'")
          bus.$emit("status:change", "scanning finished")
          this.$emit("scanning", false)
        }
        if ("scan" in results){
          logger.debug("SpectrometerControl.scansHandler: processing 'scan'")
          this.lastScan = results["scan"]
        }
        if ("record" in results){
          logger.debug("SpectrometerControl.scansHandler: processing 'record'")
          this.lastRecord = results["record"]
        }
        if ("table" in results){
          logger.debug("SpectrometerControl.scansHandler: processing 'table'")
          this.chartData = results["table"]
          // console.log(`SpectrometerControl.scansHandler: chartData: ${this.chartData}`)
          bus.$emit("status:change", "received spectra table")
        }
        logger.debug(`SpectrometerControl.scansHandler: processed ${results}`)
    },
    registerSocketHandlers(){
        // handles the result of 'start_spec_scans'
        this.socket.on("spec_scan_handler", this.scansHandler),
        // handles the result of 'save_FITS'
        this.socket.on("save_fits_handler",  this.saveFitsHandler),
        this.socket.on("last_spectrum_handler", this.lastSpectrumHandler)
    },
    getInitialData(){
      // this is here only because SpectrometerCalibraton has it
      // I don't know why it is here
      console.log('SpectrometerControl.getInitialData: called')
    }
  },
  computed:{
      header(){
          // headerText is a list of text items to be joined as one string
          var headerText = ["Spectrometer Control"]
          return headerText.join(" ")
      }
  },
  watch:{
    modePicked: function(){
      console.log(`SpectrometerControl: mode is now ${this.modePicked}`)
      this.serverCommand("set_obsmode",[this.modePicked],{},"")
    }
  },
  data(){
      return {
          n_scans: 1,
          timePerScan: 5,
          log_n_avg: 4,
          mid_chan: 512,
          integrationTime: 1.0,
          delay: 400,
          timer: null,
          clicks: 0,
          chartData:[['Frequency', 'sao64k-1', 'sao64k-2','sao64k-3','sao64k-4'],
                     [          0,          1,          2,         3,         4],
                     [        200,          1,          2,         3,         4],
                     [        450,          1,          2,         3,         4],
                     [        500,          6,          7,         8,         9],
                     [        550,          1,          2,         3,         4],
                     [        800,          1,          2,         3,         4],
                     [       1000,          1,          2,         3,         4]
          ],
          chartOptions: {
                  title: 'IF Passband',
                  subtitle: '(smoothed)',
                  explorer: { axis: 'vertical',
                              actions: ['dragToZoom', 'rightClickToReset']},
                  titlePosition: 'in',
                  width: 600,
                  height: 400,
                  vAxis: {
                    //logScale: true,
                    scaleType: 'log',
                    viewWindow: {
                      min: 5,
                      max: 8
                    }
                  },
                  hAxis: {
                    viewWindow: {
                      min: 10,
                      max: 1010
                    }
                  }
          },
          value: 0,
          modePicked: 'PBSW',
          lastScan: 0,
          lastRecord: 0,
          fileName: 'none'
      }
  }
}
</script>

<style scoped>
.specctrl-container {
    display: grid;
    grid-template-columns: 1fr;
    grid-gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.label-row {
    display: grid;
    grid-template-columns: 1fr 2fr;
    grid-column-gap: 0.5rem;
}

.controls {
  display: grid;
  grid-template-columns: 3fr 1fr;
  grid-column-gap: 0.5rem;
}

.obs-modes {
  display: grid;
  grid-template-columns: 4fr 1fr 3fr 1fr 3fr 1fr 3fr 1fr 3fr;
  grid-column-gap: 0.5rem;
}

.plot-control-container {
   display: grid;
   grid-template-columns: 1fr 1fr;
   grid-column-gap: 0.5rem;
}

.last-spectrum {
  display: grid;
  grid-template-columns: 1fr 2fr;
  grid-column-gap: 0.5rem;
}
.full-row {
    display: grid;
    grid-template-columns: 1fr;
    grid-gap: 0.5rem;
}

.start-scanning {}
.start-scanning:hover {
    /* color: inherit; */
    border-color: var(--green);
}

</style>
