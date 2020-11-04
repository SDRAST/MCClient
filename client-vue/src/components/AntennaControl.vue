
<template>
    <collapsable-panel header="Antenna Control">
        <div class="container">
            <button class="full-row" @click="onPointClick" v-html="pointText"></button>
        </div>
        <panel header="Offsets" size="medium">
            <div class="container scrollable-child">
                <label>EL PO</label>
                <spin-box-with-accept @input-spin-box-accept="setOffset('EL',$event)">
                </spin-box-with-accept>
                <label>xEl PO</label>
                <spin-box-with-accept @input-spin-box-accept="setOffset('XEL',$event)">
                </spin-box-with-accept>
                <label>S/R Angle</label>
                <spin-box-with-accept @input-spin-box-accept="setSubReflAng('SR',$event)">
                </spin-box-with-accept>
                <label>S/R Pos</label>
                <input-drop-down ref="subref-drop-down"
                                 :contents="subrefpos"></input-drop-down>
                <label>XT SR</label>
                <spin-box-with-accept @input-spin-box-accept="setOffset('XT',$event)">
                </spin-box-with-accept>
                <label>YT SR</label>
                <spin-box-with-accept @input-spin-box-accept="setOffset('YT',$event)">
                </spin-box-with-accept>
                <label>X SR</label>
                <spin-box-with-accept @input-spin-box-accept="setOffset('X',$event)">
                </spin-box-with-accept>
                <label>Y SR</label>
                <spin-box-with-accept @input-spin-box-accept="setOffset('Y',$event)">
                </spin-box-with-accept>
                <label>Z SR</label>
                <spin-box-with-accept @input-spin-box-accept="setOffset('Z',$event)">
                </spin-box-with-accept>
            </div>
            <div class="container">
                <button class="full-row" @click="clearOffsets">Clear Offsets</button>
                <button class="full-row" @click="clearRates">Clear Offset Rates</button>
                <button class="full-row" @click="onStowClick">Stow</button>
            </div>
        </panel>
        <panel header="NMC Workstation" size="medium">
            <div class="workstation">
                <!-- show the current workstation and site if selected -->
                <label v-show="currentWorkstation !== null">Current Workstation: <span v-html="currentWorkstation"></span></label>
                <label v-show="currentSite !== null">Current Site: <span v-html="currentSite"></span></label>
                <!-- site and workstation selection -->
                <label>Site</label>
                <input-drop-down ref="site-drop-down" :contents="sites"></input-drop-down>
                <label>Workstation</label>
                <input-drop-down ref="workstation-drop-down" :contents="workstations"></input-drop-down>
                <button class="full-row" @click="onConnectClick">Connect</button>
            </div>
        </panel>
    </collapsable-panel>
</template>

<script>
import Panel from "./Panel.vue"
import CollapsablePanel from "./CollapsablePanel.vue"
import SpinBoxWithAccept from "./SpinBoxWithAccept.vue"
import InputDropDown from "./InputDropDown.vue"
import TableRow from "./TableRow.vue"
import SocketIOMixin from "./SocketIOMixin.vue"

import util from "./../util.js"
import PausableTimer from "./../pausable_timer.js"

