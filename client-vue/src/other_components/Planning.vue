<!-- Page for planning observations

When the page has been compiled, the 'created(){...}' section of the script is
called.  It calls 'initSocket()' expecting the socket exists already. It emits
'hostname' on the socket but the response will be handled by App.

There is a 'watch' defined for these variables:
  "port":                  calls 'initSocket()'
  "domain":                calls 'initSocket()'

The SourceMonitor object 'source_monitor' can trigger two events that trigger
calls to these respective functions:
  time-change:                   onSourceMonitorTimeChange(time), which sets
                                 'sourceMonitorTime' to the new time
  select-source-for-observation: onSelectSourceForObservation(), which changes
                                 'sourceForObservation'
Both trigger 'watch' functions.
 -->
<template>
    <div class="main">
      <center>
        <B>DSS<code>{{station}}</code> Session Planning</B>
      </center>
      <div class="app-container">
        <!-- bind variable 'sourcePlot' attribute 'styles' to property 'styles';
            variable 'sourcePlot' is defined in 'data' -->
        <source-monitor
            class="source-monitor"
            ref="source-monitor"
            @time-change="onSourceMonitorTimeChange"
            @select-source-for-observation="onSelectSourceForObservation"
            :sources="sources"
            :sourcesObject="sourcesObject"
            :styles="sourcePlot.styles"
            :sourceNames="sourceNames"
            :width="sourcePlot.width"
            :height="sourcePlot.height">
        </source-monitor>
      </div>
    <p>
        version: {{version}}
    </p>
    </div>
</template>



<script>
import io from "socket.io-client"
import * as log from "loglevel"

//import PausableTimer from "./../pausable_timer.js"

import SourceMonitor from "./SourceMonitor.vue"

var logger = log.getLogger("App") // this must have the name of the App, not
                                  // the component
logger.debug("Planning: logger created")

export default {
    props:{
        domain:            {type: String, default: "localhost"},
        port:              {type: Number, default: 5000},
        version:           {type: String, default: ""},
        author:            {type: String, default: ""},
        thisHostTime:      {type: String, default: ""},
        socket:            {type: Object, default: null},
        registeredPorts:   {type: Object, default: null},
        sourcePlot:        {type: Object, default: null},
        sourceMonitorTime: {type: Object, default: null},
        sources:           {type: Array,  default: () => []},
        sourcesObject:     {type: Object, default: null},
        sourceNames:       {type: Array,  default: () => []}
    },
    components:{
        "source-monitor":SourceMonitor,
    },
    beforeCreate(){
      logger.debug(`Planning.beforeCreate: invoked`);
    },
    created(){
        document.title = "Session Planning";
        logger.debug(`Planning.created: invoked`);
        var srcPltKeys = Object.keys(this.sourcePlot)
        logger.debug(`Planning.created: sourcePlot keys: ${srcPltKeys}`)
        var styleKeys = Object.keys(this.sourcePlot.styles)
        logger.debug(`Planning.created: sourcePlot styles=${styleKeys}`)
    },
    // mounted(){
    //    logger.debug("Planning.mounted invoked")
    // },
    methods:{
        onSelectSourceForObservation(source){
            logger.debug(`selectSourceForObservation: ${source.name}`)
            this.sourceForObservation = source
        },
        formatSourceForObservation: function(sourceObject){
            if (sourceObject === null){first
                return
            }
            var name = sourceObject.name
            var category = sourceObject.category
            return `<span style="color:${this.sourcePlot.styles[category].fill};">${sourceObject.name}</span>`
        },
        initSocket: function(){
            logger.debug(`Planning.initSocket: called with socket = ${this.socket}`)
            this.socket.on("connect", ()=>{
                logger.debug(`Planning.initSocket: connected to ${this.socketPort}`)
                this.socket.emit("hostname")
                bus.$emit(
                    "status:change",
                    `client connected on port ${this.socketPort}`
                )
            })
        },
        onSourceMonitorTimeChange(newTime){
            // in the event that <source-monitor> property 'time-change'
            // happens
            logger.debug(`Planning.onSourceMonitorTimeChange: called for ${newTime}`)
            this.sourceMonitorTime = newTime
        },
        onNodding(flag){
            // in the event that <nodding> property 'nodding' changes
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
            // logger.debug("Planning: socket port changed")
            this.socketPort = this.port
            this.initSocket()
        },
        domain: function(){
            logger.debug("Planning: domain changed")
            this.socketDomain = this.domain
            this.initSocket()
        },
        sourceForObservation(){
            logger.debug("Planning: source for observation changed")
            this.sourceForObservation.formatted = this.formatSourceForObservation(
                                                      this.sourceForObservation)
        }
    },
    data: function(){
        var port = this.port
        logger.debug(`Planning.data: data function called with port: ${port}`)
        logger.debug("Planning.data: refs object:")
        logger.debug(this.$refs) // show refs defined in context 'main'
        return {
            station: 43,
            status: "hello!",
            sourceForObservation:null,
            socketPort: port,
            socketDomain: this.domain
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
</style>
