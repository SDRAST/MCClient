<template>
    <collapsable-panel header="Source Monitor"
                       :noBorder="false" size="large">
      <div class="container">
        <!-- this is the source filter panel on the left -->
        <div>
            <panel header="Category" :noBorder="true" size="medium">
                <rounded-check-button-list
                    ref="category-list"
                    :contents="styles" >
                </rounded-check-button-list>
            </panel>
            <source-filter
                ref="source-filter"
                :elLimits="elLimits"
                :azLimits="azLimits"
                :fluxLimits="fluxLimits"
                :obsLimits="obsLimits"
                @setElLimits="setElLimits"
                @setAzLimits="setAzLimits"
                @setFluxLimits="setFluxLimits"
                @setObsLimits="setObsLimits">
            </source-filter>
        </div>
        <!-- this is the source polar plot in the center -->
        <div ref="source-plot-container">
            <d3-polar-plot
                ref="source-plot"
                @circle-click="onPolarPlotClick"
                @circle-dbclick="onPolarPlotDblClick"
                @circle-mouseover="onPolarPlotMouseOver"
                @circle-mouseout="onPolarPlotMouseOut"
                :circles="computedSources"
                :circle-options="styles"
                :width="computedWidth"
                :height="computedHeight"
                :key="computedRender">
            </d3-polar-plot>
            <P>
              Double click on source to select for queue
            </P>
        </div>
        <!-- this is the source information and selection on the right -->
        <div class="third-column-container">
            <!-- this is the source time panel; used for planning -->
            <panel :noPad="true" :noBorder="true"
                   :header="timeHeader()" size="medium">
                <div class="planning-container">
                    <label>Days</label><spin-box @spin-box-value="onDaysChange"></spin-box>
                    <label>Hours</label><spin-box @spin-box-value="onHoursChange"></spin-box>
                    <label>Minutes</label><spin-box @spin-box-value="onMinutesChange"></spin-box>
                </div>
                <div class="equal-row">
                    <button @click="onTimeAccept">Advance</button>
                    <button @click="onTimeNow">Now</button>
                </div>
            </panel>
            <!-- this is the source search panel -->
            <panel :noPad="true" :noBorder="true"
                   header="Search" size="medium">
                <drop-down-input
                    :contents="sourceNames"
                    @drop-down-click="($event)=>{setSourceInfo($event);setSourcePlotToolTip($event)}"
                    ref="source-search">
                </drop-down-input>
            </panel>
            <!-- this is the source information panel -->
            <panel :noPad="true" :noBorder="true"
                   header="Source Information" size="medium">
                <source-info-display
                    :sourceInfo="sourceInfo">
                </source-info-display>
            </panel>
            <!-- this is the source queue and selection panel -->
            <panel :noPad="true" :noBorder="true"
                   header="Source Queue" size="medium">
                <source-queue
                    :styles="styles"
                    :sourcesObject="sourcesObject"
                    @source-dblclick="selectSourceForObservation">
                </source-queue>
                <P>
                  Double click to enable 'Point'
                </P>
            </panel>
            <!-- adding "go to source" button here -->
            <div>
                <button class="full-row" @click="onPointClick"
                        v-html="pointText"></button>
                <P>
                  Click this again after server restart
                </P>
            </div>
        </div> <!-- end third column -->
      </div>
    </collapsable-panel>
</template>


<script>
import Vue from "vue"

import CollapsablePanel from "./CollapsablePanel.vue"
import Panel from "./Panel.vue"
import PanelHeading from "./PanelHeading.vue"
import RoundedCheckButtonList from "./RoundedCheckButtonList.vue"
import InputDropDown from "./InputDropDown.vue"
import SpinBox from "./SpinBox.vue"
import SourceInfoDisplay from "./SourceInfoDisplay.vue"
import SourceQueue from "./SourceQueue.vue"
import D3PolarPlot from "./D3PolarPlot.js"
import TableRow from "./TableRow.vue"
import SourceFilter from "./SourceFilter.vue"
import SocketIOMixin from "./SocketIOMixin.vue"

