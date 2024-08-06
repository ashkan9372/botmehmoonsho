<script>
export default {
  name: "table",
}
</script>
<template>
  <div class="overflow-auto">
    <table class="min-w-full font-sans text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
      <thead class="truncate font-sans text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <slot name="head"></slot>
        </tr>
      </thead>
      <tbody>
        <slot name="body"></slot>
      </tbody>
    </table>
  </div>
</template>
