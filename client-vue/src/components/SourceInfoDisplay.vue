<template>
    <panel v-show="category !== ''">
        <div class="table">
        <table-row>
            <div v-html="name[0]"></div>
            <div class="align-right" v-html="name[1]"></div>
        </table-row>
        <table-row v-show="category[0] !== 'antenna'">
            <div>{{ra[0]}}</div>
            <div class="align-right" v-html="ra[1]"></div>
        </table-row>
        <table-row v-show="category[0] !== 'antenna'">
            <div>{{dec[0]}}</div>
            <div class="align-right" v-html="dec[1]"></div>
        </table-row>
        <table-row>
            <div>{{az[0]}}</div>
            <div class="align-right" v-html="az[1]"></div>
        </table-row>
        <table-row>
            <div>{{el[0]}}</div>
            <div class="align-right" v-html="el[1]"></div>
        </table-row>
        <div v-show="category[0] === 'calibrator'">
            <hr/>
            <table-row>
                <div>{{flux[0]}}</div>
                <div class="align-right" v-html="flux[1]"></div>
            </table-row>
        </div>
        <div v-show="category[0] === 'catalog'">
            <hr/>
            <table-row>
                <div>Status</div>
                <div class="align-right" v-html="status"></div>
            </table-row>
            <hr/>
            <div v-if="obsData.length > 0">
                <table-row>
                    <div>Observation Date (YY-DOY)</div>
                    <div class="align-right">Integration time (min)</div>
                </table-row>
                <table-row v-for="(item, idx) in obsData" :key="idx">
                    <div v-html="item.date"></div>
                    <div class="align-right" v-html="item.integ || 0"></div>
                </table-row>
            </div>
            <table-row v-else>
                <div>Unobserved</div>
            </table-row>
        </div>
        <div v-show="category[0] === 'known maser'">
            <hr/>
            <table-row>
                <div>{{velocity[0]}}</div>
                <div class="align-right" v-html="velocity[1]"></div>
            </table-row>
        </div>
        </div>
        <button class="u-full-width" @click="onAddToQueueClick">Add to Queue</button>
    </panel>
</template>

<script>
import Vue from "vue"

import TableRow from "./TableRow.vue"
import Panel from "./Panel.vue"

export default{
    components:{
        "table-row":TableRow,
        "panel":Panel
    },
    props:{
        sourceInfo:{type:Object, default:()=>{return {}}}
    },
    created:function(){
        bus.$on("source-plot:source-clicked",()=>{})
    },
    methods:{
        toCode: function(val){
            if (val !== undefined){
                return `<code>${parseFloat(val,10).toFixed(3)}</code>`
            }
        },
        onAddToQueueClick: function(){
            bus.$emit("source-info-display:add-to-queue", this.name[1])
        },
        processSourceInfo: function(info){
            if (info === undefined){info = {}}
            info = Object.assign({name:null, info:{obs_data:[{}], category:""}}, info)
            var flux = 0.0
            if ("flux" in info.info){ flux = this.toCode(info.info.flux.K) }
            var velocity = 0.0
            if ("velocity" in info.info) {velocity = this.toCode(info.info.velocity)}
            var obsData = []
            if ("obs_data" in info.info){
                obsData = info.info.obs_data
            }
            var link
            if (obsData[0] !== undefined){
                if ("link" in obsData[0]){
                    link = obsData[0].link
                }
            }
            var processed = {
                "name": info.name,
                "ra": this.toCode(info.ra*this.convert),
                "dec": this.toCode(info.dec*this.convert),
                "az": this.toCode(info.az),
                "el": this.toCode(info.el),
                "category": info.info.category,
                "status": info.info.status,
                "flux": flux,
                "obsData":obsData,
                "link": link,
                "velocity":velocity
            }
            console.log(`SourceInfoDisplay.processSourceInfo: returns ${JSON.stringify(processed)}`)
            return processed
        }
    },
    watch:{
        sourceInfo: function(newSourceInfo){
            var processed = this.processSourceInfo(newSourceInfo)
            if (processed.link != undefined){
                Vue.set(this.name, 0, `<a href="${processed.link}">Name</a>`)
            }else{
                Vue.set(this.name, 0, "Name")
            }
            Vue.set(this.name, 1, processed.name)
            Vue.set(this.ra, 1,  processed.ra)
            Vue.set(this.dec, 1, processed.dec)
            Vue.set(this.az, 1,  processed.az)
            Vue.set(this.el, 1,  processed.el)
            Vue.set(this.flux, 1, processed.flux)
            Vue.set(this.velocity, 1, processed.velocity)
            this.category = processed.category
            this.status = processed.status
            this.obsData = processed.obsData
        }
    },
    data: function(){
        var convert = 180. / Math.PI
        var processed = this.processSourceInfo(this.sourceInfo)
        return {
            "convert":convert,
            name: ["Name", processed.name],
            ra: ["RA J2000", processed.ra],
            dec: ["DEC J2000", processed.dec],
            az: ["Azimuth", processed.az],
            el: ["Elevation", processed.el],
            category: processed.category,
            status: processed.status,
            flux: ["Flux (Jy)", processed.flux],
            obsData: processed.obsData,
            link: processed.link,
            velocity:["Velocity (km/s)", processed.velocity]
        }
    }
}
</script>


<style scoped>
.table {
    margin-bottom: 0.5rem;
}

.align-right {
    text-align:right;
}
</style>
