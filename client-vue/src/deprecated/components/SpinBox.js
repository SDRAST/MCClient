import octicons from "octicons"
import Vue from "vue"

var spinBoxMixin = {
    props: {
        "init-value":{type: Number, default: 0},
        "min-value":{type: Number, default: -100},
        "max-value":{type: Number, default: 100},
        "increment":{type: Number, default: 1},
    },
    data: function(){
        return {
            value: parseFloat(this.initValue,10),
            chevronUp:octicons["chevron-up"].toSVG(),
            chevronDown: octicons["chevron-down"].toSVG()
        }
    },
    methods:{
        increase: function(){this.value += this.increment; return this.value},
        decrease: function(){this.value -= this.increment; return this.value},
    },
    template: `<div class="spin-box"><input type="text" v-bind:value="value">
<button class="up" v-on:click="increase"><span>${octicons["chevron-up"].toSVG()}</span></button>
<button class="down" v-on:click="decrease"><span>${octicons["chevron-down"].toSVG()}</span></button></div>`
}

var SpinBox = Vue.extend({
    mixins:[spinBoxMixin]
})

var SpinBoxInput = Vue.extend({
    props: {
        something:{}
    },
    mixins:[spinBoxMixin],
    methods:{
        accept: function(){this.$emit("my-event")}
    },
    template: `<div class="with-accept spin-box"><input type="text" v-bind:value="value">
<button class="up" v-on:click="increase"><span>${octicons["chevron-up"].toSVG()}</span></button>
<button class="down" v-on:click="decrease"><span>${octicons["chevron-down"].toSVG()}</span></button>
<button class="accept" v-on:click="accept"><span>${octicons.check.toSVG()}</span></button></div>`
})

module.exports = {
    SpinBox: SpinBox,
    SpinBoxInput: SpinBoxInput
}
