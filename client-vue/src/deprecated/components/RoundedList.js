import Vue from "vue"
import octicons from "octicons"

var roundedListMixin = {
    props:{
        contents:{type:Object,default:()=>{return{__order__:[]}}},
    },
    computed:{
        displayContents: function(){
            var displayContents = this.contents["__order__"].map(
                    (item, idx)=>{
                        var obj = this.contents[item]
                        if (obj.constructor !== Object){
                            obj = {value:obj, display:obj}
                        }else{
                            if (!("value" in obj)){
                                obj.value = item
                            }
                            if ("fill" in obj){
                                obj.style = {}
                                obj.style.color = obj.fill
                            }
                        }
                        return Object.assign({id:idx, show:true, style:{}}, obj)
                    }
            )
            return displayContents
        }
    }
}

var RoundedObjectList = Vue.extend({
    mixins:[roundedListMixin],
})

var RoundedButtonList = Vue.extend({
    mixins:[roundedListMixin],
    template:`<div class="rounded-list">
        <button v-for="item in displayContents" v-bind:style="item.style" v-bind:value="item.value" v-show="item.show" class="item">
            {{item.display}}
        </button>
    </div>`
})

var CheckButton = Vue.extend({
    props:{
        options: {default: {style:{}, show:true, value:"", showCheck:true, display:""}, type:Object}
    },
    computed:{
        show: function(){
            return this.options.show
        }
    },
    methods: {
        toggleCheck: function(){
            this.showCheck = !this.showCheck
            var emitData = {
                hidden: this.showCheck,
                value: this.options.value
            }
            console.log(`CheckButton.toggleCheck: emitting check-button: emitData: ${emitData}`)
            bus.$emit("check-button-toggle", emitData)
        }
    },
    data: function(){
        return {
            showCheck:true
        }
    },
    template: `<button :style="options.style" v-on:click="toggleCheck" v-show="show" class="item" :value="options.value">
                    <span v-show="showCheck">${octicons.check.toSVG()}</span>{{options.display}}
               </button>`
})

var RoundedCheckButtonList = Vue.extend({
    components:{
        "check-button":CheckButton
    },
    mixins:[roundedListMixin],
    template: `<div class="rounded-list">
        <check-button v-for="(item, idx) in displayContents" v-bind:options="item" v-bind:key="idx"></check-button>
    </div>`
})


export default {
    RoundedObjectList: RoundedObjectList,
    RoundedButtonList: RoundedButtonList,
    CheckButton: CheckButton,
    RoundedCheckButtonList: RoundedCheckButtonList
}