export default{
    mixins:[SocketIOMixin],
    components:{
        "collapsable-panel": CollapsablePanel,
        "spin-box-with-accept": SpinBoxWithAccept,
        "input-drop-down": InputDropDown,
        "table-row": TableRow,
        "panel": Panel
    },
    props:{
        sourceForObservation: {type:Object, default:()=>{return {name:""}}}
    },
    methods:{
        setOffset: function(axis, value){
            console.log(`AntennaControl.setOffset: ${axis}, ${value}`)
            this.serverCommand("hdwr",
                               ["Antenna","set_offset_one_axis", axis, value],
                               {},"")
        },
        setSubReflAng: function(value){
            console.log(`AntennaControl.setSubReflAng: set to ${value}`)
            this.serverCommand("hdwr", ["Antenna", "R", value],{},"")
        },
        clearOffsets: function(){
            console.log("AntennaControl.clearOffsets")
            this.serverCommand("hdwr",["Antenna", "clr_offsets"],{},"")
        },
        clearRates: function(){
            console.log("AntennaControl.clearOffsets")
            this.serverCommand("hdwr",["Antenna", "clr_rate"],{},"")
        },
        connectToWorkstation: function(site, workstation){
            console.log(`AntennaControl.connectToWorkstation ${site}, ${workstation}`)
            this.serverCommand("hdwr",
                               ["Antenna","connect_to_hardware",workstation, site],
                               {},
                               "connect_to_hardware_handler")
        },
        point: function(sourceName){
            console.log(`AntennaControl.point: ${sourceName}`)
            this.serverCommand("point",[sourceName],{},"")
        },
        formatOnSource: function(){
            var status = ["Point:"]
            if (this.onsource === null){
                status.push("unknown")
            }else if (this.onsource){
                status.push("On source")
            }else if (! this.onsource){
                status.push("Slewing")
            }
            return status.join(" ")
        },
        registerSocketHandlers: function(){
            // onSourceHandler does nothing
            this.socket.on("onsource_handler",this.onSourceHandler)
            // the next two set the site and server
            this.socket.on("wsn_handler", this.onWorkStationNumber)
            this.socket.on("site_handler", this.onSiteName)
            // this gives a value to variable 'antennaSimulated'
            this.socket.on("simulated_handler", this.onSimulatedHandler)
            // this event causes getInitilaData() to be invoked
            this.socket.on("connect_to_hardware_handler",
                           this.onConnectToHardwareHandler)
        },
        startTimers: function(){
            var updateTime = 10000 // used to initialize this timer
            // defines the timer
            var retrieveSimulatedOnSource = (interval)=>{
                var timer = new PausableTimer(()=>{
                    this.onSourceHandler()
                }, interval)
                timer.start()
            }
            var retrieveOnSource = (interval)=>{
                var timer = new PausableTimer(()=>{
                    this.socket.emit("hdwr",
                                     ["Antenna","onsource"],{},
                                     "onsource_handler")
                }, interval)
                timer.start()
            }
            // start timer
            if (this.simulated){
                retrieveSimulatedOnSource(updateTime)
            }else{
                // retrieveOnSource(updateTime)
            }
        },
        getInitialData: function(){
            this.serverCommand("hdwr",["Antenna","simulated"],{},
                               "simulated_handler")
            this.serverCommand("hdwr",["Antenna","wsn"],{},"wsn_handler")
            this.serverCommand("hdwr",["Antenna","site"],{},"site_handler")
        },
        onSourceHandler: function(data){
        },
        onWorkStationNumber: function(data){
            var wsn = data.args[0]
            this.currentWorkstation = wsn
            console.log(`AntennaControl.onWorkStationNumber: ${wsn}`)
        },
        onSiteName: function(data){
            var site = data.args[0]
            this.currentSite = site
            console.log(`AntennaControl.onSiteName: ${site}`)
        },
        onSimulatedHandler: function(data){
            var antennaSimulated = data.args[0]
            this.antennaSimulated = antennaSimulated
            console.log(`AntennaControl.onSimulatedHandler: ${antennaSimulated}`)
        },
        onConnectToHardwareHandler: function(data){
            console.log(`AntennaControl.onConnectToHardwareHandler: ${Object.keys(data.args[0])}`)
            this.getInitialData()
        },
        onConnectClick: function(){
            var site = this.$refs["site-drop-down"].displayVal.value
            var ws = this.$refs["workstation-drop-down"].displayVal.value
            this.connectToWorkstation(site, ws)
        },
        onPointClick: function(){
            var sourceName = this.sourceForObservation.name
            if (sourceName !== ""){
                console.log(`onPointClick: for ${sourceName}`)
                this.point(sourceName)
            }
        },
        onStowClick: function(){
          // send stow command
        }
    },
    computed:{
        pointText(){
            var pointText = ["Point"]
            if (this.sourceForObservation !== null){
                if ("formatted" in this.sourceForObservation){
                    pointText.push("to")
                    pointText.push(this.sourceForObservation.formatted)
                }
            }
            return pointText.join(" ")
        }
    },
    mounted: function(){

    },
    data:function(){
        return {
            sites: ["CDSCC","GDSCC","MDSCC"],
            //workstations: [{display:"0 (simulator)", value:0}].concat([91,92]).concat(util.range(1,10)),
            workstations: [{display:"0 (simulator)", value:0}].concat([91,92]),
            currentWorkstation: null,
            currentSite: null,
            antennaSimulated: null,
            onsource: null,
            subrefpos: ["none", "P1L", "P1R", "P3", "P4"]
        }
    }
}
</script>

<style scoped>
label {
    display: unset;
}

.scrollable-child {
    margin-bottom: 0.5rem;
}

.container {
    display: grid;
    grid-template-columns: 0.4fr 1fr;
    grid-gap: 0.25rem;
}

.container button{
    margin-bottom: 0.0rem;
}

.full-row {
    grid-column: 1 / 3;
    font-size: 15px;
}

.scrollable-child {
    max-height: 200px;
}

</style>
