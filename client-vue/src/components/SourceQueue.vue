<template>
    <rounded-button-list
        :contents="queue"
        @rounded-list-dblclick="onRoundedButtonDblClick">
    </rounded-button-list>
</template>

<script>
import Vue from "vue"
import RoundedButtonList from "./RoundedButtonList.vue"

export default {
    components:{
        "rounded-button-list":RoundedButtonList
    },
    props:{
        contents:{type:Array, default:()=>[]},
        styles: {type:Object, default:()=>{return {}}},
        sourcesObject: {type: Object, default: ()=>{return {}}}
    },
    methods:{
        lookUpSource: function(name){
            // console.log(`SourceQueue.lookUpSource: ${name}`)
            var sourceObject = this.sourcesObject[name]
            var category = sourceObject.category
            if (category === undefined){
                category = "calibrators"
            }
            var queueObject = {
                value: name,
                display: name,
                style:{
                    color:this.styles[category].fill
                }
            }
            return queueObject
        },
        onRoundedButtonDblClick: function(name){
            var sourceObject = this.sourcesObject[name]
            this.$emit("source-dblclick", sourceObject)
        }
    },
    mounted: function(){
        bus.$on("source-info-display:add-to-queue",(name)=>{
            console.log(`SourceQueue: received ${name}`)
            if (!(name in this.queue)){
                var queueObject = this.lookUpSource(name)
                Vue.set(this.queue,name,queueObject)
                this.queue[name] = queueObject
                this.queue.__order__.push(name)
            }
        })
    },
    watch:{
        contents:function(){
            contents.forEach((name)=>{
                var queueObject = this.lookUpSource(name)
                Vue.set(this.queue, name, queueObject)
            })
            this.queue.__order__ = contents
        }
    },
    data:function(){
        return {
            queue: {__order__:[]}
        }
    }
}

</script>
