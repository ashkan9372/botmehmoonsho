<script>
import Dropdown from "@/components/Dropdown.vue";

export default {
  name: "searchInput",
  components: {Dropdown},
  props: {
    // Receive the initial value from the parent component
    placeholder: {
      type: String,
      default: 'Enter text here'
    },
    filterOptions: {
      type: Array,
      required: true,
    }
  },
  data(){
    return {
        value: '',
        selectedFilter: this.filterOptions[0]
    }
  },
  methods: {
    updateValue(newValue) {
      // Emit the updated value to the parent component
      this.$emit('serachInput', {'filter': this.selectedFilter, 'input': newValue});
    },
    dropdownEvent(event){
      this.selectedFilter = event[0]
    }
  }
}
</script>

<template>
  <form class="flex flex-row items-center gap-2">
    <Dropdown @dropdownEvent="dropdownEvent" title="فیلتر" :options="filterOptions"></Dropdown>
    <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
    <div class="relative ">
        <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
            <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
              </svg>
          </div>
        <input v-model="value" @input="updateValue($event.target.value)" type="search" id="default-search" class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" :placeholder="placeholder" required />
      </div>
  </form>
</template>
