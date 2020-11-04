<template>
  <div class="spin-box">
    <input class="spin-box-input" type="text" :value="value" @keyup="onInput">
    <button class="spin-box-up" @click="increase">
      <span v-html="chevronUp"></span>
    </button>
    <button class="spin-box-down" @click="decrease">
      <span v-html="chevronDown"></span>
    </button>
  </div>
</template>

<script>
import SpinBoxMixin from "./SpinBoxMixin.vue"

export default {
    mixins:[SpinBoxMixin]
}
</script>
