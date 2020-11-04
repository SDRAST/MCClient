<template>
    <collapsable-panel :header="header">
        <div class="nodding-container">
            <div class="label-row">
                <label>Cycles</label>
                <spin-box ref="cycles-spin-box"
                    :init-value="cycles"
                    :increment="1"
                    @spin-box-value="cycles=$event">
                </spin-box>
            </div>
            <div class="label-row">
                <label>Time per scan (s)</label>
                <spin-box ref="time-per-scan-spin-box"
                    :init-value="timePerScan"
                    :increment="1"
                    @spin-box-value="timePerScan=$event">
                </spin-box>
            </div>
            <div class="label-row">
                <label>Integration time (s)</label>
                <spin-box ref="integration-time-spin-box"
                    :init-value="integrationTime"
                    :increment="1"
                    @spin-box-value="integrationTime=$event">
                </spin-box>
            </div>
        </div>
        <button class="full-row u-full-width start-nodding"
                @click="onStartNoddingClick">Start Nodding</button>
        <hr/>
        <button
            class="full-row u-full-width stop-nodding"
            @click="onStopNoddingClick">
            Stop Nodding
        </button>
    </collapsable-panel>
</template>

<script>
import * as log from "loglevel"

import SpinBox from "./SpinBox.vue"
import CollapsablePanel from "./CollapsablePanel.vue"
import SocketIOMixin from "./SocketIOMixin.vue"

var logger = log.getLogger("Nodding")

export default {
    mixins:[SocketIOMixin],
    props:{
        sourceForObservation: {type:Object, default: ()=>{return null}}
    },
    components: {
        "spin-box": SpinBox,
        "collapsable-panel": CollapsablePanel
    },
    methods: {
        onStartNoddingClick(){
            logger.debug("Nodding.onStartNoddingClick")
            bus.$emit("status:change", "starting nodding")
            this.twoBeamNod()
        },
        onStopNoddingClick(){
            this.clicks += 1
            if (this.clicks === 1){
                this.timer = setTimeout(()=>{
                    this.clicks = 0
                    bus.$emit("status:change", "double click to stop nodding")
                }, this.delay)
            }else{
                clearTimeout(this.timer)
                this.clicks = 0
                bus.$emit("status:change", "stopping nodding")
                this.$emit("nodding", false)
            }
        },
        twoBeamNod(){
            logger.debug("Nodding.twoBeamNod")
            this.$emit("nodding", true)
            var options = {
                cycles: this.cycles,
                scan_time: this.timePerScan,
                integration_time: {"Backend": this.integrationTime}
            }
            //if (this.sourceForObservation !== null){
            //    options["src_name_or_dict"] = this.sourceForObservation.name
            //}

            this.serverCommand(
                "two_beam_nod", [], options, "two_beam_nod_handler"
            )
        },
        twoBeamNodHandler(data){
            var results = data.args[0]
            console.log(`twoBeamNodHandler: ${JSON.stringify(results)}`)
            if ("cycle" in results){
                bus.$emit("status:change",
                          `nodding: cycle ${results.cycle},
                          feed ${results.feed}`)
            }
            if (results.done){
                bus.$emit("status:change", "nodding finished")
                this.$emit("nodding", false)
            }
        },
        registerSocketHandlers(){
            this.socket.on("two_beam_nod_handler", this.twoBeamNodHandler)
        }
    },
    computed:{
        header(){
            var headerText = ["Nodding"]
            if (this.sourceForObservation !== null){
                if ("formatted" in this.sourceForObservation){
                    headerText.push(this.sourceForObservation.formatted)
                }
            }
            return headerText.join(" ")
        }
    },
    data(){
        return {
            cycles: 1,
            timePerScan: 5,
            integrationTime: 1.0,
            delay: 400,
            timer: null,
            clicks: 0
        }
    }
}
</script>


<style scoped>
.nodding-container {
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

.full-row {
    display: grid;
    grid-template-columns: 1fr;
    grid-gap: 0.5rem;
}

.start-nodding {}
.start-nodding:hover {
    /* color: inherit; */
    border-color: var(--green);
}

.stop-nodding {}
.stop-nodding:hover {
    /* color: inherit; */
    border-color: var(--red);
}

</style>
