import Vue from "vue"

var Panel = Vue.extend({
    props:{
        header:{type:String,default:""},
        classObject: {type:Array, default: ()=>[]}
    },
    methods:{
        empty:function(val){
            if (val === ""){
                return true
            }
            return false
        }
    },
    template:`<div>
        <div class="panel-heading" v-if="! empty(header)">{{header}}</div>
        <div class="panel" :class="classObject"><slot></slot></div>
    </div>`
})

export default Panel
