<!-- Home Page for DSN Science M&C

When the page has been compiled, the 'created(){...}' section of the script is
called.  It calls 'initSocket()'.
 -->
<template>
    <div class="main">
    <!-- <h6 align="center">DSS<code>{{station}}</code> Monitor and Control</h6> -->
    <div class="app-container">
        <!-- bind variable 'sourcePlot' attribute 'styles' to property 'styles';
            variable 'sourcePlot' is defined in 'data' -->
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
        <div class="power-meter-monitor">
            <power-meter-monitor
                ref="power-meter-monitor"
                :socket="socket">
            </power-meter-monitor>
        </div>
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

import PowerMeterMonitor from "./PowerMeterMonitor.vue"
import AntennaMonitor from "./AntennaMonitor.vue"
import AntennaControl from "./AntennaControl.vue"
import SocketIOMixin from "./SocketIOMixin.vue"

var logger = log.getLogger("App") // this must have the name of the App, not
                                  // the component
logger.debug("Home: logger created")

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
        "power-meter-monitor":PowerMeterMonitor,
        "antenna-monitor": AntennaMonitor,
        "antenna-control": AntennaControl,
    },
    created(){
        logger.debug("Home.created invoked");
        document.title = "RA M&C Home";
        //this.initSocket();
    },
    //mounted(){
    //    logger.debug("Home.mounted invoked")
  //  },
    methods:{
        setStatus: function(newStatus){
            // logger.debug(`Home.setStatus for ${newStatus}`)
            this.status = newStatus
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
            logger.debug(`Home.initSocket: called with socket = ${this.socket}`)
            this.socket.on("connect", ()=>{
                logger.debug(`Home.initSocket: connected to ${this.socketPort}`)
                this.socket.emit("hostname")
                bus.$emit(
                    "status:change",
                    `client connected on port ${this.socketPort}`
                )
            })
        },
        onSelectSourceForObservation(source){
            logger.debug(`selectSourceForObservation: ${source.name}`)
            this.sourceForObservation = source
        }
    },
    watch: {
        port: function(){
            // logger.debug("Home: socket port changed")
            this.socketPort = this.port
            this.initSocket()
        },
        domain: function(){
            logger.debug("Home: domain changed")
            this.socketDomain = this.domain
            this.initSocket()
        },
        sourceForObservation(){
            logger.debug("AppOld: source for observation changed")
            this.sourceForObservation.formatted = this.formatSourceForObservation(
                                                      this.sourceForObservation)
        }
    },
    data: function(){
        var port = this.port
        logger.debug(`Home.data: data function called with port: ${port}`)
        logger.debug("Home.data: refs object:")
        logger.debug(this.$refs) // show refs defined in context 'main'
        return {
            station: 43,
            status: "hello!",
            sourceForObservation:null,
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

</style>
