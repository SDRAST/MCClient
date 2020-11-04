import * as d3 from "d3"

var D3PlotMixin = {
    props: {
        plotData: {type:Array,default:()=>{return {}}},
        plotOptions: {type:Object, default:()=>{return {}}},
        height: {type:Number,default:300},
        width: {type:Number,default:300},
        options: {type:Object,default:()=>{return {
            margin:{top:0,right:20,bottom:20,left:60},
            xLabel:"",
            yLabel:"",
            axisLabelFontSize:"10px"
        }}}
    },
    mounted: function(){
        var plot = this.createSVG(this.$el)
        var [plot, xScale, xAxis] = this.createXAxis(plot)
        var [plot, yScale, yAxis] = this.createYAxis(plot)
        this.plot = plot
        this.xScale = xScale
        this.yScale = yScale
        this.xAxis = xAxis
        this.yAxis = yAxis
    },
    key: function(){
        if (this.plot !== null){
            this.clearCircles()
            this.updateCircles(this.circles)
        }
    },
    methods:{
        createSVG: function(mount){
            // console.log(`elWidth: ${this.elWidth} elHeight: ${this.elHeight} elMargin: ${JSON.stringify(this.elMargin)}`)
            var svg = d3.select(mount).append("svg")
                    .attr("width", this.elWidth + this.elMargin.left + this.elMargin.right)
                    .attr("height", this.elHeight + + this.elMargin.top + this.elMargin.bottom)
                    .append("g")
                    .attr("transform", `translate(${this.elMargin.left},${this.elMargin.top})`)
            return svg.append("g")
        },
        createXAxis: function(plot){
            var xScale = d3.scaleLinear().domain([0,1]).range([0, this.elWidth]);
            var xAxis = d3.axisBottom(xScale).ticks(10);

            plot.append("g")
                .attr("class", "x axis")
                .attr("transform", `translate(0,${this.elHeight})`)
                .call(xAxis)

            plot.append("text")
                .attr("transform",
                    `translate(${this.elWidth/2}, ${this.elHeight + this.elMargin.bottom*0.8})`)
                .style("text-anchor", "middle")
                .style("font-size", this.elAxisLabelFontSize)
                .text(this.elXLabel)
            return [plot, xScale, xAxis]
        },
        createYAxis: function(plot){
            var yScale = d3.scaleLinear().domain([0,1]).range([this.elHeight, 0]);
            var yAxis = d3.axisLeft(yScale).ticks(10);

            plot.append("g")
                .attr("class", "y axis")
                .call(yAxis)
            plot.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0 - (this.elMargin.left)*0.8)
                .attr("x", 0 - (this.elHeight / 2))
                .attr("dy", ".1em")
                .style("text-anchor", "middle")
                .style("font-size", this.elAxisLabelFontSize)
                .text(this.elYLabel)

            return [plot, yScale, yAxis]
        },
        clearPlot: function(){},
        updatePlot: function(){}
    },
    watch:{
        width:function(newVal){
            this.elWidth = newVal - this.elMargin.left - this.elMargin.right
        },
        height:function(newVal){
            this.elHeight = newVal - this.elMargin.top - this.elMargin.bottom
        },
    },
    data: function(){
        var margin = this.options.margin
        return {
            elHeight: this.height - margin.top - margin.bottom,
            elWidth: this.width - margin.left - margin.right,
            elMargin: this.options.margin,
            elXLabel: this.options.xLabel,
            elYLabel: this.options.yLabel,
            elAxisLabelFontSize: this.options.axisLabelFontSize,
            plot: null,
            xScale: null,
            yScale: null,
            xAxis: null,
            yAxis: null
        }
    },
    template:`<div></div>`
}

export default D3PlotMixin
