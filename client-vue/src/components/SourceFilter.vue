<template>
    <panel header="Filter" :noBorder="true" size="medium">
        <panel header="Elevation" size="medium">
            <div class="table">
                <table-row :layout="[1,1]">
                    <label>Minimum</label>
                    <spin-box :min-value="0"
                              :max-value="90"
                              :init-value="elLimits[0]"
                              @spin-box-value="$emit('setElLimits', 0, $event)"></spin-box>
                </table-row>
                <table-row :layout="[1,1]">
                    <label>Maximum</label>
                    <spin-box :min-value="0"
                              :max-value="90"
                              :init-value="elLimits[1]"
                              @spin-box-value="$emit('setElLimits', 1, $event)"></spin-box>
                </table-row>
            </div>
        </panel>
        <panel header="Azimuth" size="medium">
            <div class="table">
                <table-row :layout="[1,1]">
                    <label>Minimum</label>
                    <spin-box :min-value="0"
                              :max-value="360"
                              :init-value="azLimits[0]"
                              @spin-box-value="$emit('setAzLimits', 0, $event)"></spin-box>
                </table-row>
                <table-row  :layout="[1,1]">
                    <label>Maximum</label>
                    <spin-box :min-value="0"
                              :max-value="360"
                              :init-value="azLimits[1]"
                              @spin-box-value="$emit('setAzLimits', 1, $event)"></spin-box>
                </table-row>
            </div>
        </panel>
        <panel header="Calibrator Flux" size="medium">
            <div class="table">
                <table-row  :layout="[1,1]">
                    <label>Minimum</label>
                    <spin-box :min-value="0" :max-value="30" :increment="0.1" :init-value="fluxLimits[0]"
                              @spin-box-value="$emit('setFluxLimits', 0, $event)"></spin-box>
                </table-row>
            </div>
        </panel>
        <panel header="Observation Time" size="medium">
            <div class="table">
                <table-row :layout="[1,1]">
                    <label>Maximum</label>
                    <spin-box :min-value="0" :max-value="200" :increment="1" :init-value="obsLimits[1]"
                              @spin-box-value="$emit('setObsLimits', 1, $event)"></spin-box>
                </table-row>
            </div>
        </panel>
    </panel>
</template>

<script>
import Panel from "./Panel.vue"
import TableRow from "./TableRow.vue"
import SpinBox from "./SpinBox.vue"
import RoundedCheckButtonList from "./RoundedCheckButtonList.vue"

export default {
    components:{
        "panel":Panel,
        "table-row":TableRow,
        "spin-box":SpinBox,
        "rounded-check-button-list": RoundedCheckButtonList
    },
    props:{
        elLimits: {type:Array, default:()=>[]},
        azLimits: {type:Array, default:()=>[]},
        fluxLimits: {type:Array, default:()=>[]},
        obsLimits: {type:Array, default:()=>[]},
    },
    beforeCreate(){
      console.log("SourceFilter.beforeCreate: invoked")
    },
    created(){
      console.log("SourceFilter.created: invoked")
    }
}

</script>
