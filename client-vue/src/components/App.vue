<template>
  <div class="main">
    <status-bar
        :status="status"
        :sourceForObservation="sourceForObservation">
    </status-bar>
    <h4>DSS<code>{{station}}</code> Monitor and Control</h4>
    <div class="app-container">
        <source-monitor
            class="source-monitor"
            ref="source-monitor"
            :socket="socket"
            @time-change="onSourceMonitorTimeChange"
            @select-source-for-observation="onSelectSourceForObservation"
            :sources="sources"
            :sourcesObject="sourcesObject"
            :sourceForObservation="sourceForObservation"
            :styles="sourcePlot.styles"
            :sourceNames="sourceNames"
            :width="sourcePlot.width"
            :height="sourcePlot.height"
            :render="sourcePlot.render">
        </source-monitor>
        <div class="power-meter-monitor">
            <!-- added 'info' for flux-calibration -->
            <power-meter-monitor
                ref="power-meter-monitor"
                :socket="socket"
                :info="serverInfo.flux_calibration">
            </power-meter-monitor>
        </div>
        <div class="antenna-monitor">
            <antenna-monitor
                ref="antenna-monitor"
                :socket="socket">
            </antenna-monitor>
        </div>
        <antenna-control
            class="antenna-control"
            :socket="socket"
            :sourceForObservation="sourceForObservation">
        </antenna-control>
        <boresight-calibration
            class="boresight-calibration"
            :info="serverInfo.boresight"
            :socket="socket"
            :sourceForObservation="sourceForObservation">
        </boresight-calibration>
        <div class="flux-calibration">
            <!-- flux-calibration
                :info="serverInfo.flux_calibration"
                :socket="socket">
            </flux-calibration -->
            <spectrometer-control
                :socket="socket">
            </spectrometer-control>
        </div>
        <div class="spectrometer-calibration">
            <spectrometer-calibration
                :socket="socket"
                :ROACHNames="ROACHNames">
            </spectrometer-calibration>
        </div>
        <div class="nodding">
            <nodding
                :socket="socket"
                :sourceForObservation="sourceForObservation"
                @nodding="onNodding">
            </nodding>
        </div>
        <!-- <input type="text" v-model="socketPortModel" @keyup.enter="onSocketPortChange(socketPortModel)">
        <button @click="onSocketPortChange(socketPortModel)">Connect</button> -->
    </div>
    <p>
        version: {{version}}
    </p>
  </div>
</template>



<script>
import io from "socket.io-client"
import Vue from "vue"
import * as log from "loglevel"

import PausableTimer from "./../pausable_timer.js"

import SourceMonitor from "./SourceMonitor.vue"
import PowerMeterMonitor from "./PowerMeterMonitor.vue"
import AntennaMonitor from "./AntennaMonitor.vue"
import AntennaControl from "./AntennaControl.vue"
import FluxCalibration from "./FluxCalibration.vue"
import BoresightCalibration from "./BoresightCalibration/BoresightCalibration.vue"
import SpectrometerCalibration from "./SpectrometerCalibration.vue"
import SpectrometerControl from "./SpectrometerControl.vue"
import Nodding from "./Nodding.vue"
import Panel from "./Panel.vue"
import StatusBar from "./StatusBar.vue"
import SocketIOMixin from "./SocketIOMixin.vue"

var logger = log.getLogger("App")

