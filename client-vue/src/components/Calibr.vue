<template>
  <div>
    <boresight-calibration
        class="boresight-calibration"
        :info="serverInfo.boresight"
        :socket="socket"
        :sourceForObservation="sourceForObservation">
    </boresight-calibration>
    <div class="flux-calibration">
        <flux-calibration
            :info="serverInfo.flux_calibration"
            :socket="socket">
        </flux-calibration>
    </div>
    <div class="spectrometer-calibration">
        <spectrometer-calibration
            :socket="socket"
            :ROACHNames="ROACHNames">
        </spectrometer-calibration>
    </div>
  </div>
</template>

<script>
import FluxCalibration from "./FluxCalibration.vue"
import BoresightCalibration from "./BoresightCalibration/BoresightCalibration.vue"
import SpectrometerCalibration from "./SpectrometerCalibration.vue"

export default {
  props:{
    socket:               {default: null, type: Object},
    serverInfo:           {type:Object, default:null},
    sourceForObservation: {type:Object, default:null},
    ROACHNames:           {type:Array,  default: ()=>[]}
  },
  components:{
      "boresight-calibration":BoresightCalibration,
      "flux-calibration":FluxCalibration,
      "spectrometer-calibration":SpectrometerCalibration,
  },
  created () {
    document.title = "Calibration";
  },
  data: function(){
    return {
      // ROACHNames: []
    }
  }
}
</script>

<style scoped>

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

</style>
