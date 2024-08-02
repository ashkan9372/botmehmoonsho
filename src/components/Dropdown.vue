<script>
import Button from "@/components/button.vue";

// export default {
//   name: "Dropdown",
//   components: {Button},
//   props:['title', 'options'],
//   data(){
//     return{
//       hidden: false,
//     }
//   }
// }

export default {

  name: "Dropdown",
  components: {Button},
  props:['title', 'options'],
  data() {
    return {
      isOptionsExpanded: false,
    };
  },
  methods: {
    setOption(option, target) {
      this.$emit('DropdownEvent', [option, target]);
      this.isOptionsExpanded = false;
    }
  }
};
</script>

<template>
    <div class="relative space-y-2">
      <Button @click="isOptionsExpanded = !isOptionsExpanded" @blur="isOptionsExpanded = false">
        <template v-slot:title>
            {{ title }}
            <svg
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              class="h-4 w-4 transform transition-transform duration-200 ease-in-out"
              :class="isOptionsExpanded ? 'rotate-180' : 'rotate-0'"
            >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
        </template>
      </Button>
      <transition
        enter-active-class="transform transition duration-500 ease-custom"
        enter-class="-translate-y-1/2 scale-y-0 opacity-0"
        enter-to-class="translate-y-0 scale-y-100 opacity-100"
        leave-active-class="transform transition duration-300 ease-custom"
        leave-class="translate-y-0 scale-y-100 opacity-100"
        leave-to-class="-translate-y-1/2 scale-y-0 opacity-0"
      >
        <ul
          v-show="isOptionsExpanded"
          class="absolute mb-4 overflow-hidden bg-green-400 bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700"
        >
          <li
            v-for="(option, index) in options"
            :key="index"
            class="block w-full px-4 py-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700"
            @click="setOption(option, $event.target)"
          >
            {{ option }}
          </li>
        </ul>
      </transition>
    </div>
</template>

<style>
.ease-custom {
  transition-timing-function: cubic-bezier(.61,-0.53,.43,1.43);
}
</style>