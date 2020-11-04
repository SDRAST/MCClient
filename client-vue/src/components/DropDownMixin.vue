
<script>
import octicons from "octicons"

import DropDownRow from "./DropDownRow.vue"

export default {
    components:{
        'drop-down-row':DropDownRow
    },
    props:{
        contents: {type:Array,default:[]},
        dropDownStyle: {type:Object, default:()=>{return {}}},
    },
    methods:{
        hide:function(){this.show=false},
        unhide:function(){this.show=true},
        toggle:function(){this.show = !this.show},
        onContentClick:function(newDisplayVal, idx){
            this.displayVal = newDisplayVal
            this.idx = idx
            var id = this.$el.getAttribute("id")
            bus.$emit(`${id}-drop-down-click`,this.displayVal.value, idx)
            this.$emit("drop-down-click", this.displayVal.value, idx)
            this.toggle()
        },
        contentsToDisplay: function(contents){
            if (contents.length === 0){
                return [{value: "", display: "", show: true}]
            }else{
                return contents.map((item)=>{
                    if (item.constructor !== Object){
                        return {value:item, display:item, show:true}
                    }else{
                        var newItem = Object.assign({show:true}, item)
                        return newItem
                    }
                })
            }
        }
    },
    watch: {
        contents: function(){
            this.displayContents = this.contentsToDisplay(this.contents)
            this.idx = 0
            this.displayVal = this.displayContents[this.idx]
        }
    },
    data:function(){
        var displayContents = this.contentsToDisplay(this.contents)
        var displayVal = displayContents[0]
        return {
            show: false,
            "displayVal": displayVal,
            "idx":0,
            "displayContents": displayContents,
            chevronDown: octicons["chevron-down"].toSVG()
        }
    }
}
</script>

<style scoped>

.dropdown {
    display: flex;
    flex-flow: row wrap;
    padding:0;
    position: relative;
    /*margin-left: 0.5rem;*/
    text-align: left;
}

.dropdown div.dropdown-display{
    height: 38px;
    border-width: 1px;
    border-style: solid;
    border-color: #bbb;
    border-right-style:none;
    border-top-right-radius: 0px ;
    border-bottom-right-radius: 0px;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
    width: 85%;
    padding-right: 0.5rem;
    padding-top: 5px;
    padding-left: 0.5rem;
    margin: 0;
    max-width: 200px;
}

.dropdown input.dropdown-display{
    border-top-right-radius: 0px ;
    border-bottom-right-radius: 0px;
    text-align:right;
    border-right-style:none;
    height: 38px;
    width: 85%;
    margin-bottom: 0px;
}

/*Define the styling of the button to the right of the dropdown display area*/
.dropdown button {
    border-top-left-radius: 0px ;
    border-bottom-left-radius: 0px;
    width: 15%;
    margin:0;
    padding:0;
    height: 38px;
}

.dropdown button span {
    position: relative;
    bottom: -4px;
    right:0px;
}
/* Dropdown Content (Hidden by Default) */
.dropdown-content {
    display: block;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
    width:100%;
    top:100%;
    max-height: 250px;
    overflow-y: auto;
}

/* divs inside the dropdown */
.dropdown-content div {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    position: relative;
    display: block;
    width: 100%;
}

/* Change color of dropdown links on hover */
.dropdown-content div:hover {background-color: #f1f1f1}

</style>
