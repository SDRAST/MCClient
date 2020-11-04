<template>
    <button class="bare" @click="toggle" v-html="display"></button>
</template>

<script>
var paths = {
    play:"images/play-button.svg",
    stop:"images/square-shape-shadow.svg"
}

export default {
    methods:{
        toggleDisplay: function(){
            this.stopped = !this.stopped
            if (this.stopped){
                this.display = this.stop
            }else{
                this.display = this.play
            }
        },
        toggle:function(){
            this.toggleDisplay()
            this.$emit("start-stop-toggle",this.stopped)
        }
    },
    data:function(){
        var play = `<span><img style="width:25px;" src="${paths.play}"></span>`
        var stop = `<span><img style="width:25px;" src="${paths.stop}"></span>`
        var display = play
        return {
            "stopped": false,
            "play": play,
            "stop": stop,
            "display":display
        }
    }
}
</script>


<style scoped>
.bare {
    border: 0;
    padding-left: 5px;
    padding-right: 5px;
}
</style>
