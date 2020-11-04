<template>
    <div class="table-row" :class="classObject" :style="styleObject">
        <div class="table-element"
             v-for="(item, idx) in contents"
             :style="computedLayout[idx]"
             v-html="item">
        </div>
        <slot></slot>
    </div>
</template>

<script>
export default {
    props:{
        classObject: {type:Object, default: ()=>{return {}}},
        styleObject: {type:Object, default: ()=>{return {}}},
        contents: {type:Array, default: ()=>[]},
        layout: {type:Array, default: ()=>[]},
    },
    data: function(){
        var computedLayout = this.layout.map(
            (l)=>{
              return {flex:l, "flex-basis":"0"}
            }
        )
        if (this.contents.length !== 0){
            if (this.contents.length !== this.layout.length){
                computedLayout = this.contents.map(
                  ()=>{
                    return {flex:1}
                  }
                )
            }
        }
        // if (computedLayout.length !== 2 && computedLayout.length > 0){
        //     computedLayout[0]["font-weight"] = 400
        // }
        return {
            "computedLayout":computedLayout
        }
    },
    methods:{
        /**
         * Inspired by [this](https://github.com/vuejs/vue/issues/7701) issue
         * I saw, where they show a means of getting rid of extra rendered
         * white space.
         * @param  {Array} node Array of nodes
         * @return {Array} input node with empty text elements removed
         */
        trimExtraText(node){
            node.forEach((childNode, i)=>{
                if (childNode.elm.nodeType === 3 && childNode.elm.data.trim() === ""){
                    node.splice(i, 1)
                }
            })
            return node
        }
    },

    /**
     * @return {[type]} [description]
     */
    mounted(){
        var node = this.$slots.default
        if (node === undefined){
            return
        }
        node = this.trimExtraText(node)
        node.forEach((childNode)=>{
            if (! childNode.elm.classList.contains("table-element")){
                childNode.elm.classList.add("table-element")
            }
        })
        if (this.contents.length === 0){
            if (this.computedLayout.length === node.length){
                node.forEach((childNode, i)=>{
                    Object.keys(this.computedLayout[i]).forEach((style)=>{
                        childNode.elm.style[style] = this.computedLayout[i][style]
                    })
                })
            }
        }
    }
}
</script>

<style scoped>
.table {
    display: flex;
    flex-direction: column;
    margin-bottom: 0.25rem; /* was 0.5rem */
}

.table .table-row {
    width:100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom:0.25rem; /* was 0.5rem */
}

.table .table-row:last-child {
    margin-bottom: 0rem;
}

.table-row .table-element {
    min-width: 0px;
    margin-right:0.5rem;
}

.table-element label {
    /* display: inline; */
    /* position: relative;
    top: 0.3rem; */
}
</style>


<comment>
We can use this component in two ways.
First, we can specify the contents of the row by setting the `contents` property.
Second, we can fill in the <slot></slot> with some HTML elements.
For both, we can set the `layout` property to indicate how the table elements
should be laid out on the page.
</comment>