export default {
    props:{
        domain: {type: String, default:"localhost"},
        port: {type:Number, default:5000},
        version: {type: String, default: ""}
    },
    components:{
        "source-monitor":SourceMonitor,
        "power-meter-monitor":PowerMeterMonitor,
        "antenna-monitor": AntennaMonitor,
        "antenna-control": AntennaControl,
        "boresight-calibration":BoresightCalibration,
        "flux-calibration":FluxCalibration,
        "spectrometer-calibration":SpectrometerCalibration,
        "spectrometer-control":SpectrometerControl,
        "nodding":Nodding,
        "status-bar": StatusBar,
        "panel":Panel
    },
    created(){
        var time = new Date().toISOString()
        logger.debug(`App: created at ${time}`)
        this.initSocket()
    },
    mounted(){
        var time = new Date().toISOString()
        logger.debug(`App: mounted at ${time}`)
        bus.$on("antenna-monitor:monitor-data", this.setAntennaMonitorData)
        bus.$on("status:change", this.setStatus)
    },
    methods:{
        serverCommand: SocketIOMixin.methods.serverCommand,
        getPort: SocketIOMixin.methods.getPort,
        checkIfRegistered: SocketIOMixin.methods.checkIfRegistered,
        registerPort: function(socketOrPort){
            var time = new Date().toISOString()
            logger.debug(`App: registering socket ${socketOrPort} at ${time}`)
            var port = this.getPort(socketOrPort)
            this.socketPort = port
            this.registeredPorts[port] = true
        },
        onSelectSourceForObservation(source){
            logger.debug(`selectSourceForObservation: ${source.name}`)
            this.sourceForObservation = source
        },
        setAntennaMonitorData(antennaMonitorData){
            //logger.debug(`App.setAntennaMonitorData: ${JSON.stringify(antennaMonitorData)}`)
            var circleData = {
                "az":parseFloat(antennaMonitorData["AzimuthAngle"], 10),
                "el":parseFloat(antennaMonitorData["ElevationAngle"], 10),
                "ra":0.0,
                "dec":0.0,
                "info":{
                    "name":"Antenna",
                    "category":["antenna"]
                },
                "category":"antenna"
            }
            Vue.set(this.sourcesObject, "Antenna", circleData)
            var names = this.sources.map((obj)=>{obj.name})
            var idxAntenna = names.indexOf("Antenna")
            this.sources.splice(idxAntenna, 1)
            this.sources.push(circleData)
        },
        setStatus: function(newStatus){
            this.status = newStatus
        },
        formatSourceForObservation: function(sourceObject){
            if (sourceObject === null){
                return
            }
            var name = sourceObject.name
            var category = sourceObject.category
            return `<span style="color:${this.sourcePlot.styles[category].fill};">${sourceObject.name}</span>`
        },
        initSocket: function(){
            var time = new Date().toISOString()
            logger.debug(`App.initSocket called at ${time}`)
            if (this.socket === null || ! this.checkIfRegistered(this.socket)){
                this.socket = io.connect(`http://${this.socketDomain}:${this.socketPort}`)
                this.registerPort(this.socket)
                this.registerSocketHandlers()
                logger.debug(`App.initSocket: ${this.socket} registered`)
            }
            this.socket.on("connect", ()=>{
                var time = new Date().toISOString()
                logger.debug(`App.initSocket: connected at ${time}`)
                this.socket.emit("hostname")
                bus.$emit(
                    "status:change",
                    `connected to server on port ${this.socketPort}`
                )
            })
        },
        sourcesObjectToSourceList:function(sourcesObject){
            logger.debug("App.sourcesObjectToSourceList: called")
            var categoryLookup = (category)=>{
                var mapping = {
                    "known maser": "known-masers",
                    "catalog":"catalog-sources",
                    "antenna":"antenna",
                    "calibrator": "calibrators",
                    "priority 1":"priority-1",
                    "priority 2":"priority-2",
                    "priority 3":"priority-3",
                    "priority 4":"priority-4",
                }
                var categoryStr = []
                if (! Array.isArray(category)){
                    category = [category]
                }
                category.forEach((subCategory)=>{
                    categoryStr.push(mapping[subCategory])
                })
                return categoryStr.join("-")
            }

            var convert = 180. / Math.PI
            var data = []
            Object.keys(sourcesObject).forEach((srcName)=>{
                var src = sourcesObject[srcName]
                src.name = srcName
                if (src.name !== "Antenna"){
                    src.az = src.az * convert
                    src.el = src.el * convert
                }
                src.category = categoryLookup(src.info.category)
                data.push(src)
            })
            return data
        },
        setInfoHandler(data){
            logger.debug("App.setInfoHandler: called")
        },
        getSources(time){
            logger.debug(`App.getSources: ${time}`)
            this.serverCommand(
                "get_sources",
                [this.sourceNames],
                {
                    when:time,
                    formatter:"%Y-%m-%dT%H:%M:%S.%fZ"
                },
                "get_sources_handler"
            )
        },
        loadSourcesHandler(data){
            logger.debug("App.loadSourcesHandler: called")
            var verifiers = data.args[0]["verifiers"]
            var sources = Object.assign(verifiers, data.args[0]["sources"])
            this.sourceNames = Object.keys(sources)
            var changeTime = ()=>{
                if (this.sourceMonitorTime === null){
                    var time = new Date().toISOString()
                    this.getSources(time)
                }
            }
            this.timer = new PausableTimer(changeTime, this.sourceUpdateTime)
            this.timer.start()
        },
        getSourcesHandler(data){
            logger.debug("App.getSourcesHandler: called")
            var sources = data.args[0]
            this.sourcesObject = sources
            this.sources = this.sourcesObjectToSourceList(sources)
        },
        getInfoHandler(data){
            logger.debug(`App.getInfoHandler: called`)
            var info = data.args[0]
            this.serverInfo = info
        },
        roachNameHandler(data){
            logger.debug(`App.roachNameHandler: called`)
            var ROACHNames = data.args[0]
            logger.debug(`App.roachNameHandler: got ${ROACHNames}`)
            this.ROACHNames = ROACHNames
        },
        hostNameHandler(data){
          logger.debug(`App.hostNameHandler: data: ${data}`)
            // var hostName = data
            // logger.debug(`App.hostNameHandler: hostName: ${hostName}`)
            // bus.$emit("status:change", `Remote host name: ${hostName}`)
            // var sourceDir = this.hostNameConfig[hostName]
            if(this.hostName === ""){
              this.hostName = data
              logger.debug(`App.hostNameHandler: hostName: ${this.hostName}`)
              bus.$emit("status:change", `Remote host name: ${this.hostName}`)
              var sourceDir = this.hostNameConfig[this.hostName]
              this.serverCommand(
                  "set_info",[["project","source_dir"],sourceDir],{},"set_info_handler")
              this.serverCommand(
                  "load_sources",[],{},"load_sources_handler")
              this.serverCommand(
                  "get_info",[],{},"get_info_handler")
              this.serverCommand(
                  "hdwr", ["Backend", "roachnames"], {}, "roachnames_handler")
            } else {
              // the case of a changed source is not yet handled
              return
            }
        },
        registerSocketHandlers(){
            logger.debug(`App.registerSocketHandlers`)
            this.socket.on("hostname",this.hostNameHandler)
            this.socket.on("set_info_handler", this.setInfoHandler)
            this.socket.on("load_sources_handler", this.loadSourcesHandler)
            this.socket.on("get_sources_handler", this.getSourcesHandler)
            this.socket.on('get_info_handler', this.getInfoHandler)
            this.socket.on("roachnames_handler", this.roachNameHandler)
        },
        onSocketPortChange(newPort){
            this.socketPortModel = parseInt(newPort)
            this.socketPort = this.socketPortModel
            this.initSocket()
        },
        onSourceMonitorTimeChange(newTime){
            this.sourceMonitorTime = newTime
        },
        onNodding(flag){
            if (flag){
                this.$refs["power-meter-monitor"].pauseTimers()
                this.$refs["antenna-monitor"].pauseTimers()
            }else{
                this.$refs["power-meter-monitor"].unPauseTimers()
                this.$refs["antenna-monitor"].unPauseTimers()
            }
        }
    },
    watch: {
        port: function(){
            this.socketPort = this.port
            this.initSocket()
        },
        domain: function(){
            this.socketDomain = this.domain
            this.initSocket()
        },
        sourceMonitorTime: function(){
            var date = this.sourceMonitorTime
            if (this.sourceMonitorTime === null){
                date = new Date()
            }
            this.getSources(date.toISOString())
        },
        sourceForObservation(){
            this.sourceForObservation.formatted = this.formatSourceForObservation(this.sourceForObservation)
        }
    },
    data: function(){
        var port = this.port
        return {
            hostName: "",
            station: 43,
            status: "hello!",
            sources: [],
            sourcesObject: {},
            sourceNames: [],
            sourcePlot:{
                styles: {
                    "calibrators":{
                        class:"scatter calibrators",
                        fill:"#B10DC9",
                        opacity:0.8,
                        r:(d)=>{
                            var flux = parseFloat(d.info.flux.K)
                            if (flux === undefined || isNaN(flux)){
                                flux = 0.0
                            }
                            flux += 3.0
                            return flux
                        },
                        display:"Calibrators"
                    },
                    "known-masers":{
                        class:"scatter known-masers",
                        fill:"#FF851B",
                        opacity:0.8,
                        r:8,
                        display:"Known Masers"
                    },
                    "catalog-sources-priority-1":{
                        class:"scatter catalog-sources priority-1",
                        fill:"#001f3f",
                        opacity:0.8,
                        r:8,
                        display:"Priority 1"
                    },
                    "catalog-sources-priority-2":{
                        class:"scatter catalog-sources priority-2",
                        fill:"#0074D9",
                        opacity:0.8,
                        r:8,
                        display:"Priority 2"
                    },
                    "catalog-sources-priority-3":{
                        class:"scatter catalog-sources-priority-3",
                        fill:"#7FDBFF",
                        opacity:0.8,
                        r:8,
                        display:"Priority 3"
                    },
                    "catalog-sources-priority-4":{
                        class:"scatter catalog-sources-priority-4",
                        fill:"#39CCCC",
                        opacity:0.8,
                        r:8,
                        display:"Priority 4"
                    },
                    "antenna":{
                        class:"scatter antenna",
                        fill:"#FF4136",
                        opacity:0.8,
                        r:12,
                        display:"Antenna"
                    },
                    __order__:[
                                "calibrators",
                                "known-masers",
                                "catalog-sources-priority-1",
                                "catalog-sources-priority-2",
                                "catalog-sources-priority-3",
                                "catalog-sources-priority-4",
                                "antenna"
                    ]
                },
                filters:{
                    el: (val)=>{
                        if (val < 0){
                            return false
                        } else {
                            return true
                        }
                    },
                    az: (val)=>true,
                    flux: (val)=>true
                },
                width: 300,
                height: 300,
                render: 0
            },
            sourceUpdateTime:4*60*1000,
            sourceForObservation:null,
            serverInfo:{
                boresight:{},
                flux_calibration:{},
            },
            socketPort: port,
            socketPortModel: port,
            socketDomain: this.domain,
            registeredPorts: {port: false},
            socket: null,
            hostNameConfig:{
                "dean-ThinkPad-T460": "/home/dean/jpl-dsn/projects_TAMS",
                "enceladus":          "/home/dean/work/tams/project_TAMS",
                "crux1":              "/home/ops/projects/TAMS",
                "crux":               "/home/ops/projects/TAMS",
                "kuiper":             "/usr/local/projects/TAMS",
                "nutmeg2":            "/usr/local/projects/TAMS"
            },
            ROACHNames: [],
            sourceMonitorTime: null
        }
    }
}
</script>

