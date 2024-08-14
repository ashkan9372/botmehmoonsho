<script>
export default {
  name: "input",
  props: {
    title: {
      type: String,
      required: true,
    },
    formName: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    value: {
      type: String,
      default: '',
    },
    type: {
      type: String,
      default: 'text',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    hidden:{
      type: Boolean,
      default: false,
   },
  },
  data(){
    return {
      error: false,
      message: '',
      inputValue: this.value
    }
  },
  methods: {
    updateValue(newValue) {
      this.$emit('update', newValue);
    },
  },
  watch: {
     value(newVal) {
        this.inputValue = newVal;
        // console.log(newVal, this.value, this.inputValue, this.type)
     }
  }
};
</script>

<template>
 <div :class="[hidden ? 'hidden':'flex flex-col md:flex-row gap-2 items-center justify-center']">

    <label
        :for="formName"
        :class="[
          error ? 'peer-focus:text-red-500 text-red-500' : 'peer-focus:text-green-500 text-gray-500'
        ]"
        class="md:text-nowrap mb-2 text-md font-medium font-semibold text-gray-900 dark:text-white">{{ title }}</label>
    <input
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        v-model="inputValue"
        @input="updateValue($event.target.value)"
        type="text"
        :id="formName"
        :disabled="disabled"
        :class="[
          error ? 'text-red-900 border-red-500 focus:border-red-500' : 'text-gray-900 focus:border-green-500 border-gray-300'
        ]"
    />
 </div>
</template>
