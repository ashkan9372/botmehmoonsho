<script>
import {FwbButton} from "flowbite-vue";

export default {
  name: "button",
  components: {FwbButton},
  props: {
    type: {
      type: String,
      default: 'button',
    },
  },
}
</script>

<template>
  <button :type="type" class="truncate font-sans flex flex-row w-full items-center justify-between gap-2 px-5 py-2.5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-md">
    <slot name="title"></slot>
  </button>
</template>
