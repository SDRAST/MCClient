<template>
    <div class="grid-container">
        <div>
            <label>
                {{axis}}
            </label>
        </div>
        <div v-for="(dir) in Object.keys(directions)"
             v-show="directions[dir].show">
            <label>{{directions[dir].display}}</label>
            <div v-for="(obj, idx) in channelsToDisplay[dir]"
                 class="channel-display">
                <button
                    :class="obj.classObject"
                    @click="onChannelButtonClick(dir, idx)">
                    {{obj.display}}
                </button>
                <label class="channel-label"
                    v-show="obj.classObject['bg-silver']">
                    {{obj.offset}}
                    <span v-if="obj.score !== null && obj.classObject['bg-silver']">
                        <span v-if="obj.score" v-html="check"></span>
                        <span v-else v-html="x"></span>
                    </span>
                </label>
            </div>
        </div>
    </div>
</template>

<script>
import octicons from "octicons"
import Vue from "vue"

export default {
    props:{
        axis:{type:String, default:""},
        channels:{type:Array, default:()=>[1,2,3,4]},
        directions:{type:Object, default:()=>{
            return {
                right:{
                    show: true,
                    display: "Right"
                },
                left:{
                    show: true,
                    display: "Left"
                }
            }
        }},
    },
    methods: {
        onChannelButtonClick:function(direction, idx){
            var classObject = this.channelsToDisplay[direction][idx].classObject
            classObject["bg-silver"] = ! classObject["bg-silver"]
            Vue.set(
                this.channelsToDisplay[direction][idx],
                "classObject",
                classObject
            )
            var show = this.channelsToDisplay[direction][idx]["classObject"]["bg-silver"]
            this.$emit("channel-selected", this.axis, direction, idx, show)
        },
        updateChannelsToDisplay: function(channels){
            var generateChannelToDisplay = ()=>{
                return channels.map((chan, idx)=>{
                    return Object.assign({}, {
                        display: chan,
                        offset: 0.0,
                        score: null,
                        amplitude: 0.0,
                        classObject: {
                            "channel-button":true,
                            "bg-silver":false
                        }
                    })
                })
            }
            var channelsToDisplay = {}
            Object.keys(this.directions).forEach((d)=>{
                channelsToDisplay[d] = generateChannelToDisplay()
            })
            return channelsToDisplay
        }
    },
    data: function(){
        return {
            channelsToDisplay: this.updateChannelsToDisplay(this.channels),
            x: octicons["x"].toSVG({"class": "fill-red"}),
            check: octicons["check"].toSVG({"class": "fill-green"})
        }
    }
}
</script>

<style scoped>
/* .column-oriented {
    display: flex;
    flex-direction: row;
    justify-content: center;
} */

/* .column-oriented label {
    position: relative;
    top: 0.1rem;
    left: 0.5rem;
} */

/* .space-evenly {
    justify-content: space-evenly;
} */

/* .row-oriented {
    display: flex;
    flex-direction: column;
    justify-content: center;
} */

/* .channel-selector-axis {
    flex-basis: 20%;
} */

/* .channel-selector-direction {
    flex-basis: 80%;
} */

.channel-display {
    display: grid ;
    grid-template-columns: 1fr 3.5rem;
    grid-column-gap: 0.3rem;
}

.channel-button {
    width: 30px;
    height: 30px;
    margin-bottom: 0.5rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    line-height: 1.5rem;
}

.grid-container {
    display: grid;
    grid-column-gap: 0.5rem;
    grid-row-gap: 0.5rem;
    grid-template-columns: 2.0rem 1fr 1fr;
    grid-template-rows: 0.5fr auto;
}

</style>
