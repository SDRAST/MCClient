<template>
    <div class="dropdown">
        <input type="text"
               class="dropdown-display"
               :value="displayInputVal"
               :placeHolder="displayVal.display"
               @keyup="searchContents">
        <button @click="toggle"><span v-html="chevronDown"></span></button>
        <div class="dropdown-content" v-show="show">
            <drop-down-row v-for="(elem, idx) in displayContents"
                           :key="idx"
                           :options="elem"
                           @click.native="onContentClick(elem)"></drop-down-row>
        </div>
    </div>
</template>


<script>
import DropDownMixin from "./DropDownMixin.vue"
import util from "./../util.js"

export default {
    mixins: [DropDownMixin],
    methods:{
        onContentClick:function(newDisplayVal){
            // console.log(`onContentClick: ${value}`)
            this.displayVal = newDisplayVal
            this.displayInputVal = ""
            var id = this.$el.getAttribute("id")
            this.$emit("drop-down-click", this.displayVal.value)
            bus.$emit(`${id}-drop-down-click`,this.displayVal.value)
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
        var displayContents = this.contentsToDisplay(this.contents)
        if (displayContents.length === 0){
            var displayVal = {value:"",display:""}
        }else{
            var displayVal = displayContents[0]
        }
        return {
            show: false,
            displayInputVal: "",
            "displayVal": displayVal,
            "displayContents": displayContents
        }
    }
}
</script>
