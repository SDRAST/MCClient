<template>
    <div class="dropdown">
        <!--
        <div class="dropdown-display no-overflow" :value="displayVal.value">{{displayVal.display}}</div>
        -->
        <div class="dropdown-display no-overflow" v-model="displayVal.value">{{displayVal.display}}</div>
        <button @click="toggle"><span v-html="chevronDown"></span></button>
        <div class="dropdown-content" v-show="show" :style="dropDownStyle">
            <drop-down-row v-for="(elem, idx) in displayContents"
                :key="idx" :options="elem" @click.native="onContentClick(elem, idx)">
            </drop-down-row>
        </div>
    </div>
</template>

<script>
import DropDownMixin from "./DropDownMixin.vue"

export default {
    mixins: [DropDownMixin]
}
</script>

<style>

.no-overflow{
    overflow: hidden;
}

</style>
