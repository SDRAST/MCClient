<template>
    <div class="boresight-run-container">
        <div class="label-row">
            <label>Type</label>
            <drop-down
                :contents="types"
                ref="type-drop-down"
                @drop-down-click="onTypeDropDownClick">
           </drop-down>
        </div>
      <p><small>
        (Use "scanning" for initial estimate and "stepping" for
        final result.)
      </small></p>
        <div class="label-row">
            <label>Initial EL</label>
            <spin-box
                ref="el-spin-box"
                :init-value="initEL"
                :increment="0.1"
                @spin-box-value="initEL=$event">
            </spin-box>
        </div>
        <div class="label-row">
            <label>Initial XEL</label>
            <spin-box
                ref="xel-spin-box"
                :init-value="initXEL"
                :increment="0.1"
                @spin-box-value="initXEL=$event">
            </spin-box>
        </div>
        <check-button
            class="full-row"
            v-show="true"
            ref="two-direction"
            style="width:100%;"
            :options="{display:'Two Direction?'}">
        </check-button>
        <!-- simulation added by TBHK 2019-06-08 -->
        <check-button
            class="full-row"
            v-show="true"
            ref="simulate"
            style="width:100%;"
            :options="{display:'Simulate?'}">
        </check-button>
        <div class="label-row">
            <label>Iterations</label>
            <spin-box
                ref="iter-spin-box"
                :init-value="iter"
                @spin-box-value="iter=$event">
            </spin-box>
        </div>
        <div class="label-row" v-show="type == 'scanning'">
            <label>Offset Rate</label>
            <spin-box
                ref="offset-rate-spin-box"
                :init-value="rate"
                :increment="1"
                :min-value="0"
                :max-value="20"
                @spin-box-value="rate=$event">
            </spin-box>
        </div>
        <div class="label-row" v-show="type == 'scanning'">
            <label>Sample Rate</label>
            <spin-box
                ref="sample-rate-spin-box"
                :init-value="sampleRate"
                :increment="0.1"
                @spin-box-value="sampleRate=$event">
            </spin-box>
        </div>
        <div class="label-row" v-show="type == 'scanning'">
            <label>Limit</label>
            <spin-box
                ref="limit-spin-box"
                :init-value="limit"
                :increment="1"
                :min-value="0"
                :max-value="200"
                @spin-box-value="limit=$event">
            </spin-box>
        </div>
        <div class="label-row" v-show="type == 'scanning'">
            <label>Settle Time</label>
            <spin-box
                ref="settle-time-spin-box"
                :init-value="settleTime"
                :increment="1"
                :min-value="2"
                :max-value="15"
                @spin-box-value="settleTime=$event">
            </spin-box>
        </div>
        <div class="label-row" v-show="type == 'stepping'">
            <label>Integration Time</label>
            <spin-box
                ref="integration-time-spin-box"
                :init-value="integrationTime"
                :increment="1"
                :min-value="1"
                :mav-value="20"
                @spin-box-value="integrationTime=$event">
            </spin-box>
        </div>
        <div class="label-row" v-show="type == 'stepping'">
            <label>No. Points</label>
            <spin-box
                ref="n-points-spin-box"
                :init-value="nPoints"
                @spin-box-value="nPoints=$event">
            </spin-box>
        </div>
        <button class="full-row" @click="onRunButtonClick">{{runButton.text}}</button>
    </div>
</template>

<script>
import DropDown from "./../DropDown.vue"
import SpinBox from "./../SpinBox.vue"
import TableRow from "./../TableRow.vue"
import CheckButton from "./../CheckButton.vue"


export default {
    components:{
        "drop-down": DropDown,
        "spin-box": SpinBox,
        "table-row":TableRow,
        "check-button":CheckButton,
    },
    methods: {
        onTypeDropDownClick(val, idx){
            this.type = val
        },
        onRunButtonClick: function(evt){
            if (this.runButton.text === "Run"){
                this.$emit("boresight-run",true)
                this.runButton.text = "Stop"
            }else{
                this.$emit("boresight-run",false)
                this.runButton.text = "Run"
            }
        }
    },
    mounted: function(){
        this.$refs["two-direction"].showCheck = false
        this.$refs["type-drop-down"].$on("drop-down-click", (value)=>{
            this.type = value
        })
    },
    data: function(){
        return {
            axes: ["EL","XEL"],
            type: "scanning",
            types: ["scanning", "stepping"],
            initEL: 0.0,
            initXEL: 0.0,
            iter: 1,
            rate: 2.0,
            sampleRate: 0.3,
            limit: 65,
            settleTime: 10,
            nPoints: 9,
            integrationTime: 2.0,
            runButton:{
                text: "Run"
            }
        }
    }
}

</script>

<style scoped>
.no-bottom-margin {
    margin-bottom: 0px;
}

.boresight-run-container {
    display: grid;
    grid-template-columns: 1fr;
    grid-gap: 0.5rem;
}

.boresight-run-container button {
    margin-bottom: 0px;
}

.label-row {
    display: grid ;
    grid-template-columns: 2fr 3fr;
}

.full-row {
    grid-template-columns: 1fr;
}
</style>
