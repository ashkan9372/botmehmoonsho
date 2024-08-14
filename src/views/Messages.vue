<script>
import Table from "@/components/table.vue";
import Dropdown from "@/components/Dropdown.vue";
import SearchInput from "@/components/searchInput.vue";
import {useToast} from "vue-toastification";
import Button from "@/components/button.vue";
import Modal from "@/components/Modal.vue";

export default {
  name: "Messages",
  components: {Modal, Button, SearchInput, Dropdown, Table},
  data() {
    return {
      heads: ['نام و نام خانوادگی', 'یوزرنیم', 'سوال کاربر', 'جواب ادمین', 'حذف', 'بستن'],
      datum: [],
      sendMessageParam: {
        text: '',
        image: null
      },

    }
  },
  methods: {
    onFilePicked (event) {
      const files = event.target.files
      // Send the image file to the server
      const image = new FormData();
      image.append("image", files[0]); // Add image to form data
      this.sendMessageParam.image = image
    },
    editUser(id){
      this.$router.push({ path: '/Profile', query: { id: id} });
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
            return item.sender_profile.enter_name.toLowerCase().includes(searchText);
          }
          if (filter == 'یوزرنیم'){
            return item.sender_profile.enter_id.toLowerCase().includes(searchText);
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
    deleteMessage(id){
        const params = {
          "id": id,
        };
        this.axios.get('/api/deleteMessage',{params: params}).then((response) => {
          const index = this.datum.findIndex(item => item.id === id);
          if (index > -1) {
            this.datum.splice(index, 1);
          }
          // Get toast interface
          const toast = useToast();
          toast.success('.پیام کاربر با موفقیت حدف شد'); // Display error toast notification
        })

    },
    closeMessage(id){
        const params = {
          "id": id,
        };
        this.axios.get('/api/closeMessage',{params: params}).then((response) => {
          // Get toast interface
          const toast = useToast();
          toast.success('.تیکت با موفقیت بسته شد'); // Display error toast notification
        })
    },
    sendMessage(row){
        const id = row['id']
        this.datum.forEach(r=>{
          if (r == row){
            r['answer']=this.sendMessageParam.text
            r['answer_picture']=this.sendMessageParam.image
          }
        })
        const params = {
          "message_id": id,
          "message": this.sendMessageParam.text,
        };
        if (this.sendMessageParam.image){
          this.axios.post('/api/sendMessageWithImage', this.sendMessageParam.image, {
            headers: {
              'Content-Type': 'multipart/form-data' // Set content type for image upload
            },
            params: params
          }).then((response) => {
            const toast = useToast();
            toast.success("پیام شما با موفقیت ارسال شد.");
          })
        } else {
          this.axios.get('/api/sendMessage',{params: params}).then((response) => {
            const toast = useToast();
            toast.success("پیام شما با موفقیت ارسال شد.");
          })
        }
    },
    openImageInNewWindow(imageUrl) {
      window.open(imageUrl, '_blank');
    }
  },
  mounted() {
    this.axios.get('/api/loadMessagesyHistory').then((response) => {
      this.datum = response.data['data']
      this.copyOfDatum = response.data['data']
      // console.log(this.datum)
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
      <Dropdown @dropdownEvent="dropdownEvent" title="مرتب سازی" :options="['جدیدترین پیام', 'قدیمی ترین پیام']"></Dropdown>
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
        <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
            <th class="px-6 py-4 max-w-[400px]">
                {{ row['sender_profile']['enter_name'] }}
            </th>
            <td class="px-6 py-4 max-w-[400px]">
                {{ row['sender_profile']['enter_id'] }}
            </td>
            <th class="px-6 py-4 max-w-[400px] ">
              <template v-if="row['sender_picture']">
                <div class="flex flex-row items-start gap-2">
                  <img class="object-cover w-10 h-10  rounded-t-lg md:rounded-none md:rounded-s-lg" :src="row['sender_picture']" alt=""  @click="openImageInNewWindow(row['sender_picture'])">
                  <p class=" font-normal text-gray-700 dark:text-gray-400 leading-normal">
                    {{ row['message'] }}
                  </p>

                </div>
              </template>
              <template v-else>
                <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
                  {{ row['message'] }}
                </p>
              </template>
            </th>
            <td class="px-6 py-4 max-w-[400px]">
                <template v-if="row['answer'] == null ">
                  <div class="w-14">
                    <!--  send message to user  -->
                      <Modal @modalOpened='modalHandlerSendMessage' btn-title="پیام" modal-title="ارسال پیام به کاربر">
                        <template v-slot:modalBody>
                          <form>
                             <div class="md:w-[450px] mb-4 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600">
                                 <div class="px-4 py-2 bg-white rounded-t-lg dark:bg-gray-800">
                                     <label for="comment" class="sr-only">پیام خود را برای کاربر بنویسید</label>
                                     <textarea v-model="sendMessageParam.text" id="comment" rows="4" class="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400" placeholder="پیام خود را برای کاربر بنویسید..." required ></textarea>
                                 </div>
                                 <div class="flex items-center justify-between px-3 py-2 border-t dark:border-gray-600">
                                     <div class="w-45">
                                       <Button @click="sendMessage(row)">
                                         <template v-slot:title>
                                           <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope" viewBox="0 0 16 16">
                                             <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1zm13 2.383-4.708 2.825L15 11.105zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741M1 11.105l4.708-2.897L1 5.383z"/>
                                           </svg>
                                           <span>ارسال پیام</span>
                                         </template>
                                       </Button>
                                     </div>
                                     <div class="flex ps-0 space-x-1 rtl:space-x-reverse sm:ps-2">
                                         <button
                                             @click="$refs.fileInput[0].click()"
                                             type="button" class="inline-flex justify-center items-center p-2 text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600">
                                             <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                                                <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                                             </svg>
                                             <span class="sr-only">Upload image</span>
                                         </button>
                                          <input
                                            type="file"
                                            ref="fileInput"
                                            accept="image/*"
                                            @change="onFilePicked"
                                            class="hidden"
                                          />
                                     </div>
                                 </div>
                             </div>
                          </form>
                        </template>
                      </Modal>
                  </div>
                </template>
                <template v-else>
                  <template v-if="row['answer_picture']">
                    <div class="flex flex-row items-start gap-2">
                      <img class="object-cover w-10 h-10  rounded-t-lg md:rounded-none md:rounded-s-lg" :src="row['answer_picture']" alt=""  @click="openImageInNewWindow(row['answer_picture'])">
                      <p class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-normal">
                        {{ row['answer'] }}
                      </p>
                    </div>
                  </template>
                  <template v-else>
                    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
                      {{ row['answer'] }}
                    </p>
                  </template>
                </template>
            </td>

            <td class="px-6 py-4">
                <a @click="deleteMessage(row['id'])" href="#" class="font-medium text-red-600 dark:text-red-500 hover:underline">حذف</a>
            </td>
            <td class="px-6 py-4">
                <a @click="closeMessage(row['id'])" href="#" class="font-medium text-green-600 dark:text-green-500 hover:underline">بستن</a>
            </td>

        </tr>
      </template>
    </template>
  </Table>
</template>

