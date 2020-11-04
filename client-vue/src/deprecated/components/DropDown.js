import Vue from "vue"
import octicons from "octicons"

import util from "./../util.js"

// var DropDownRow = Vue.extend({
//     props:{
//         options: {default: {value:"", show:false}, type:Object}
//     },
//     methods:{
//         onClick: function(){
//             this.$emit("update:value", this.value)
//         }
//     },
//     computed:{
//         displayOptions: function(){
//             console.log(`options changed: ${this.options.show}`)
//             return this.options
//         }
//     },
//     template:`<div v-bind:value="displayOptions.value" v-show="displayOptions.show" class="item">{{displayOptions.value}}</div>`
// })


var dropDownMixin = {
    components:{
        'drop-down-row':DropDownRow
    },
    props:{
        contents: {type:Array,default:[]}
    },
    methods:{
        hide:function(){this.show=false},
        unhide:function(){this.show=true},
        toggle:function(){this.show = !this.show},
        onContentClick:function(evt){
            this.displayVal = evt.target.getAttribute("value")
            var id = this.$el.getAttribute("id")
            bus.$emit(`${id}-drop-down-click`,this.displayVal)
            this.toggle()
        },
        contentsToDisplay: function(contents){
            return contents.map((item)=>{return {value:item, show:true}})
        }
    },

    watch: {
        contents: function(){
            this.displayContents = this.contentsToDisplay(this.contents)
            this.displayVal = this.contents[0]
        }
    },
    data:function(){
        return {
            show: false,
            displayVal: this.contents[0],
            displayContents: this.contentsToDisplay(this.contents)
        }
    },
    template:`<div class="dropdown">
    <div class="dropdown-display" v-bind:value="displayVal" v-on:update:value="onContentClick">{{displayVal}}</div>
    <button v-on:click="toggle"><span>${octicons["chevron-down"].toSVG()}</span></button>
    <div class="dropdown-content"  v-show="show">
    <drop-down-row v-for="(elem, idx) in displayContents" v-bind:key="idx" v-bind:options="elem" v-on:click.native="onContentClick"></drop-down-row>
    </div>
    </div>`
}
// <div v-on:click="onContentClick" v-for="elem in displayContents" v-bind:value="elem.value" v-show="elem.show">{{elem.value}}</div>

var DropDown = Vue.extend({
    mixins: [dropDownMixin]
})

var DropDownInput = Vue.extend({
    mixins: [dropDownMixin],
    methods:{
        onContentClick:function(value){
            console.log(`onContentClick: ${value}`)
            this.displayInputVal = ""
            this.displayVal = value
            var id = this.$el.getAttribute("id")
            bus.$emit(`${id}-drop-down-click`,this.displayVal)
            this.toggle()
        },
        searchContents: function(evt){
            var currentText = evt.target.value
            var keyCode = evt.keyCode
            if (keyCode === 13){
                var filteredDisplayContent = this.displayContents.filter((item)=>{return item.show})
                if (filteredDisplayContent.length >= 1){
                    this.onContentClick(filteredDisplayContent[0].value)
                    currentText = ""
                }
            }
            this.displayInputVal = currentText
            if (currentText === ""){
                this.displayContents = this.displayContents.map((item, i)=>{
                    item.show = true
                    return item
                })
                this.hide()
            }else{
                this.unhide()
                var shows = []
                this.displayContents.forEach((item, i)=>{
                    var show = false
                    if (util.strIn(item.value, currentText)){
                        show = true
                    }
                    shows.push(show)
                })
                this.displayContents = this.displayContents.map((item, i)=>{
                    item.show = shows[i]
                    return item
                })
            }
        }
    },
    data:function(){
        return {
            show: false,
            displayInputVal: "",
            displayVal: this.contents[0],
            displayContents: this.contentsToDisplay(this.contents)
        }
    },
    template:`<div class="dropdown">
    <input type="text" class="dropdown-display" v-bind:value="displayInputVal" v-bind:placeHolder="displayVal" v-on:keyup="searchContents">
    <button v-on:click="toggle"><span>${octicons["chevron-down"].toSVG()}</span></button>
    <div class="dropdown-content" v-show="show">
    <drop-down-row v-for="(elem, idx) in displayContents" v-bind:key="idx" v-bind:options="elem" v-on:click.native="onContentClick(elem.value)"></drop-down-row>
    </div>
    </div>`
})

export default {
    DropDown: DropDown,
    DropDownInput: DropDownInput,
    DropDownRow: DropDownRow
}
