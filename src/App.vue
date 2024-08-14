<template>
    <main class="flex flex-grow overflow-auto bg-gray-100 h-screen">
        <transition name="slide-fade">
<!--          max-sm:hidden -->
        <aside :class="[isMenuHidden? 'hidden':'']" class="flex flex-col justify-between font-sans fixed top-0 right-0 z-40 sm:w-64 h-screen py-4 text-md font-medium text-gray-900 bg-white border border-gray-200">
          <button @click="isMenuHidden=!isMenuHidden" type="button"
                  class="font-sans text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center absolute left-0 mx-2">
              <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
              </svg>
              <span class="sr-only">Close modal</span>
          </button>
          <div>
            <router-link to="/" class="flex flex-row gap-4 items-center block w-full px-4 py-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-people" viewBox="0 0 16 16">
                  <path d="M15 14s1 0 1-1-1-4-5-4-5 3-5 4 1 1 1 1zm-7.978-1L7 12.996c.001-.264.167-1.03.76-1.72C8.312 10.629 9.282 10 11 10c1.717 0 2.687.63 3.24 1.276.593.69.758 1.457.76 1.72l-.008.002-.014.002zM11 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4m3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0M6.936 9.28a6 6 0 0 0-1.23-.247A7 7 0 0 0 5 9c-4 0-5 3-5 4q0 1 1 1h4.216A2.24 2.24 0 0 1 5 13c0-1.01.377-2.042 1.09-2.904.243-.294.526-.569.846-.816M4.92 10A5.5 5.5 0 0 0 4 13H1c0-.26.164-1.03.76-1.724.545-.636 1.492-1.256 3.16-1.275ZM1.5 5.5a3 3 0 1 1 6 0 3 3 0 0 1-6 0m3-2a2 2 0 1 0 0 4 2 2 0 0 0 0-4"/>
                </svg>
                <span>کاربرها</span>
            </router-link>
            <router-link to="/Messages" class="flex flex-row gap-4 items-center justify-between block w-full px-4 py-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700">
                <div class="flex flex-row gap-4 items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope" viewBox="0 0 16 16">
                  <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1zm13 2.383-4.708 2.825L15 11.105zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741M1 11.105l4.708-2.897L1 5.383z"/>
                </svg>
                <span>پیام های پشتیبانی</span>
                </div>
                <template v-if="userUnReadMessages.status">
                  <span class="flex">
                    <span class="animate-ping absolute inline-flex w-6 h-6 rounded-full bg-sky-400 opacity-85"></span>
                    <div class="inline-flex items-center justify-center w-6 h-6 text-xs font-bold text-white bg-sky-500 border-2 border-white rounded-full -top-2 -end-2 dark:border-gray-900">
                      {{ userUnReadMessages.count }}
                    </div>
                  </span>
                </template>
              </router-link>
            <router-link to="/Winning" class="flex flex-row gap-4 items-center block w-full px-4 py-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trophy" viewBox="0 0 16 16">
                <path d="M2.5.5A.5.5 0 0 1 3 0h10a.5.5 0 0 1 .5.5q0 .807-.034 1.536a3 3 0 1 1-1.133 5.89c-.79 1.865-1.878 2.777-2.833 3.011v2.173l1.425.356c.194.048.377.135.537.255L13.3 15.1a.5.5 0 0 1-.3.9H3a.5.5 0 0 1-.3-.9l1.838-1.379c.16-.12.343-.207.537-.255L6.5 13.11v-2.173c-.955-.234-2.043-1.146-2.833-3.012a3 3 0 1 1-1.132-5.89A33 33 0 0 1 2.5.5m.099 2.54a2 2 0 0 0 .72 3.935c-.333-1.05-.588-2.346-.72-3.935m10.083 3.935a2 2 0 0 0 .72-3.935c-.133 1.59-.388 2.885-.72 3.935M3.504 1q.01.775.056 1.469c.13 2.028.457 3.546.87 4.667C5.294 9.48 6.484 10 7 10a.5.5 0 0 1 .5.5v2.61a1 1 0 0 1-.757.97l-1.426.356a.5.5 0 0 0-.179.085L4.5 15h7l-.638-.479a.5.5 0 0 0-.18-.085l-1.425-.356a1 1 0 0 1-.757-.97V10.5A.5.5 0 0 1 9 10c.516 0 1.706-.52 2.57-2.864.413-1.12.74-2.64.87-4.667q.045-.694.056-1.469z"/>
              </svg>
              <span>برنده ها</span>
            </router-link>
            <router-link to="/Payments" class="flex flex-row gap-4 items-center justify-between block w-full px-4 py-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700">
              <div class="flex flex-row gap-4 items-center ">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cash-coin" viewBox="0 0 16 16">
                  <path fill-rule="evenodd" d="M11 15a4 4 0 1 0 0-8 4 4 0 0 0 0 8m5-4a5 5 0 1 1-10 0 5 5 0 0 1 10 0"/>
                  <path d="M9.438 11.944c.047.596.518 1.06 1.363 1.116v.44h.375v-.443c.875-.061 1.386-.529 1.386-1.207 0-.618-.39-.936-1.09-1.1l-.296-.07v-1.2c.376.043.614.248.671.532h.658c-.047-.575-.54-1.024-1.329-1.073V8.5h-.375v.45c-.747.073-1.255.522-1.255 1.158 0 .562.378.92 1.007 1.066l.248.061v1.272c-.384-.058-.639-.27-.696-.563h-.668zm1.36-1.354c-.369-.085-.569-.26-.569-.522 0-.294.216-.514.572-.578v1.1zm.432.746c.449.104.655.272.655.569 0 .339-.257.571-.709.614v-1.195z"/>
                  <path d="M1 0a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h4.083q.088-.517.258-1H3a2 2 0 0 0-2-2V3a2 2 0 0 0 2-2h10a2 2 0 0 0 2 2v3.528c.38.34.717.728 1 1.154V1a1 1 0 0 0-1-1z"/>
                  <path d="M9.998 5.083 10 5a2 2 0 1 0-3.132 1.65 6 6 0 0 1 3.13-1.567"/>
                </svg>
                <span>پرداخت ها</span>
              </div>
              <template v-if="userNewPayments.status">
                <span class="flex">
                  <span class="animate-ping absolute inline-flex w-6 h-6 rounded-full bg-green-400 opacity-85"></span>
                  <div class="inline-flex items-center justify-center w-6 h-6 text-xs font-bold text-white bg-green-400 border-2 border-white rounded-full -top-2 -end-2 dark:border-gray-900">
                    {{ userNewPayments.count }}
                  </div>
                </span>
              </template>
            </router-link>
            <router-link to="/Settings" class="flex flex-row gap-4 items-center block w-full px-4 py-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear" viewBox="0 0 16 16">
                  <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0"/>
                  <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115z"/>
                </svg>
                <span>تنظیمات</span>
              </router-link>
          </div>
          <div class="flex flex-row justify-between">
            <button @click="Logout" class="flex flex-row gap-4 items-center justify-center block text-red-600 w-full px-4 py-2 border-b border-e border-t border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-red-700">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-right" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z"/>
                <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z"/>
              </svg>
              <span>خروج</span>
            </button>
            <button @click="onToggle" class="truncate flex flex-row justify-center items-center  w-full text-sky-600 px-4 py-2 border-b border-t border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                  <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                </svg>
                <span>پیام همگانی</span>
            </button>
            <!-- Render inside our `<div id="modals"></div>` in index.html -->
            <Teleport to="body">
              <transition name="fade">
              <!-- Show / hide the modal -->
              <div :class="[isModalVisible? '': 'hidden']">
                <!-- The backdrop -->
                <div @click="onToggle" class="fixed inset-0 bg-gray-900 opacity-40"></div>

                <!-- Where the actual content goes -->
                <div class="fixed inset-0 flex items-center justify-center">
                  <div class="flex flex-col  max-h-[600px] bg-white rounded-lg shadow dark:bg-gray-700">
                        <!-- Modal header -->
                        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                            <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                                ارسال پیام به همه کاربر ها
                            </h3>
                            <button @click="onToggle" type="button" class="font-sans text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
                                <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                                </svg>
                                <span class="sr-only">Close modal</span>
                            </button>
                        </div>
                        <!-- Modal body -->
                        <div class="p-4 font-sans  md:p-5 space-y-4 overflow-auto min-w-full">
                           <form>
                           <div class="w-[450px] mb-4 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600">
                               <div class="px-4 py-2 bg-white rounded-t-lg dark:bg-gray-800">
                                   <label for="comment" class="sr-only">پیام خود را برای کاربر بنویسید</label>
                                   <textarea v-model="sendToAllParams.text" id="comment" rows="4" class="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400" placeholder="پیام خود را برای کاربر بنویسید..." required ></textarea>
                               </div>
                               <div class="flex items-center justify-between px-3 py-2 border-t dark:border-gray-600">
                                   <div class="w-45">
                                     <Button @click="sendToAll">
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
                                           @click="$refs.fileInput.click()"
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
                        </div>
                    </div>
                </div>
              </div>
              </transition>
            </Teleport>
          </div>
        </aside>
        </transition>

        <div :class="[isMenuHidden? '':'sm:mr-64']" class="flex flex-col flex-grow gap-2 px-4 py-2 min-w-1">

          <transition name="fade" mode="out-in">
            <router-view
                @sidebarOpen="isMenuHidden=false;"
            />
          </transition>
        </div>
    </main>

