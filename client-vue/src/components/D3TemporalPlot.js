import Vue from "vue"
import * as d3 from "d3"

import D3PlotMixin from "./D3PlotMixin.js"

var D3TemporalPlot = Vue.extend({
    mixins: [D3PlotMixin],
    props: {
        maxPlotElements: {type:Number, default: 200},
        plotData: {type:Array, default:()=>[]},
        plotOptions: {type:Array, default:()=>[]},
    },
    methods:{
        updatePlot: function(data){
            var currentTime = new Date()
            var newDeltaTime = (currentTime - this.initialTime) / 1000
            console.log(`this.temporalData.time.length: ${this.temporalData.time.length}, this.temporalData.dep.length: ${this.temporalData.dep.length}`)
            this.temporalData.time.push(newDeltaTime)
            this.temporalData.dep.push(data)
            if (this.temporalData.time.length > this.maxPlotElements){
                this.temporalData.time.shift()
                this.temporalData.dep.shift()
            }
            var firstTime = this.temporalData.time[0]
            if (firstTime === newDeltaTime){
                firstTime = 0.0
            }
            var deltaTime = newDeltaTime - firstTime
            var xlim = [firstTime*0.8, newDeltaTime + 0.1*deltaTime]

            var [min, max] = [Math.min.apply(null, data), Math.max.apply(null, data)]
            var delta = max - min
            var ylim = [min - 0.3*delta, max + 0.3*delta]

            this.xScale.domain(xlim)
            this.yScale.domain(ylim)
            this.clearPlot()
            data.forEach((val, i)=>{
                var plotData = []
                this.temporalData.time.forEach((t, j)=>{
                    var [t, y] = [this.temporalData.time[j], this.temporalData.dep[j][i]]
                    plotData.push({
                        fill: this.plotOptions[i].fill,
                        r: (y <= ylim[1] && y >= ylim[0]) ? 3.5: 0.0,
                        t: t,
                        y: y
                    })
                })

                this.plot.selectAll(".circle")
                    .data(plotData)
                    .enter().append("circle")
                    .attr("class", "dot")
                    .attr("r",(d)=>d.r)
                    .attr("cx",(d)=>this.xScale(d.t))
                    .attr("cy",(d)=>{
                        return this.yScale(d.y)
                    })
                    .style("fill",(d)=>d.fill)
            })

            this.xAxis = d3.axisBottom(this.xScale).ticks(10)
            this.yAxis = d3.axisLeft(this.yScale).ticks(10)
            this.plot.select("g.x.axis").call(this.xAxis)
            this.plot.select("g.y.axis").call(this.yAxis)

        },
        clearPlot: function(){
            this.plot.selectAll("circle").remove()
        }
    },
    watch:{
        plotData: function(newData){
            console.log("D3TemporalPlot.watch.plotData")
            this.updatePlot(newData)
        }
    },
    data:function(){
        var initialTime = new Date()
        if (this.plotData.length == 0){
            var initialDepArray = []
            var initialTimeArray = []
        }else{
            var initialDepArray = [this.plotData]
            var initialTimeArray = [(new Date() - initialTime)/1000]
        }
        return {
            "initialTime": initialTime,
            temporalData: {time:initialTimeArray, dep:initialDepArray}
        }
    }
})

export default D3TemporalPlot
