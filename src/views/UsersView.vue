<script>
// @ is an alias to /src
import Table from "@/components/table.vue";
import SearchInput from "@/components/searchInput.vue";
import Button from "@/components/button.vue";
import Dropdown from "@/components/Dropdown.vue";

export default {
  name: 'UsersView',
  components: {
    Dropdown,
    Button,
    SearchInput,
    Table,
  },
  data() {
    return {
      heads: ['پروفایل', 'نام و نام خانوادگی', 'یوزرنیم', 'اکشن'],
      datum: [{profile:{name:'mahdi', username:'@hosseini'}, fullName:'mahdi hosseini', userId:'hsm'}],
    }
  },
  methods: {
    editUser(id){
      this.$router.push({ path: '/Profile', query: { id: id, route: '/'} });
    },
    filterBasedOnColumn(event) {
      console.log(event)
      let filter = event['filter']
      let searchTerm = event['input']
      if (searchTerm == ''){
        this.datum = this.copyOfDatum
      } else {
        this.datum = this.datum.filter(item => {
          const searchText = searchTerm.toLowerCase();
          // Search fullName using includes
          if (filter == 'نام و نام خانوادگی'){
            return item.fullName.toLowerCase().includes(searchText);
          }
          if (filter == 'یوزرنیم'){
            return item.userId.toLowerCase().includes(searchText);
          }
        });
      }
    },
    sortBasedOnNewUser(){
      this.datum.sort((a, b) => {
        // Sort by ID first (ascending)
        if (a.id < b.id) return -1;
        if (a.id > b.id) return 1;
        return 0; // No further sorting needed if no invest field or IDs are equal
      });
    },
    sortBasedOnOldUser(){
      this.datum.sort((a, b) => {
        // Sort by ID first (ascending)
        if (a.id > b.id) return -1;
        if (a.id < b.id) return 1;
        return 0; // No further sorting needed if no invest field or IDs are equal
      });
    },
    sortBasedOnAlphba(){
      this.datum.sort((a, b) => {
        const nameA = a.fullName.toLowerCase(); // Ensure case-insensitive sorting
        const nameB = b.fullName.toLowerCase();
          if (nameA < nameB) return -1;
          if (nameA > nameB) return 1;
        return 0; // No change if names are equal
      });
    },
    sortBasedOnInverseAlphba(){
      this.datum.sort((a, b) => {
        const nameA = a.fullName.toLowerCase(); // Ensure case-insensitive sorting
        const nameB = b.fullName.toLowerCase();
        if (nameA > nameB) return -1;
        if (nameA < nameB) return 1;
        return 0; // No change if names are equal
      });
    },
    dropdownEvent(event){
      console.log(event[0]);
      if (event[0]=="جدیدترین کاربر"){
        this.sortBasedOnNewUser()
        console.log(this.datum)
      }
      if (event[0]=="قدیمی ترین کاربر"){
        this.sortBasedOnOldUser()
        console.log(this.datum)
      }
      if (event[0]=="حروف الفبا"){
        this.sortBasedOnAlphba()
        console.log(this.datum)
      }
      if (event[0]=="حروف الفبا برعکس"){
        this.sortBasedOnInverseAlphba()
        console.log(this.datum)
      }
    },
  },
  mounted() {
    this.axios.get('/api/getUsers').then((response) => {
      this.datum = response.data['data']
      this.copyOfDatum = response.data['data']
      console.log(response.data['data'])
    })

  }
}
</script>

<template>
  <nav class="flex flex-row gap-2 items-center justify-between">
    <Dropdown @dropdownEvent="dropdownEvent" title="مرتب سازی" :options="['جدیدترین کاربر', 'قدیمی ترین کاربر', 'حروف الفبا', 'حروف الفبا برعکس']"></Dropdown>
    <search-input @serachInput="filterBasedOnColumn" placeholder="جستوجو" :filterOptions="['نام و نام خانوادگی', 'یوزرنیم']"></search-input>
  </nav>
  <Table>
    <template v-slot:head>
      <template v-for="head in heads">
        <th scope="col" class="px-6 py-3">
          {{ head }}
        </th>
      </template>
    </template>
    <template v-slot:body>
      <template v-for="row in datum">
        <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
            <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
                <img class="w-10 h-10 rounded-full" :src="row['picture']" alt="">
                <div class="ps-3">
                    <div class="text-base font-semibold">{{ row['profile']['name'] }}</div>
                    <div class="font-normal text-gray-500">{{ row['profile']['username'] }}</div>
                </div>
            </th>
            <td class="px-6 py-4">
                {{ row['fullName'] }}
            </td>
            <td class="px-6 py-4">
              {{ row['userId'] }}
            </td>
            <td class="px-6 py-4">
                <a @click="editUser(row['id'])" href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">پنل کاربر</a>
            </td>
        </tr>
      </template>
    </template>
  </Table>
</template>