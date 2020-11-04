import Vue from "vue"
import * as d3 from "d3"

import D3PlotMixin from "./D3PlotMixin.js"

/**
 * Should send data of the following type:
 * :plotData=[
 *      {
 *          x: [],
 *          y: [],
 *          options: {}
 *     }
 * ]
 * :plotdata = "[
 *     {x:util.range(0,10),
 *     y:util.range(0,10),
 *     options:{type:"scatter"}},
 *    {x:util.range(0,10,0.5),
 *     y:util.range(0,20,1),
 *    options:{class:"dot", r:5.0}},
 *    {x:util.range(0,10,0.1),
 *     y:util.range(0,10,0.1).map((x)=>x**2),
 *    options:{"type":"line","stroke-width":1.5}},
 *    {x:util.range(0,10,0.1),
 *     y:util.range(0,10,0.1).map((x)=>-(x**2)+10),
 *    options:{class:"line","stroke-width":1.5,stroke:"rgb(66, 134, 244)"}},
 * ]"
 * @type {[type]}
 */
var D3StaticPlot = Vue.extend({
    mixins: [D3PlotMixin],
    props: {
        plotData: {type:Array, default:()=>{return [{x:[],y:[],options:{}}]}},
    },
    methods:{
        defaultPlotOptions: function(data){
            const defaultScatterOptions = {
                "class": "dot",
                r: 3.5,
                fill: "rgb(0,0,0)",
                opacity: 0.8
            }
            const defaultLineOptions = {
                "class":"line",
                "stroke-linejoin": "round",
                "stroke-linecap": "round",
                "stroke-width": 1.5,
                "fill":"none",
                "stroke":"rgb(0,0,0)"
            }
            data.forEach((datum, i)=>{
                if (!("options" in datum)){
                    datum.options = {}
                }
                var newOptions = Object.assign(Object.assign({}, defaultScatterOptions), datum.options)
                if (datum.options.class === "line" || datum.options.type === "line"){
                    newOptions = Object.assign(Object.assign({}, defaultLineOptions), datum.options)
                }
                data[i].options = newOptions
            })
            return data
        },
        updatePlot: function(data){
            // console.log("D3StaticPlot.updatePlot")
            data = this.defaultPlotOptions(data)

            var minMax = (arr, scaleFactor)=>{
                if (scaleFactor == undefined){
                    scaleFactor = 0.3
                }
                var [min, max] = [Math.min.apply(null, arr), Math.max.apply(null, arr)]
                var delta = max - min
                return [min - (delta*scaleFactor), max+(delta*scaleFactor)]
            }

            var _updatePlot = (x,y,options)=>{
                if (x.length !== y.length){
                    console.error("D3StaticPlot.updatePlot: X and Y must me same length")
                    return
                }
                var xlim = minMax(x, 0.0)
                var ylim = minMax(y, 0.0)
                var plotData = x.map((_, i)=>{
                    return Object.assign({"x":x[i],"y":y[i]}, options)
                })
                if (options.class === "line"){
                    plotData = {"data":plotData,"options":plotData[0]}
                }
                return [xlim, ylim, plotData]
            }

            var linePlotData = []
            var scatterPlotData = []
            var xlims = []
            var ylims = []
            data.forEach((datum)=>{
                // console.log(datum.options)
                var [xlim, ylim, plotDatum] = _updatePlot(datum.x, datum.y, datum.options)
                if (datum.options.class === "dot"){
                    scatterPlotData = scatterPlotData.concat(plotDatum)
                }else if (datum.options.class === "line"){
                    linePlotData.push(plotDatum)
                }
                xlims = xlims.concat(xlim)
                ylims = ylims.concat(ylim)
            })
            var xlim = minMax(xlims, 0.1)
            var ylim = minMax(ylims, 0.1)
            this.xScale.domain(xlim)
            this.yScale.domain(ylim)
            this.plot.selectAll(".circle")
                .data(scatterPlotData)
                .enter().append("circle")
                .attr("class", "dot")
                .attr("r", d=>d.r)
                .attr("cx",d=>this.xScale(d.x))
                .attr("cy",d=>this.yScale(d.y))
                .style("fill",d=>d.fill)
                .style("opacity",d=>d.opacity)

            var lineFunction = d3.line()
                                 .x(d=>this.xScale(d.x))
                                 .y(d=>this.yScale(d.y))

            this.plot.selectAll(".line")
                .data(linePlotData)
                .enter().append("path")
                .attr("class", "line")
                .attr("fill","none")
                .attr("stroke",d=>{return d.options.stroke})
                .attr("stroke-linejoin", d=>d.options["stroke-linejoin"])
                .attr("stroke-linecap", d=>d.options["stroke-linecap"])
                .attr("stroke-width", d=>d.options["stroke-width"])
                .attr("d", (d)=>{return lineFunction(d.data)})

            this.xAxis = d3.axisBottom(this.xScale).ticks(10)
            this.yAxis = d3.axisLeft(this.yScale).ticks(10)
            this.plot.select("g.x.axis").call(this.xAxis)
            this.plot.select("g.y.axis").call(this.yAxis)
        },
        clearPlot: function(){
            this.plot.selectAll("circle").remove()
            this.plot.selectAll(".line").remove()
        }
    },
    mounted:function(){
        this.updatePlot(this.plotData)
    },
    watch:{
        plotData: function(newData){
            this.updatePlot(newData)
        }
    }
})

export default D3StaticPlot