export default {
    //props:["styles",
    //       "sources",
    //       "sourcesObject",
    //       "sourceNames",
    //       "width",
    //       "height"],
    props: {
      socket:               {default: null, type: Object},
      styles:               {type:Object, default:()=>{return {}}},
      sources:              {type: Array,  default: () => []},
      sourcesObject:        {type: Object, default: ()=>{return {}}},
      sourceNames:          {type: Array,  default: () => []},
      width:                Number,
      height:               Number,
      sourceForObservation: {type:Object, default:()=>{return {name:""}}}
    },
    components:{
        "panel":Panel,
        "panel-heading":PanelHeading,
        "collapsable-panel":CollapsablePanel,
        "table-row":TableRow,
        "rounded-check-button-list":RoundedCheckButtonList,
        "d3-polar-plot":D3PolarPlot,
        "drop-down-input":InputDropDown,
        "spin-box":SpinBox,
        "source-info-display":SourceInfoDisplay,
        "source-queue":SourceQueue,
        "source-filter":SourceFilter
    },
    methods:{
        test:function(){
            console.log("hey")
        },
        serverCommand: SocketIOMixin.methods.serverCommand,
        generateTime: function(){
            var now = new Date()
            now.setDate(now.getDate() + this.days)
            now.setHours(now.getHours() + this.hours)
            now.setMinutes(now.getMinutes() + this.minutes)
            return now
        },
        timeHeader: function(){
            var date = this.generateTime()
            return `Time ${date.toString()}`
        },
        reRenderSourcePlot: function(width, height){
            this.computedWidth = width
            this.computedHeight = height
            if (this.computedRender == 0){
                this.computedRender = 1
            }else{
                this.computedRender = 0
            }
        },
        onResize: function(){
            var renderedWidth = this.$refs["source-plot-container"].offsetWidth
            this.reRenderSourcePlot(renderedWidth, renderedWidth)
        },
        togglePlotCategories: function(value, hidden){
            this.categoriesToDisplay[value] = hidden
            this.computedSources = this.filterSources(this.sources)
        },
        setSourceInfo: function(sourceName){
            if (sourceName in this.sourcesObject){
                this.sourceInfo = this.sourcesObject[sourceName]
                if (this.sourceInfo.category === "catalog-sources"){
                    console.log(this.calculateTotalObservationTime(this.sourceInfo))
                }
            }
        },
        setSourcePlotToolTip: function(sourceName){
            var node = this.findPolarPlotNodeByName(sourceName).node()
            if (node !== null){
                this.$refs["source-plot"].tooltipClick.show(this.sourceInfo, 0, [node])
            }
        },
        selectSourceForObservation(source){
            this.$emit("select-source-for-observation", source)
        },
        onPolarPlotClick: function(d){
            // console.log(`SourceMonitor.onPolarPlotClick: ${d.name}`)
            // console.log(`SourceMonitor.onPolarPlotClick: ${JSON.stringify(d)}`)
        },
        onPolarPlotDblClick: function(d, i, node){
            // console.log(`SourceMonitor.onPolarPlotDblClick: ${JSON.stringify(d)}`)
            var name = d.name
            this.setSourceInfo(name)
        },
        onPolarPlotMouseOver:function(d){
            // console.log(`SourceMonitor.onPolarPlotMouseOver: ${JSON.stringify(d)}`)
        },
        onPolarPlotMouseOut: function(d){
            // console.log(`SourceMonitor.onPolarPlotMouseOut: ${JSON.stringify(d)}`)
        },
        onDaysChange: function(val){
            this.days = val
            this.$emit("time-change", this.generateTime())
        },
        onHoursChange: function(val){
            this.hours = val
            this.$emit("time-change", this.generateTime())
        },
        onMinutesChange: function(val){
            this.minutes = val
            this.$emit("time-change", this.generateTime())
        },
        onTimeAccept: function(){
            this.$emit("time-change", this.generateTime())
        },
        onTimeNow: function(){
            this.$emit("time-change", null)
        },
        calculateTotalObservationTime: function(source){
            var totalTime = 0.0
            var obsData = source.info.obs_data
            if (obsData !== undefined){
                obsData.forEach((sessionInfo)=>{
                    if ("integ" in sessionInfo){
                        var integ = parseFloat(sessionInfo.integ)
                        if (!isNaN(integ)){
                            totalTime += integ
                        }
                    }
                })
            }
            return totalTime
        },
        filterElevation: function(d){
            if (this.elLimits.length === 0){
                return true
            }
            if (d.el >= this.elLimits[0] && d.el <= this.elLimits[1]){
                return true
            }
            return false
        },
        filterAzimuth: function(d){
            if (this.azLimits.length === 0){
                return true
            }
            if (d.az >= this.azLimits[0] && d.az <= this.azLimits[1]){
                return true
            }
            return false
        },
        filterFlux: function(d){
            if (d.category === "calibrators"){
                if ("flux" in d.info){
                    var kBandFlux = parseFloat(d.info.flux.K)
                    if (kBandFlux !== 0 && kBandFlux < this.fluxLimits[0] || kBandFlux > this.fluxLimits[1]){
                        return false
                    }
                }
            }
            return true
        },
        filterObsTime: function(d){
            if (d.category === "catalog-sources"){
                var totalObsTime = this.calculateTotalObservationTime(d)
                if (totalObsTime < this.obsLimits[0] || totalObsTime > this.obsLimits[1]){
                    return false
                }
            }
            return true
        },
        filterCategory: function(d){
            return this.categoriesToDisplay[d.category]
        },
        filterSources: function(sourceList){
            var newSourceList = []
            sourceList.forEach((d)=>{
                if (this.filterElevation(d) && this.filterAzimuth(d) &&
                    this.filterFlux(d) && this.filterObsTime(d) &&
                    this.filterCategory(d)){
                    newSourceList.push(d)
                }
            })
            return newSourceList
        },
        setElLimits: function(idx, value){
            console.log(`setElLimits: ${idx} ${value}`)
            Vue.set(this.elLimits, idx, value)
        },
        setAzLimits: function(idx, value){
            console.log(`setAzLimits: ${idx} ${value}`)
            Vue.set(this.azLimits, idx, value)
        },
        setFluxLimits: function(idx, value){
            console.log(`setFluxLimits: ${idx} ${value}`)
            Vue.set(this.fluxLimits, idx, value)
        },
        setObsLimits: function(idx, value){
            console.log(`setObsLimits: ${idx} ${value}`)
            Vue.set(this.obsLimits, idx, value)
        },
        findPolarPlotNodeByName: function(name){
            var filterFn = (d)=>{return name === d.name}
            return this.$refs["source-plot"].filterNode(filterFn)
        },
        onPointClick: function(){
            var sourceName = this.sourceForObservation.name
            if (sourceName !== ""){
                console.log(`onPointClick: for ${sourceName}`)
                this.point(sourceName)
            }
        },
        point: function(sourceName){
            console.log(`AntennaControl.point: ${sourceName}`)
            this.serverCommand("point",[sourceName],{},"")
        },
        startTimers: function(){}
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
        this.onResize()
        window.addEventListener('resize', this.onResize)
        this.$refs["category-list"].$on("toggle", (evtData)=>{
            this.togglePlotCategories(evtData.value, evtData.hidden)
        })
    },
    data:function(){
        var categoriesToDisplay = {}
        Object.keys(this.styles).forEach((category)=>{
            categoriesToDisplay[category] = true
        })
        return {
            computedWidth: this.width,
            computedHeight: this.height,
            computedRender: this.render,
            computedSources: this.filterSources(this.sources),
            sourceInfo: {},
            elLimits: [18,88],
            azLimits: [0,360],
            fluxLimits: [0,30],
            obsLimits: [0,120],
            "categoriesToDisplay": categoriesToDisplay,
            days: 0,
            hours: 0,
            minutes: 0
        }
    },
    watch:{
        sources: function(newSources){
            // console.log("SourceMonitor.watch.sources: called")
            this.computedSources = this.filterSources(this.sources)
        },
        elLimits: function(newLimits){
            this.computedSources = this.filterSources(this.sources)
        },
        azLimits: function(newLimits){
            this.computedSources = this.filterSources(this.sources)
        },
        fluxLimits: function(newLimits){
            this.computedSources = this.filterSources(this.sources)
        },
        obsLimits: function(newLimits){
            this.computedSources = this.filterSources(this.sources)
        },
        width: function(newWidth){
            this.computedWidth = newWidth
        },
        height:function(newHeight){
            this.computedHeight = newHeight
        },
        render:function(newRender){
            this.computedRender = newRender
        }
    }
}
</script>

<style scoped>

.container {
    display: grid;
    grid-template-columns: 2fr 6fr 2fr;
    grid-gap: 0.5rem 0.5rem;
}

.planning-container {
    display: grid;
    grid-template-columns: 0.4fr 1fr;
    grid-gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.full-row {
    grid-column: 1 / 4;
}

.equal-row {
    display: grid ;
    grid-template-columns: 1fr 1fr;
}

.third-column-container {

}

</style>
