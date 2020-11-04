<template>
<div class="with-accept spin-box">
    <input class="with-accept spin-box-input" type="text" :value="value" @keyup="onInput">
    <button class="with-accept spin-box-up" @click="increase"><span v-html="chevronUp"></span></button>
    <button class="with-accept spin-box-down" @click="decrease"><span v-html="chevronDown"></span></button>
    <button class="with-accept spin-box-accept" @click="accept"><span v-html="check"></span></button>
</div>
</template>



<script>
import SpinBoxMixin from "./SpinBoxMixin.vue"

export default {
    mixins:[SpinBoxMixin],
    methods:{
        accept: function(){
            this.$emit("input-spin-box-accept",this.value)
        }
    }
}
</script>
