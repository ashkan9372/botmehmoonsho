<script>
import JalaliMoment from 'jalali-moment';
import Button from "@/components/button.vue";
export default {
  name: "DatePicker",
  components: {Button},
  props:['date', 'Title', 'modelValue'],
  data(){
    return {
      isOpen: false,
      days: ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"],
      dayIndex: 0,
      hour: 0,
      minute: 0,
    }
  },
  watch: {
    modelValue(newVal) {
      if (newVal !== null) {
        const jalaliDate = JalaliMoment(newVal);
        this.dayIndex = jalaliDate.weekday();
        this.hour = jalaliDate.hour();
        this.minute = jalaliDate.minute();
      }
    }
  },
  mounted() {
    if (this.modelValue !== null) {
      const jalaliDate = JalaliMoment(this.modelValue);
      this.dayIndex = jalaliDate.weekday();
      this.hour = jalaliDate.hour();
      this.minute = jalaliDate.minute();
    }
  },
  methods:{
    changeIndex(amount) {
      this.dayIndex = (this.dayIndex + amount + this.days.length) % this.days.length;
    },
    changeMinute(amount) {
      this.minute = (this.minute + amount + 60) % 60;
    },
    changeHour(amount) {
      this.hour = (this.hour + amount + 24) % 24;
    },
    timeFormater(time){
      if (0<=time && time<10){
        time = `0${time}`
        return time
      } else {
        return time
      }
    },
    onToggle() {
      this.isOpen = !this.isOpen;
      this.$emit('modalOpened', this.isOpen);
    }
  },
  computed: {
    formattedDate() {
      let date = JalaliMoment().day((this.dayIndex + 6) % 7).hour(this.hour).minute(this.minute)
      this.$emit('update:modelValue', date.format('YYYY-MM-DD HH:mm'));
      const dayOfWeek = date.format('dddd');
      const time = date.format('HH:mm');
      return `${dayOfWeek} ${time}`;
    },
    isModalVisible() {
      return this.isOpen;
    }
  },
}
</script>

<template>
    <Button @click="onToggle" class="font-semibold">
      <template v-slot:title>
        {{Title}}: {{ formattedDate }}
      </template>
    </Button>
    <!-- Render inside our `<div id="modals"></div>` in index.html -->
    <Teleport to="body">
      <transition name="fade">
      <!-- Show / hide the modal -->
      <div :class="[isModalVisible? '': 'hidden']">
        <!-- The backdrop -->
        <div @click="onToggle" class="fixed inset-0 bg-gray-900 opacity-40"></div>

        <!-- Where the actual content goes -->
        <div class="fixed inset-0 flex items-center justify-center">
          <div class="flex flex-col items-center justify-center  max-h-[600px] bg-white rounded-lg shadow dark:bg-gray-700">
                <!-- Modal header -->
                <div class="flex items-center justify-between gap-2 text-white bg-blue-600 p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                    <button @click="onToggle" type="button" class="text-white bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
                        <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                        </svg>
                        <span class="sr-only">Close modal</span>
                    </button>
                    <h3 class="text-xl font-semibold text-white">
                      {{ Title }}
                    </h3>
                </div>
                <!-- Modal body -->
                <div class="p-4 md:p-5 space-y-4 overflow-auto min-w-full">
                  <div class="flex flex-row gap-2">

                      <!--    days-->
                      <div class="flex flex-col justify-center items-center">
                        <span @click="changeIndex(1)" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-up" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M7.776 5.553a.5.5 0 0 1 .448 0l6 3a.5.5 0 1 1-.448.894L8 6.56 2.224 9.447a.5.5 0 1 1-.448-.894z"/>
                          </svg>
                        </span>
                        {{days[dayIndex]}}
                        <span @click="changeIndex(-1)" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-down" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67"/>
                          </svg>
                        </span>
                      </div>
        <!--      time-->
                      <div class="flex flex-row">
                        <!--    minute-->
                        <div class="flex flex-col justify-center items-center">
                          <span @click="changeMinute(1)" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-up" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M7.776 5.553a.5.5 0 0 1 .448 0l6 3a.5.5 0 1 1-.448.894L8 6.56 2.224 9.447a.5.5 0 1 1-.448-.894z"/>
                            </svg>
                          </span>
                              {{timeFormater(minute)}}
                              <span @click="changeMinute(-1)" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-down" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67"/>
                            </svg>
                          </span>
                        </div>
                        <div class="flex flex-col justify-center items-center font-bold"><span></span>:<span></span></div>
                        <!--    houe-->
                        <div class="flex flex-col justify-center items-center">
                          <span @click="changeHour(1)" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-up" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M7.776 5.553a.5.5 0 0 1 .448 0l6 3a.5.5 0 1 1-.448.894L8 6.56 2.224 9.447a.5.5 0 1 1-.448-.894z"/>
                            </svg>
                          </span>
                          {{timeFormater(hour)}}
                          <span @click="changeHour(-1)" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-down" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67"/>
                            </svg>
                          </span>
                        </div>
                      </div>
                  </div>
                </div>
            </div>
        </div>
      </div>
      </transition>
    </Teleport>


</template>