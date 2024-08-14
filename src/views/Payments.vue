<script>
import SearchInput from "@/components/searchInput.vue";
import Dropdown from "@/components/Dropdown.vue";
import Table from "@/components/table.vue";
import {useToast} from "vue-toastification";
import Button from "@/components/button.vue";

export default {
  name: "Payments",
  components: {Button, Table, Dropdown, SearchInput},
  data(){
    return {
      cardToCard: true,
      Heads:['تاریخ ثبت نام', 'عکس فیش پرداخت', 'وضعیت پرداخت', 'تایید پرداخت',],
      Datum: null
    }
  },
  mounted() {
    this.getPaymentsDate()
  },
  methods:{
    changePaymentMethod(status){
      this.cardToCard = status
      if (status){
        this.getPaymentsDate()
      }
    },
    getPaymentsDate(){
      this.axios.get('/api/getPaymentsDate').then((response) => {
        this.Datum = response.data['data']
      })
    },
    sendTicket(row){
        const id = row['id']
        const params = {
          "lottery_id": id,
        };
        this.axios.get('/api/sendTicket',{params: params}).then((response) => {
          this.messagesDatum = response.data['data']
          const toast = useToast();
          toast.success("پرداخت تایید و بلیط با موفقیت ارسال شد.");
          this.Datum.forEach(r=>{
            if (r == row){
              r['payment_status']="PAID"
            }
          })
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
  <nav class="flex flex-row gap-2 sm:items-center justify-between font-semibold bg-white">
    <div @click='changePaymentMethod(true)' class="truncate flex flex-row gap-4 items-center justify-center block w-full px-4 py-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700 hover:border-blue-600">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-credit-card-2-back" viewBox="0 0 16 16">
        <path d="M11 5.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5z"/>
        <path d="M2 2a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zm13 2v5H1V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1m-1 9H2a1 1 0 0 1-1-1v-1h14v1a1 1 0 0 1-1 1"/>
      </svg>
      کارت به کارت
    </div>
    <div @click='changePaymentMethod(false)' class="truncate flex flex-row gap-4 items-center justify-center block w-full px-4 py-2 border-b border-gray-200 cursor-pointer hover:bg-gray-100 hover:text-blue-700 hover:border-blue-600">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-postcard" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M2 2a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zM1 4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1zm7.5.5a.5.5 0 0 0-1 0v7a.5.5 0 0 0 1 0zM2 5.5a.5.5 0 0 1 .5-.5H6a.5.5 0 0 1 0 1H2.5a.5.5 0 0 1-.5-.5m0 2a.5.5 0 0 1 .5-.5H6a.5.5 0 0 1 0 1H2.5a.5.5 0 0 1-.5-.5m0 2a.5.5 0 0 1 .5-.5H6a.5.5 0 0 1 0 1H2.5a.5.5 0 0 1-.5-.5M10.5 5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5zM13 8h-2V6h2z"/>
      </svg>
      درگاه پرداخت
    </div>
  </nav>
  <main>
    <template v-if="cardToCard">
      <Table>
        <template v-slot:head>
          <template v-for="head in Heads">
            <th scope="col" class="px-6 py-3">
              {{ head }}
            </th>
          </template>
        </template>
        <template v-slot:body>
          <template v-for="row in Datum">
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
                    {{ row['register_date'] }}
                </th>
                <td class="px-6 py-4">
                  <img class="object-cover w-10 h-10  rounded-t-lg md:rounded-none md:rounded-s-lg" :src="row['payment_picture']" alt=""  @click="openImageInNewWindow(row['payment_picture'])">
                </td>
                <td class="px-6 py-4">
                  {{ row['payment_status'] }}
                </td>
                <td class="px-6 py-4 text-nowrap">
                  <template v-if="row['payment_status']=='PENDING'">
                    <a @click="sendTicket(row)" href="#" class="font-medium text-green-600 dark:text-blue-500 hover:underline">
                      تایید و ارسال بلیط
                    </a>
                  </template>
                  <template v-else>تایید شده</template>
                </td>
            </tr>
          </template>
        </template>
      </Table>
    </template>
    <template v-else>
      هنوز طراحی نشده!
    </template>
  </main>
</template>
