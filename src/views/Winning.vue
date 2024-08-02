<script>
import Table from "@/components/table.vue";
import Modal from "@/components/Modal.vue";
import Button from "@/components/button.vue";
import SearchInput from "@/components/searchInput.vue";
import Dropdown from "@/components/Dropdown.vue";
import {useToast} from "vue-toastification";
import Input from "@/components/input.vue";

export default {
  name: "Winning",
  components: {Input, Dropdown, SearchInput, Button, Modal, Table},
  data(){
    return {
      winningDatum: [],
      copyOfDatum: [],
      winningHeads: ['تاریخ ثبت نام','نام و نام خانوادگی', 'یوزرنیم', 'بازی انتخاب شده','دوستان انتخاب شده', 'کد بلیط', 'وضعیت پرداخت', 'پیام به برنده'],
      sendMessageParam: {
        text: '',
        image: null
      },
    }
  },
  mounted() {
    this.axios.get('/api/modalHandlerLotteryWinning').then((response) => {
      this.winningDatum = response.data['data']
      this.copyOfDatum = response.data['data']
      console.log(this.winningDatum)
    })
  },
  methods:{
    onFilePicked (event) {
      const files = event.target.files
      // Send the image file to the server
      const image = new FormData();
      image.append("image", files[0]); // Add image to form data
      this.sendMessageParam.image = image
    },
    sendMessage(id){
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
    sendMessageToWinner(id){
        const params = {
          "message_id": id,
          "message": this.sendMessageParam.text,
        };
        if (this.sendMessageParam.image){
          this.axios.post('/api/sendMessageWithImageToWinner', this.sendMessageParam.image, {
            headers: {
              'Content-Type': 'multipart/form-data' // Set content type for image upload
            },
            params: params
          }).then((response) => {
            const toast = useToast();
            toast.success("پیام شما با موفقیت ارسال شد.");
          })
        } else {
          this.axios.get('/api/sendMessageToWinner',{params: params}).then((response) => {
            const toast = useToast();
            toast.success("پیام شما با موفقیت ارسال شد.");
          })
        }
    },
    filterBasedOnColumn(event) {
      console.log(event)
      let filter = event['filter']
      let searchTerm = event['input']
      if (searchTerm == ''){
        this.winningDatum = this.copyOfDatum
      } else {
        this.winningDatum = this.winningDatum.filter(item => {
          const searchText = searchTerm.toLowerCase();
          // Search fullName using includes
          if (filter == 'نام و نام خانوادگی'){
            return item.enter_name.toLowerCase().includes(searchText);
          }
          if (filter == 'یوزرنیم'){
            return item.enter_id.toLowerCase().includes(searchText);
          }
        });
      }
    },

    sortBasedOnNewUser(){
      this.winningDatum.sort((a, b) => {
        // Sort by ID first (ascending)
        if (a.id < b.id) return -1;
        if (a.id > b.id) return 1;
        return 0; // No further sorting needed if no invest field or IDs are equal
      });
    },
    sortBasedOnOldUser(){
      this.winningDatum.sort((a, b) => {
        // Sort by ID first (ascending)
        if (a.id > b.id) return -1;
        if (a.id < b.id) return 1;
        return 0; // No further sorting needed if no invest field or IDs are equal
      });
    },
    sortLotteryBasedOnHighest(action){
      const params = {
        "action": action,
      };
      this.axios.get('/api/sortLotteryBasedOnHighest', {params: params}).then((response) => {
        this.winningDatum = response.data['data']
      })
    },
    dropdownEvent(event){
      console.log(event[0]);
      if (event[0]=="جدیدترین"){
        this.sortBasedOnNewUser()
      }
      if (event[0]=="قدیمی ترین"){
        this.sortBasedOnOldUser()
      }
      if (event[0]=="یورنیم با بیشترین برد"){
        this.sortLotteryBasedOnHighest('profile')
      }
      if (event[0]=="بیشترین بازی انتخاب شده"){
        this.sortLotteryBasedOnHighest('game')
      }
      if (event[0]=="دوستان انتخاب شده بابیشترین برد"){
        this.sortLotteryBasedOnHighest('friends')
      }
    },
  }
}
</script>

<template>
  <nav class="flex flex-row gap-2 items-center justify-between">
    <Dropdown @dropdownEvent="dropdownEvent" title="مرتب سازی" :options="['جدیدترین', 'قدیمی ترین', 'یورنیم با بیشترین برد', 'دوستان انتخاب شده بابیشترین برد', 'بیشترین بازی انتخاب شده']"></Dropdown>
    <search-input @serachInput="filterBasedOnColumn" placeholder="جستوجو" :filterOptions="['نام و نام خانوادگی', 'یوزرنیم']"></search-input>
  </nav>
  <Table>
    <template v-slot:head>
      <template v-for="head in winningHeads">
        <th scope="col" class="px-6 py-3">
          {{ head }}
        </th>
      </template>
    </template>
    <template v-slot:body>
      <template v-for="row in winningDatum">
        <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
            <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
                {{ row['register_date'] }}
            </th>
            <td class="px-6 py-4">
                {{ row['enter_name'] }}
            </td>
            <td class="px-6 py-4">
                {{ row['enter_id'] }}
            </td>
            <td class="px-6 py-4">
                {{ row['game'] }}
            </td>
            <td class="px-6 py-4">
              <template v-for="f in row['friends']">
                <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">
                  {{ f['enter_name'] }}
                </a>,
              </template>
            </td>
            <td class="px-6 py-4">
              {{ row['ticket'] }}
            </td>
            <td class="px-6 py-4">
              {{ row['payment_status'] }}
            </td>
            <td class="px-6 py-4">
                <div class="w-14">
                  <!--  send message to user  -->
                    <Modal btn-title="پیام" modal-title="ارسال پیام به کاربر">
                                  <template v-slot:modalBody>
                                    <form>
                                       <div class="w-[450px] mb-4 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600">
                                           <div class="px-4 py-2 bg-white rounded-t-lg dark:bg-gray-800">
                                               <label for="comment" class="sr-only">پیام خود را برای کاربر بنویسید</label>
                                               <textarea v-model="sendMessageParam.text" id="comment" rows="4" class="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400" placeholder="پیام خود را برای کاربر بنویسید..." required ></textarea>
                                           </div>
                                           <div class="flex items-center justify-between px-3 py-2 border-t dark:border-gray-600">
                                               <div class="w-45">
                                                 <Button @click="sendMessageToWinner(row['profile_id'])">
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
            </td>
        </tr>
      </template>
    </template>
  </Table>
</template>
