<script>
import * as log from "loglevel"

var logger = log.getLogger("RoundedListMixin")

export default {
    props:{
        // define property 'contents' as an object with a default item
        // '__order__' which is an empty list
        contents:{type:Object, default:()=>{return{__order__:[]}}},
    },
    methods:{
        onContentClick: function(value){
            console.log(`RoundedListMixin.onContentClick: ${value}`)
            this.$emit("rounded-list-click", value)
        },
        onContentDblClick: function(value){
            console.log(`RoundedListMixin.onContentDblClick: ${value}`)
            this.$emit("rounded-list-dblclick", value)
        }
    },
    computed:{
        displayContents: function(){
            // take contents in the specified order and for each item
            // return an Object. If the item is not already an Object then
            // assume it is a string and assign it to attributes 'value' and
            // 'display'.  If it is an Object but does not have an attribute
            // 'value' then assume the item is the value.  If the object has
            // attribute 'fill' then use it to set the objects 'style'
            // attribute to have the property 'color' with the value of 'fill'
            // (An 'arrow' function has arguments on the left and result on
            // the right.)
            console.log("RoundedListMixin.displayContents: invoked")
            console.log(`RoundedListMixin.displayContents: for ${this.contents["__order__"]}`)
            var displayContents = this.contents["__order__"].map(
                    // 'item' is what is being processed and 'idx' is loop index
                    (item, idx)=>{
                        var obj = this.contents[item]
                        console.log(`RoundedListMixin.displayContents processing: ${item}`);
                        // console.log(`RoundedListMixin.displayContents ID: ${idx}`);
                        if (obj.constructor !== Object){
                            obj = {value:obj, display:obj}
                        }else{
                            if (!("value" in obj)){
                                obj.value = item
                            }
                            if ("fill" in obj){
                                if (!("style" in obj)){obj.style={}}
                                obj.style.color = obj.fill
                            }
                        }
                        var keys = Object.keys(obj);
                        // console.log(`RoundedListMixin.displayContents keys: ${keys}`)
                        // 'obj' now has keys:
                        // 'class', 'fill', 'opacity' , 'r', 'display', 'value', 'style'
                        // create a new object with the keys: 'id', 'show',
                        // 'class', 'fill', 'opacity' , 'r', 'display', 'value', 'style'
                        var newobj = Object.assign({id:idx, show:true, style:{}}, obj)
                        var newkeys = Object.keys(newobj);
                        // console.log(`RoundedListMixin.displayContents new keys ${newkeys}`)
                        return newobj
                    }
            )
            console.log(`RoundedListMixin.displayContents returned: ${displayContents}`)
            return displayContents
        }
    }
}
</script>

<style scoped>
.rounded-list {}  /* all elements which have the class 'rounded-list' */

.rounded-list .item{  /* all elements of class 'item' inside 'rounded-list' */
    text-align: left;
    width: 100%;
    border-top-width: 0px;
    border-radius: 0px;
    font-size: 0.8rem;  /* this has no effect */
    margin-bottom: 0px;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
}

.rounded-list .item span {
    float:right;
    position: relative;
    top:2px;
    left:5px;
}

.rounded-list .item:first-child{
    border-top-width: 1px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

.rounded-list .item:last-child{
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
}

.rounded-list .item:hover{
    border-top-width: 1px;
    border-color: #888;
}
</style>
