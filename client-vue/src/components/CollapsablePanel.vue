<template>
    <div class="panel" :class="[{'no-padding':noPad}, {'no-border': noBorder}]">
        <panel-heading :size="size">
            <table-row :layout="[0,0,1]">
                <span>
                    <button class="bare" @click="toggle" v-html="burger"></button>
                    <span v-html="header"></span>
                </span>
                <start-stop-button v-show="startStop" ref="start-stop"></start-stop-button>
            </table-row>
        </panel-heading>
        <div v-show="show">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import octicons from "octicons"

import Panel from "./Panel.vue" // we also inherit styles!! ;)
import StartStopButton from "./StartStopButton.vue"
import TableRow from "./TableRow.vue"

export default {
    mixins:[Panel],
    props:{
        startStop: {default:false, type:Boolean}
    },
    components:{
        "start-stop-button":StartStopButton,
        "table-row":TableRow
    },
    data:function(){
        return {
            burger:octicons["three-bars"].toSVG(),
            show:true
        }
    },
    methods:{
        toggle: function(){
            this.show = !this.show
        }
    }
}
</script>

<style scoped>
    .bare {
        border: 0;
        padding-left: 5px;
        padding-right: 5px;
        margin-bottom: 0px;
    }
</style>