<style scoped>
/* Grid Styling */
.app-container {
    display: grid;
    grid-template-rows: 0.5fr repeat(calc(var(--rows)-1), minmax(0.5fr, 1fr));
    grid-template-columns: repeat(var(--columns), 1fr);
    grid-gap: 0.5rem 0.5rem;
}

.source-monitor {
    grid-column: 1 / calc(1 + var(--columns));
    grid-row: 1 / 1;
}

/* .source-for-observation{
    grid-column: 1 / calc(1 + var(--columns));
    grid-row: 2 / 2;
} */

.power-meter-monitor{
    grid-column: 1 / 3;
    grid-row: 2 / 2;
}

.antenna-monitor{
    grid-column: 3 / 4;
    grid-row: 2 / 2;
}

.antenna-control{
    grid-column: 4 / calc(1 + var(--columns));
    grid-row: 2 / 2;
}

.boresight-calibration{
    grid-column: 1 / calc(1 + var(--columns));
    grid-row: 3 / 3;
}

.flux-calibration{
    grid-column: 1 / 2;
    grid-row: 4 / 4;
}

.spectrometer-calibration{
    grid-column: 2 / calc(var(--columns));
    grid-row: 4 / 4;
}

.nodding {
    grid-column: 4 / 5;
    grid-row: 4 / 4;
}

</style>

<style>
.scrollable-parent {
    overflow: hidden;
}

.scrollable-child {
    max-height: 350px;
    overflow-y: scroll;
}
</style>
