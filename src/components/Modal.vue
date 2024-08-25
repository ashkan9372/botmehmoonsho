<script>
import Button from "@/components/button.vue";

export default {
  name: "Modal",
  components: {Button},
  props: ['btnTitle', 'modalTitle', 'btnClass'],
  data() {
    return {
      isOpen: false
    };
  },

  computed: {
    isModalVisible() {
      return this.isOpen;
    }
  },

  methods: {
    onToggle() {
      this.isOpen = !this.isOpen;
      this.$emit('modalOpened', this.isOpen);
    }
  }
};
</script>

<template>
    <Button @click="onToggle" :class="btnClass">
      <template v-slot:title>
        {{ btnTitle }}
      </template>
    </Button>
    <!-- Render inside our `<div id="modals"></div>` in index.html -->
    <Teleport to="body">
      <transition name="fade">
      <!-- Show / hide the modal -->
      <div :class="[isModalVisible? '': 'hidden']">
        <!-- The backdrop -->
        <div @click="onToggle" class="fixed inset-0 z-50 bg-gray-900 opacity-40"></div>

        <!-- Where the actual content goes -->
        <div class="fixed inset-0 flex items-center z-50 justify-center overflow-auto">
          <div class="flex flex-col max-h-[600px] bg-white rounded-lg shadow dark:bg-gray-700 max-sm:w-[250px]">
                <!-- Modal header -->
                <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                    <h3 class="md:text-xl font-semibold text-gray-900 dark:text-white">
                        {{ modalTitle }}
                    </h3>
                    <button @click="onToggle" type="button" class="font-sans text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
                        <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                        </svg>
                        <span class="sr-only">Close modal</span>
                    </button>
                </div>
                <!-- Modal body -->
                <div class="font-sans md:p-5 space-y-4">
                  <slot name="modalBody"></slot>
                </div>
                <!-- Modal footer -->
                <div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600"></div>
            </div>
        </div>
      </div>
      </transition>
    </Teleport>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 500ms ease-out;
}
</style>
