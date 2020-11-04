<template>
    <div class="rounded-list">
        <!-- define a DIV consisting of 'check-button' elements
             bind variable 'options' to 'item' returned from 'displayContents'
             and 'key' to the loop item ID -->
        <check-button ref="check-boxes"
                      v-for="(item, idx) in displayContents"
                        :options="item"
                        :key="idx"
                        @click.default="onContentClick(item)"
                        @dblclick.default="onContentDblClick(item)">
       </check-button>
    </div>
</template>


<script>
import CheckButton from "./CheckButton.vue"
import RoundedListMixin from "./RoundedListMixin.vue"

export default {
    components:{
        "check-button":CheckButton
    },
    mixins:[RoundedListMixin],
    beforeCreate(){
      console.log("RoundedCheckButtonList.beforeCreate: invoked")
    },
    created(){
      console.log("RoundedCheckButtonList.created: invoked")
    },
}
</script>
