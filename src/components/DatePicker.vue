<script>
export default {
  name: "DatePicker",
  data(){
    return {
      days: ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"],
      dayIndex: 0,
      hour: 0,
      minute: 0,
    }
  },
  updated() {
    this.$emit('update', this.dayIndex, this.timeFormater(this.hour)+':'+this.timeFormater(this.minute));
    console.log(this.dayIndex, this.timeFormater(this.hour)+':'+this.timeFormater(this.minute))
  },
  methods:{
    increaseIndex(){
      if (this.dayIndex<this.days.length-1){
        this.dayIndex +=1
      } else {
        this.dayIndex = 0
      }
    },
    increaseMinute(){
      if (this.minute<59){
        this.minute +=1
      } else {
        this.minute = 0
      }
    },
    increasehour(){
      if (this.hour<23){
        this.hour +=1
      } else {
        this.hour = 0
      }
    },
    decreaseIndex(){
      if (0<this.dayIndex && this.dayIndex<=this.days.length-1){
        this.dayIndex -=1
      } else {
        this.dayIndex = this.days.length-1
      }
    },
    decreaseMinute(){
      if (0<this.minute && this.minute<=59){
        this.minute -=1
      } else {
        this.minute = 59
      }
    },
    decreaseHour(){
      if (0<this.hour && this.hour<=23){
        this.hour -=1
      } else {
        this.hour = 23
      }
    },
    timeFormater(time){
      if (0<=time && time<10){
        time = `0${time}`
        return time
      } else {
        return time
      }
    }
  },
}
</script>

<template>
  <div class="flex flex-row gap-2">
<!--    days-->
    <div class="flex flex-col justify-center items-center">
      <span @click="increaseIndex" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-up" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M7.776 5.553a.5.5 0 0 1 .448 0l6 3a.5.5 0 1 1-.448.894L8 6.56 2.224 9.447a.5.5 0 1 1-.448-.894z"/>
        </svg>
      </span>
      {{days[dayIndex]}}
      <span @click="decreaseIndex" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-down" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67"/>
        </svg>
      </span>
    </div>
<!--      time-->
      <div class="flex flex-row">
        <!--    minute-->
        <div class="flex flex-col justify-center items-center">
          <span @click="increaseMinute" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-up" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M7.776 5.553a.5.5 0 0 1 .448 0l6 3a.5.5 0 1 1-.448.894L8 6.56 2.224 9.447a.5.5 0 1 1-.448-.894z"/>
            </svg>
          </span>
              {{timeFormater(minute)}}
              <span @click="decreaseMinute" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-down" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67"/>
            </svg>
          </span>
        </div>
        <div class="flex flex-col justify-center items-center font-bold"><span></span>:<span></span></div>
        <!--    houe-->
        <div class="flex flex-col justify-center items-center">
          <span @click="increasehour" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-up" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M7.776 5.553a.5.5 0 0 1 .448 0l6 3a.5.5 0 1 1-.448.894L8 6.56 2.224 9.447a.5.5 0 1 1-.448-.894z"/>
            </svg>
          </span>
          {{timeFormater(hour)}}
          <span @click="decreaseHour" class="bg-blue-500 rounded-lg px-2 py-1 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-compact-down" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67"/>
            </svg>
          </span>
        </div>
      </div>
  </div>
</template>