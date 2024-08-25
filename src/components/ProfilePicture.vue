<script>
import * as d3 from 'd3';
import {clear} from "core-js/internals/task";
export default {
  name: "ProfilePicture",
  props:['src', 'username'],
  data() {
    return {
      // colorScale: d3.scaleSequential(d3.interpolateRainbow)
      colorScale: d3.scaleOrdinal()
        .domain(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        .range(d3.schemeSpectral[7])
    };
  },
  computed: {
    random(){
      const firstTwoLetters = this.username.substring(0, 2);
      // تبدیل حروف به کدهای ASCII و جمع آنها
      let colorCode = firstTwoLetters.charCodeAt(0) + firstTwoLetters.charCodeAt(1);

      // محدود کردن رنگ به بازه 0 تا 255
      colorCode = colorCode % 100;
      return colorCode
    }
  },
};
</script>
<template>
  <template v-if="src">
    <img class="w-10 h-10 rounded-full" :src="src" alt="">
  </template>
  <template v-else>
    <div class="flex justify-center items-center w-10 h-10 rounded-full" :style="{ backgroundColor: colorScale(username[0].toUpperCase()) }">
      {{ (username.charAt(0).toUpperCase() + username.substring(1, 2)) }}
    </div>
  </template>
</template>
