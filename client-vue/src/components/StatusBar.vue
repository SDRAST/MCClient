<template>
    <div class="stuck">
         <!-- v-html="status"> -->
         <h6>DSS-{{station}} status: {{status}}</h6>
         <h6 v-html="formattedSourceForObservation"></h6>
    </div>
</template>

<script>
export default {
    props: {
        "status": {type:String, default:""},
        "station":{type:Number, default:43},
        "sourceForObservation": {type: Object, default: ()=>null}
    },
    computed: {
        formattedSourceForObservation(){
            if (this.sourceForObservation !== null){
                if ("formatted" in this.sourceForObservation){
                    var text = ["Current source:"]
                    text.push(this.sourceForObservation.formatted)
                    return text.join(" ")
                }
            } else {
                var text = "Current source: none"
                return text
            }
        }
    }
}
</script>


<style scoped>
.stuck {
    position: sticky;
    top: 0px;
    height: auto;
    width: 100%;
    z-index: 2;
    background-color: #f7ffce;
    border-style: ridge;
    border-width: thin;
    border-color: blue;
    display: flex;
    justify-content: space-between;
}

.stuck h6 {
    margin-bottom: 0px;
}


</style>