</template>

<script>
import axios from 'axios';
import {useToast} from "vue-toastification";
import Button from "@/components/button.vue";
import Input from "@/components/input.vue";
import Modal from "@/components/Modal.vue";
export default {
  components: {Modal, Input, Button},
  data() {
    return {
      userUnReadMessages: {
        count: 0,
        status: false
      },
      userNewPayments: {
        count: 0,
        status: false
      },
      sendToAllParams: {
        text: '',
        image: null
      },
      isOpen: false,
      isMenuHidden:false
    }
  },
  computed: {
    isModalVisible() {
      return this.isOpen;
    }
  },
  methods: {
    Logout() {
      axios.post('Logout/')
        .then(response => {
          console.log(response.data);
          this.$router.replace({ path: '/Login'})
        })
        .catch(error => {
          console.error(error);
        });
    },
    unReadMessages(){
      this.axios.get('/api/totalUnReadMessagesAndNewPayment', ).then((response) => {
        if(response) {
          this.userUnReadMessages.count = response.data['data']['total_unread_messages']
          this.userNewPayments.count = response.data['data']['total_new_payments']
          if (this.userUnReadMessages.count != 0) {
            this.userUnReadMessages.status = true
          }
          if (this.userNewPayments.count != 0) {
            this.userNewPayments.status = true
          }
        }
      })
    },
    sendToAll(){
        const params = {
          "message": this.sendToAllParams.text,
        };
        if (this.sendToAllParams.image){
          this.axios.post('/api/sendToAll', this.sendToAllParams.image, {
            headers: {
              'Content-Type': 'multipart/form-data' // Set content type for image upload
            },
            params: params
          }).then((response) => {
            const toast = useToast();
            toast.success("پیام شما با موفقیت ارسال شد.");
          })
        } else {
          this.axios.get('/api/sendToAll',{params: params}).then((response) => {
            const toast = useToast();
            toast.success("پیام شما با موفقیت ارسال شد.");
          })
        }
    },
    onFilePicked (event) {
      const files = event.target.files
      // Send the image file to the server
      const image = new FormData();
      image.append("image", files[0]); // Add image to form data
      this.sendToAllParams.image = image
    },
    onToggle() {
      this.isOpen = !this.isOpen;
    }
  },
  mounted() {
    this.unReadMessages()
  }
};
</script>