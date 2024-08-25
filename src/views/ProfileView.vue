<script>
import {FwbButton} from "flowbite-vue";
import Input from "@/components/input.vue";
import Dropdown from "@/components/Dropdown.vue";
import Button from "@/components/button.vue";
import Modal from "@/components/Modal.vue";
import Table from "@/components/table.vue";
import {useToast} from "vue-toastification";
import ProfilePicture from "@/components/ProfilePicture.vue";

export default {
  name: "ProfileView",
  components: {ProfilePicture, Table, Modal, Button, Dropdown, Input, FwbButton},
  data(){
    return {
      datum: [],
      prevPageRoute: '',
      friendsDatum: [],
      lotteryDatum: [],
      messagesDatum: [],
      winningDatum: [],
      sendMessageParam: {
        text: '',
        image: null
      },
      userUnReadMessages: {
        count: 0,
        status: false
      },
    }
  },
  mounted() {
    const paramValue = this.$route.query; // Replace 'yourParam' with the actual query parameter key
    this.prevPageRoute = paramValue.route
    const params = {
      "id": paramValue.id,
    };
    this.axios.get('/api/loadProfile',{params: params}).then((response) => {
      this.datum = response.data['data'][0]
      this.unReadMessages()
    })
  },
  methods: {
    modalHandlerSendMessage(event){
      if (event==true){}
    },
    recordChanges(){
      const params = {
        "id": this.datum['id'],
        "enter_id": this.datum['enter_id'],
        "enter_name": this.datum['enter_name'],
        "referral_code": this.datum['referral_code'],
      };
      this.axios.get('/api/recordChangesOfProfile',{params: params}).then((response) => {
          // Get toast interface
          const toast = useToast();
          toast.success('.اطلاعات کاربر با موفقیت ویرایش شد'); // Display error toast notification
      })
    },
    deleteProfile(){
      const params = {
        "id": this.datum['id'],
      };
      this.axios.get('/api/deleteProfile',{params: params}).then((response) => {
          // Get toast interface
          const toast = useToast();
          toast.success('.کاربر با موفقیت حدف شد'); // Display error toast notification
      })
    },
    modalHandler(event){
      if (event==true){
        this.friendsHeads=['پروفایل','نام و نام خانوادگی','یوزرنیم', 'ایدی عددی', 'اکشن']
        const params = {
          "id": this.datum['id'],
        };
        this.axios.get('/api/loadProfileFriends',{params: params}).then((response) => {
          this.friendsDatum = response.data['data']
          console.log(this.friendsDatum)
        })
      }
    },
    modalHandlerLotteryProfile(event){
      if (event==true){
        this.lotteryHeads=['تاریخ ثبت نام','بازی انتخاب شده','دوستان انتخاب شده', 'کد بلیط', 'عکس فیش پرداخت', 'وضعیت پرداخت', 'تایید پرداخت', 'وضعیت برد', 'انتخاب به عنوان برنده']
        const params = {
          "id": this.datum['id'],
        };
        this.axios.get('/api/modalHandlerLotteryProfile',{params: params}).then((response) => {
          this.lotteryDatum = response.data['data']
        })
      }
    },
    selectToWin(id){
        const params = {
          "lottery_id": id,
        };
        this.axios.get('/api/selectToWin',{params: params}).then((response) => {
          this.messagesDatum = response.data['data']
          const toast = useToast();
          toast.success("یوزر مورد نظر به عنوان برنده تعیین شد.");
        })
    },
    sendTicket(id){
        const params = {
          "lottery_id": id,
        };
        this.axios.get('/api/sendTicket',{params: params}).then((response) => {
          this.messagesDatum = response.data['data']
          const toast = useToast();
          toast.success("پرداخت تایید و بلیط با موفقیت ارسال شد.");
        })
    },
    modalHandlerMessages(event){
      if (event==true){
        this.messagesHeads=['سوال کاربر','جواب ادمین','حذف پیام', 'بستن تیکت']
        const params = {
          "id": this.datum['id'],
        };
        this.axios.get('/api/loadMessagesyHistoryOfProfile',{params: params}).then((response) => {
          this.messagesDatum = response.data['data']
          // console.log('message data:', this.messagesDatum)
        })
      }
    },
    deleteMessage(id){
        const params = {
          "id": id,
        };
        this.axios.get('/api/deleteMessage',{params: params}).then((response) => {
          const index = this.messagesDatum.findIndex(item => item.id === id);
          if (index > -1) {
            this.messagesDatum.splice(index, 1);
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
    modalHandlerWinning(event){
      if (event==true){
        this.winningHeads=['تاریخ ثبت نام','بازی انتخاب شده','دوستان انتخاب شده', 'کد بلیط', 'وضعیت پرداخت', 'وضعیت برد', 'پیام به برنده']
        const params = {
          "id": this.datum['id'],
        };
        this.axios.get('/api/modalHandlerLotteryWinningProfile',{params: params}).then((response) => {
          this.winningDatum = response.data['data']
          console.log(this.winningDatum)
        })
      }
    },
    editUser(id){
      this.$router.replace({ path: '/Profile', query: { id: id, route: '/'} }).then(()=>{
        location.reload();
      });
    },
    onFilePicked (event) {
      const files = event.target.files
      // Send the image file to the server
      const image = new FormData();
      image.append("image", files[0]); // Add image to form data
      this.sendMessageParam.image = image
    },
    sendMessage(row){
        const id = row['id']
        this.messagesDatum.forEach(r=>{
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
    sendMessageToWinner(row){
        const id = row['profile_id']
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
        this.winningDatum.forEach(r=>{
          if (r == row){
            r['answer']=this.sendMessageParam.text
            r['answer_picture']=this.sendMessageParam.image
          }
        })
    },
    openImageInNewWindow(imageUrl) {
      window.open(imageUrl, '_blank');
    },
    unReadMessages(){
      const params = {
        "id": this.datum['id'],
      };
      console.log(params)
      this.axios.get('/api/unReadMessages', {params: params}).then((response) => {
        if(response) {
          console.log(response.data)
          this.userUnReadMessages.count = response.data['data']['count']
          console.log(response.data['data']['count'], typeof response.data['data']['count'])
          if (this.userUnReadMessages.count != 0) {
            this.userUnReadMessages.status = true
          }
        }
      })
    },
  },
}
</script>

<template>
  <button
    @click="$emit('sidebarOpen', false)"
    type="button"
    class="bottom-10 left-5 bg-blue-500 font-sans text-white hover:bg-gray-200 rounded-full text-sm w-8 h-8 ms-auto inline-flex justify-center items-center absolute left-0 mx-2">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-menu-button" viewBox="0 0 16 16">
      <path d="M0 1.5A1.5 1.5 0 0 1 1.5 0h8A1.5 1.5 0 0 1 11 1.5v2A1.5 1.5 0 0 1 9.5 5h-8A1.5 1.5 0 0 1 0 3.5zM1.5 1a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5z"/>
      <path d="m7.823 2.823-.396-.396A.25.25 0 0 1 7.604 2h.792a.25.25 0 0 1 .177.427l-.396.396a.25.25 0 0 1-.354 0M0 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm1 3v2a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2zm14-1V8a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v2zM2 8.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0 4a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5"/>
    </svg>
    <span class="sr-only">open menu</span>
  </button>
  <div class="bg-white rounded-lg px-4 py-2  mx-auto flex flex-col gap-2 items-center justify-between">
    <div class="flex flex-col gap-2 py-6">
      <div class="flex flex-col gap-2">
        <Input @update="datum['enter_name']=$event" title="نام و نام خانوادگی" :value="datum['enter_name']" class="w-64"  />
        <Input @update="datum['enter_id']=$event" title="یورنیم" :value="datum['enter_id']" class="w-64" />
        <Input title="آیدی عددی" :value="datum['user_id']" class="w-64" disabled/>
      </div>
      <hr class="h-px my-8 bg-gray-200 border-0 dark:bg-gray-700">
      <div class="flex flex-col items-center col-span-2 gap-2 ">
        <div class="w-48">
        <Modal @modalOpened='modalHandler' btn-title="دوستان" modal-title="لیست دوستان">
          <template v-slot:modalBody>
            <Table>
                <template v-slot:head>
                  <template v-for="head in friendsHeads">
                    <th scope="col" class="px-6 py-3">
                      {{ head }}
                    </th>
                  </template>
                </template>
                <template v-slot:body>
                  <template v-for="row in friendsDatum">
                    <tr class="text-nowrap bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                        <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
<!--                            <img class="w-10 h-10 rounded-full" :src="row['picture']">-->
                            <ProfilePicture :username="row['enter_id']" :src="row['picture']"></ProfilePicture>
                            <div class="ps-3">
                                <div class="text-base font-semibold">{{ row['full_name'] }}</div>
                                <div class="font-normal text-gray-500">{{ row['username'] }}</div>
                            </div>
                        </th>
                        <td class="px-6 py-4">
                            {{ row['enter_name'] }}
                        </td>
                        <td class="px-6 py-4">
                          {{ row['enter_id'] }}
                        </td>
                        <td class="px-6 py-4">
                          {{ row['user_id'] }}
                        </td>
                        <td class="px-6 py-4">
                            <a @click="editUser(row['id'])" href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">پنل کاربر</a>
                        </td>
                    </tr>
                  </template>
                </template>
              </Table>
          </template>
        </Modal>
      </div>
        <div class="w-48">
          <Modal @modalOpened='modalHandlerLotteryProfile' btn-title="قرعه کشی" modal-title="لیست قرعه کشی های شرکت کرده">
            <template v-slot:modalBody>
              <Table>
                  <template v-slot:head>
                    <template v-for="head in lotteryHeads">
                      <th scope="col" class="px-6 py-3">
                        {{ head }}
                      </th>
                    </template>
                  </template>
                  <template v-slot:body>
                    <template v-for="row in lotteryDatum">
                      <tr class="text-nowrap bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                          <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
                              {{ row['register_date'] }}
                          </th>
                          <td class="px-6 py-4">
                              {{ row['game'] }}
                          </td>
                          <td class="px-6 py-4">
                            <template v-for="f in row['friends']">
                              <a @click="editUser(f['id'])" href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">
                                {{ f['enter_name'] }}
                              </a>,
                            </template>
                          </td>
                          <td class="px-6 py-4">
                            {{ row['ticket'] }}
                          </td>
                          <td class="px-6 py-4">
                            <img class="object-cover w-10 h-10  rounded-t-lg md:rounded-none md:rounded-s-lg" :src="row['payment_picture']" alt=""  @click="openImageInNewWindow(row['payment_picture'])">
                          </td>
                          <td class="px-6 py-4">
                            {{ row['payment_status'] }}
                          </td>
                          <td class="px-6 py-4">
                            <template v-if="row['payment_status']=='PENDING'">
                              <a @click="sendTicket(row['id'])" href="#" class="font-medium text-green-600 dark:text-blue-500 hover:underline">
                                تایید و ارسال بلیط
                              </a>
                            </template>
                            <template v-else>تایید شده</template>
                          </td>
                          <td class="px-6 py-4">
                            <p v-if="row['winning']==true">برده</p>
                            <p v-if="row['winning']==false">نبرده</p>
                          </td>
                          <td class="px-6 py-4">
                            <fwb-button @click="selectToWin(row['id'])">برنده شود</fwb-button>
                          </td>
                      </tr>
                    </template>
                  </template>
                </Table>
              </template>
          </Modal>
        </div>
        <div class="w-48 relative inline-flex">
          <Modal @modalOpened='modalHandlerMessages' btn-title="پیام ها" :modal-title="'لیست پیام های کاربر: '+userUnReadMessages.count+'تیکت باز وجود دارد.'">
            <template v-slot:modalBody>
              <Table>
                  <template v-slot:head>
                    <template v-for="head in messagesHeads">
                      <th scope="col" class="px-6 py-3">
                        {{ head }}
                      </th>
                    </template>
                  </template>
                  <template v-slot:body>
                    <template v-for="row in messagesDatum">
                      <tr class="text-nowrap bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
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
                                           <div class="w-[450px] mb-4 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600">
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
          </Modal>
          <template v-if="userUnReadMessages.status">
            <span class="flex absolute h-4 w-4 top-0 right-0 -mt-1 -mr-1">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-4 w-4 bg-rose-500">
              </span>
            </span>
          </template>
        </div>
        <div class="w-48">
        <Modal @modalOpened='modalHandlerWinning' btn-title="برنده شدن ها" modal-title="لیست تعداد دفعات برنده شده">
          <template v-slot:modalBody>
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
                    <tr class="text-nowrap bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                        <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
                            {{ row['register_date'] }}
                        </th>
                        <td class="px-6 py-4">
                            {{ row['game'] }}
                        </td>
                        <td class="px-6 py-4">
                          <template v-for="f in row['friends']">
                            <a @click="editUser(f['id'])" href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">
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
                          <p v-if="row['winning']==true">برده</p>
                          <p v-if="row['winning']==false">نبرده</p>
                        </td>
                        <td class="px-6 py-4">
                            <Modal @modalOpened='modalHandlerSendMessage' btn-title="پیام" modal-title="ارسال پیام به کاربر">
                                    <template v-slot:modalBody>
                                      <form>
                                         <div class="w-[450px] mb-4 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600">
                                             <div class="px-4 py-2 bg-white rounded-t-lg dark:bg-gray-800">
                                                 <label for="comment" class="sr-only">پیام خود را برای کاربر بنویسید</label>
                                                 <textarea v-model="sendMessageParam.text" id="comment" rows="4" class="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400" placeholder="پیام خود را برای کاربر بنویسید..." required ></textarea>
                                             </div>
                                             <div class="flex items-center justify-between px-3 py-2 border-t dark:border-gray-600">
                                                 <div class="w-45">
                                                   <Button @click="sendMessageToWinner(row)">
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
                        </td>
                    </tr>
                  </template>
                </template>
            </Table>
          </template>
        </Modal>
      </div>
      </div>
      <hr class="h-px my-8 bg-gray-200 border-0 dark:bg-gray-700">
      <div class="flex flex-row gap-2 ">
  <!--      <Button @click="deleteProfile" class="bg-red-600 hover:bg-red-800 focus:ring-red-300"><template v-slot:title>حذف کاربر</template></Button>-->
        <fwb-button @click="deleteProfile" class="font-sans text-nowrap bg-red-600 hover:bg-red-800 focus:ring-red-300">حذف کاربر</fwb-button>
  <!--      <Button @click="recordChanges" class="truncate bg-green-600 hover:bg-green-800 focus:ring-green-300"><template v-slot:title>ثبت تغییرات</template></Button>-->
        <fwb-button @click="recordChanges" class="font-sans text-nowrap bg-green-600 hover:bg-green-800 focus:ring-green-300">ثبت تغییرات</fwb-button>
        <router-link :to="prevPageRoute" >
          <fwb-button>
            <div class="flex flex-row gap-2 font-sans">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-bar-right" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M6 8a.5.5 0 0 0 .5.5h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L12.293 7.5H6.5A.5.5 0 0 0 6 8m-2.5 7a.5.5 0 0 1-.5-.5v-13a.5.5 0 0 1 1 0v13a.5.5 0 0 1-.5.5"/>
              </svg>
              <span>بازگشت</span>
            </div>
        </fwb-button></router-link>
      </div>
    </div>

  </div>
</template>
