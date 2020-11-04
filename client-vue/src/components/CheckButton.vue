<template>
    <!-- button belongs to classes 'item' and 'check-button' -->
    <button :style="options.style"
            v-on:click="toggleCheck"
            v-show="show"
            class="item check-button"
            :value="options.value">
        <span v-show="showCheck" v-html="check"></span>{{options.display}}
   </button>
</template>

<script>
import octicons from "octicons"

export default {
    props:{
        options: {
          default: {
            style: {},
            show:true,
            value:"",
            showCheck:true,
            display:""
          },
          type:Object
        }
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
            // console.log(`CheckButton.toggleCheck: emitting check-button: emitData: ${JSON.stringify(emitData)}`)
            this.$emit("check-button-toggle", emitData)
            this.$parent.$emit("toggle", emitData)
        }
    },
    data: function(){
        return {
            showCheck:true,
            check: octicons.check.toSVG()
        }
    }
}
</script>

<style scoped>
.check-button {
    text-align: left;
    height: 1.5rem;
    line-height: 1.5rem;
    font-size: 0.8rem;
}

.check-button span{
    float:right;
    position: relative;
    top:2px;
    left:5px;
}
</style>
