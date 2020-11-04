<template>
    <div class="rounded-list">
        <button v-for="item in displayContents"
                      @dblclick="onContentDblClick(item.value)"
                      @click.default="onContentClick(item.value)"
                      :style="item.style"
                      :value="item.value"
                      v-show="item.show"
                      class="item">
            {{item.display}}
        </button>
    </div>
</template>

<script>
import RoundedListMixin from "./RoundedListMixin.vue"

export default {
    mixins: [RoundedListMixin]
}
</script>
