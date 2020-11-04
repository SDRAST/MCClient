
<script>
import octicons from "octicons"

export default {
    props: {
        "init-value":{type: Number, default: 0},
        "min-value":{type: Number, default: -100},
        "max-value":{type: Number, default: 100},
        "increment":{type: Number, default: 1},
    },
    watch:{
        value: function(newValue){
            this.$emit("spin-box-value", newValue)
        },
        initValue: function(newValue){
            this.value = newValue
        }
    },
    data: function(){
        return {
            value: parseFloat(this.initValue,10),
            chevronUp:octicons["chevron-up"].toSVG(),
            chevronDown: octicons["chevron-down"].toSVG(),
            check: octicons.check.toSVG()
        }
    },
    methods:{
        increase: function(){this.value += this.increment; return this.value},
        decrease: function(){this.value -= this.increment; return this.value},
        onInput: function(evt){
            var currentVal = parseFloat(evt.target.value)
            if (!(isNaN(currentVal))){
                this.value = currentVal
            }
        }
    }
}
</script>

<style scoped>
.spin-box {
    display: inline-block;
    position: relative;
    padding: 0;
    text-align: left;
}
/* this positions the up/down symbol inside the button */
.spin-box button span {
    position:relative;
    bottom: 9px; /* was 6px */
}

.spin-box-input {
    text-align: right;
    height: 2.0rem; /* default was 2.5rem */
    width: 80%;
    margin: 0;
    border-top-right-radius: 0px ;
    border-bottom-right-radius: 0px;
    border-right-style: none;
    padding-left: 0.4rem;
}

.spin-box button {
    position: absolute;
    margin:0;
    padding:0;
    height: 1.0rem; /* was 1.25 rem */
    width: 20%;
}

.spin-box button.spin-box-up {
    border-bottom-left-radius: 0px;
    border-top-left-radius: 0px;
    border-bottom-right-radius: 0px;
    border-bottom-style:none;
}

.spin-box button.spin-box-down{
    top:1.0rem; /* was 1.25 rem */
    border-bottom-left-radius: 0px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

.with-accept.spin-box-input {
    text-align: right;
    width: 70%;
    margin:0;
    border-top-right-radius: 0px ;
    border-bottom-right-radius: 0px;
    border-right-style:none;
    padding-left:0.4rem;
}

.spin-box button {
    position: absolute;
    margin:0;
    padding:0;
    height: 1.0rem;
    width: 20%;
}

.with-accept.spin-box button {
    width: 15%;
}

.with-accept.spin-box button.spin-box-accept {
    height: 2.0rem; /* was 2.5 */
    left: 85%;
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    border-left-style: none;
}

.with-accept.spin-box button.spin-box-accept span{
    position: relative;
    bottom: 0px;
}

.with-accept.spin-box button.spin-box-up {
    border-bottom-left-radius: 0px;
    border-top-left-radius: 0px;
    border-bottom-right-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-style:none;
}

.spin-box button.spin-box-down{
    top:1.0rem;
    border-bottom-left-radius: 0px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

.with-accept.spin-box button.spin-box-down{
    top:1.0rem; /* was 1.25rem */
    border-bottom-left-radius: 0px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
}
</style>
