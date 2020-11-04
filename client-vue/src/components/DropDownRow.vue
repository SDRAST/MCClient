<template>
    <div :value="displayOptions.value" v-show="displayOptions.show" class="item">
        {{displayOptions.display}}
    </div>
</template>

<script>
export default {
    props:{
        options: {default: {value:"", display:"", show:false}, type:Object}
    },
    methods:{
        onClick: function(){
            this.$emit("update:value", this.value)
        }
    },
    computed:{
        displayOptions: function(){
            var newOptions = Object.assign({}, this.options)
            if (!("display" in newOptions)){
                newOptions.display = newOptions.value
            }
            return newOptions
        }
    }
}
</script>

<style scoped>
.item {}
</style>
