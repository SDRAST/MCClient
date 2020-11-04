<template>
    <div class="panel" :class="[{'no-padding':noPad}, {'no-border': noBorder}]">
        <panel-heading v-show="showHeader" v-html="header" :size="size"></panel-heading>
        <slot></slot>
    </div>
</template>


<script>
import PanelHeading from "./PanelHeading.vue"

export default {
    components:{
        "panel-heading": PanelHeading
    },
    props:{
        showHeader: {type:Boolean, default:true},
        header:{type:String,default:""},
        noPad:{type:Boolean, default:false},
        noBorder:{type:Boolean, default:false},
        size:{type:String, default:"large"}
    }
}
</script>

<style>
.panel {
    border-color: #dddddd;
    border-radius: 4px;
    border-width: 1px;
    border-style: solid;
    padding: 0.25rem 0.25rem 0.25rem 0.25rem; /* was 0.5; change has no effect */
    margin-bottom: 0.25rem;
}

.no-border.panel {
    border: none;
}
.panel.v.half{
    height: 49.5%;
    margin-bottom: 0.5rem;
}

.panel.v.half:last-child {
    margin-bottom: 0px;
}
</style>

<style scoped>
.no-padding{
    padding: 0;
}
.no-border{
    border: none;
}
</style>
