<template>
    <div :class="classObject" :style="styleObject">
        <slot></slot>
    </div>
</template>

<script>
export default {
    props:{
        header:{default:"", type:String},
        size:{default:"large", type:String}
    },
    methods:{
        empty:function(val){
            if (val === ""){
                return true
            }
            return false
        }
    },
    data: function(){
        var styleMapping = {
            "xlarge":{"font-size":"1.8rem"},
            "large": {"font-size":"1.5rem"},
            "medium": {"font-size":"1.2rem"},
            "small":{"font-size":"1.0.rem"}
        }
        return {
            classObject: {
                "panel-heading": true,
                "no-margin-bottom": true,
                "table":true,
            },
            styleObject: styleMapping[this.size]
        }
    }
}
</script>

<style scoped>
    .no-margin-bottom{
        margin-bottom:0;
    }
    .no-padding-bottom{
        padding-bottom:0;
    }
    .panel-heading {
        padding-bottom: 0.25rem; /* was 0.5 */
        padding-top: 0.25rem; /* was 0.5 */
    }
    .panel-heading:first-child{
        padding-top:0;
    }
</style>
