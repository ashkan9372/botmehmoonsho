<script>
// @ is an alias to /src
import Table from "@/components/table.vue";
import SearchInput from "@/components/searchInput.vue";
import Button from "@/components/button.vue";
import Dropdown from "@/components/Dropdown.vue";
import ProfilePicture from "@/components/ProfilePicture.vue";

export default {
  name: 'UsersView',
  components: {
    ProfilePicture,
    Dropdown,
    Button,
    SearchInput,
    Table,
  },
  data() {
    return {
      heads: ['پروفایل', 'نام و نام خانوادگی', 'یوزرنیم', 'اکشن'],
      datum: [],
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
  <nav class="flex sm:flex-row flex-col gap-2 sm:items-center justify-between">
    <div class="flex flex-row gap-2 items-center justify-between">
      <Button @click="$emit('sidebarOpen', false)">
        <template v-slot:title>
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-menu-button" viewBox="0 0 16 16">
            <path d="M0 1.5A1.5 1.5 0 0 1 1.5 0h8A1.5 1.5 0 0 1 11 1.5v2A1.5 1.5 0 0 1 9.5 5h-8A1.5 1.5 0 0 1 0 3.5zM1.5 1a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5z"/>
            <path d="m7.823 2.823-.396-.396A.25.25 0 0 1 7.604 2h.792a.25.25 0 0 1 .177.427l-.396.396a.25.25 0 0 1-.354 0M0 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm1 3v2a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2zm14-1V8a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v2zM2 8.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0 4a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5"/>
          </svg>
          <span class="sr-only">open menu</span>
        </template>
      </Button>
      <Dropdown @dropdownEvent="dropdownEvent" title="مرتب سازی" :options="['جدیدترین کاربر', 'قدیمی ترین کاربر', 'حروف الفبا', 'حروف الفبا برعکس']"></Dropdown>
    </div>
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
        <tr class="text-nowrap bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
            <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
                <ProfilePicture :username="row['userId']" :src="row['picture']"></ProfilePicture>
<!--                <img class="w-10 h-10 rounded-full" :src="row['picture']" alt="">-->
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