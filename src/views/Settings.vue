<script>
import Button from "@/components/button.vue";
import Modal from "@/components/Modal.vue";
import Table from "@/components/table.vue";
import Input from "@/components/input.vue";
import {FwbButton} from "flowbite-vue";
import {useToast} from "vue-toastification";
import DatePicker from "@/components/DatePicker.vue";

const toast = useToast();

export default {
  name: "Settings",
  components: {DatePicker, FwbButton, Input, Table, Modal, Button},
  data(){
    return {
      admin: {
        name: '',
        id: '',
      },
      game: '',
      adminsDatum: [],
      gamesDatum: [],
      selectedPaymentMethod: 'card-to-card',
      payment_card: {
        number: '',
        name: '',
        price: '',
        edit: true
      },
      settingsDatum: {
        card_name: '',
        card_number: '',
        lottery_date: '',
        channel: '',
        link: '',
      },
      date: {
        start: null,
        end: null,
        lottery: null,
      }
    }
  },
  methods: {
    setDate(){
      let params = {
        'start': JSON.stringify(this.date.start),
        'end': JSON.stringify(this.date.end),
        'lottery': JSON.stringify(this.date.lottery),
      }
      this.axios.get('/api/setDate', {params:params}).then((response) => {
        toast.success('درخواست شما با موفقیت انجام شد.');
      })
    },
    addAdmin(){
      let params = {
        'name': this.admin.name,
        'id': this.admin.id,
      }
      this.axios.get('/api/addAdmin', {params:params}).then((response) => {
        toast.success('ادمین مورد نظر با موفقیت اضاقه شد');
        this.adminsDatum.push({
        'name': this.admin.name,
        'user_id': this.admin.id,
        })
      })
    },
    removeAdmin(id){
      let params = {
        'id': id,
      }
      this.axios.get('/api/removeAdmin', {params:params}).then((response) => {
          toast.success('ادمین مورد نظر با موفقیت عزل شد');
          const index = this.adminsDatum.findIndex(item => item.id === id);
          if (index > -1) {
            this.adminsDatum.splice(index, 1);
          }
      })
    },
    getAdmins(){
      this.axios.get('/api/getAdmins').then((response) => {
          this.adminsDatum = response.data['data'] ? response.data['data'] : []
      })
    },
    addGame(){
      let params = {
        'name': this.game,
      }
      this.axios.get('/api/addGame', {params:params}).then((response) => {
          toast.success('بازی مورد نظر با موفقیت اضاقه شد');
          this.gamesDatum.push({
            'name': this.game,
          })
          console.log(this.gamesDatum)
      })
    },
    removeGame(id, name){
      let params = {
        'id': id,
      }
      this.axios.get('/api/removeGame', {params:params}).then((response) => {
          toast.success('بازی مورد نظر با موفقیت حذف شد');
          const index = this.gamesDatum.findIndex(item => item.name === name);
          if (index > -1) {
            this.gamesDatum.splice(index, 1);
          }
      })
    },
    getGames(){
      this.axios.get('/api/getGames', ).then((response) => {
          this.gamesDatum = response.data['data'] ? response.data['data'] : []
          console.log(this.gamesDatum)
      })
    },
    setCard(){
      let params = {
        'card_name': this.payment_card.name,
        'card_number': this.payment_card.number,
        'price': this.payment_card.price,
        'payment_method': this.selectedPaymentMethod
      }
      this.axios.get('/api/setCard', {params:params}).then((response) => {
          toast.success('اطلاعات کارت مورد نظر با موفقیت ثبت شد');
      })
    },
    updateCard(){
      let params = {
        'card_name': this.payment_card.name,
        'card_number': this.payment_card.number,
        'price': this.payment_card.price,
        'payment_method': this.selectedPaymentMethod
      }
      this.axios.get('/api/updateCard', {params:params}).then((response) => {
          toast.success('اطلاعات کارت مورد نظر با موفقیت آپدیت شد');
      })
    },
    getSettings(){
      this.axios.get('/api/getSettings').then((response) => {
          if (response.data['data']){
            this.settingsDatum = response.data['data'][0]
            this.payment_card.name = response.data['data'][0]['card_name']
            this.payment_card.number = response.data['data'][0]['card_number']
            this.payment_card.price = response.data['data'][0]['price']
            this.date.start = response.data['data'][0]['start_time']
            this.date.end = response.data['data'][0]['end_time']
            this.date.lottery = response.data['data'][0]['lottery_time']
          }
      })
    },
    updateChannelSettings(){
      let params = {
        'channel': this.settingsDatum.channel,
        'link': this.settingsDatum.link,
      }
      this.axios.get('/api/updateChannelSettings', {params:params}).then((response) => {
          toast.success('تنظیمات کانال با موفقیت ثبت شد');
      })
    },
    generateExcel(){
      this.axios.get('/api/generateExcel').then((response) => {
          toast.success('قرعه کشی با موفقیت پایان یافت');
          // Create a URL for the blob
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;

          // Suggest a filename for the downloaded file
          const filename = response.headers['content-disposition'];
          link.setAttribute('download', filename);

          // Append the link to the body
          document.body.appendChild(link);

          // Simulate click to download the file
          link.click();

          // Remove the link from the body
          document.body.removeChild(link);
      })
    },
    endLottery(){
      this.axios.get('/api/endLottery').then((response) => {
          toast.success('قرعه کشی با موفقیت پایان یافت');
      })
    },
  },
  mounted() {
    this.getSettings()
    this.getAdmins()
    this.getGames()
  }
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

<div class="flex flex-col gap-2">
<!--  admins-->
  <main class="flex flex-col gap-2 bg-white w-100 p-4 rounded-lg">
    <header>
      <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">تنظیمات ادمین</h5>
      <p class="font-normal text-gray-700 dark:text-gray-400">این قسمت مربوط به مدیریت ادمین ها میباشد, میتوانید در این قسمت یک ادمین اضافه کنید یا ان را عزل کنید.</p>
    </header>
    <main class="flex flex-col gap-2">
      <Table>
        <template v-slot:head>
          <template v-for="head in ['اسم','آیدی عددی','عزل']">
            <th scope="col" class="px-6 py-3">
              {{ head }}
            </th>
          </template>
        </template>
        <template v-slot:body>
          <template v-for="row in adminsDatum">
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
                    {{ row['name'] }}
                </th>
                <td class="px-6 py-4">
                    {{ row['user_id'] }}
                </td>
                <td class="px-6 py-4">
                    <a @click="removeAdmin(row['id'])" href="#" class="font-medium text-green-600 dark:text-green-500 hover:underline">عزل</a>
                </td>
            </tr>
          </template>
        </template>
      </Table>
      <div class="flex flex-col md:flex-row gap-2">
        <Input @update="admin['name']=$event" title="اسم ادمین" />
        <Input @update="admin['id']=$event" title="آیدی عددی ادمین" />
        <fwb-button @click="addAdmin">اضافه کردن</fwb-button>
      </div>
    </main>
  </main>
<!--  Games-->
  <main class="flex flex-col gap-2 bg-white w-100 p-4 rounded-lg">
    <header>
      <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">تنظیمات بازی/فعالیت ها</h5>
      <p class="font-normal text-gray-700 dark:text-gray-400">این قسمت مربوط به مدیریت بازی/فعالیت هاست میتونید بازی/فعالیت جدید اضافه کنید ها انهارا از لیست حذف کنید.</p>
    </header>
    <main class="flex flex-col gap-2">
      <Table>
        <template v-slot:head>
          <template v-for="head in ['اسم بازی','حذف']">
            <th scope="col" class="px-6 py-3">
              {{ head }}
            </th>
          </template>
        </template>
        <template v-slot:body>
          <template v-for="row in gamesDatum">
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                <th scope="row" class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap dark:text-white">
                    {{ row['name'] }}
                </th>
                <td class="px-6 py-4">
                    <a @click="removeGame(row['id'], row['name'])" href="#" class="font-medium text-green-600 dark:text-green-500 hover:underline">حذف</a>
                </td>
            </tr>
          </template>
        </template>
      </Table>
      <div class="flex flex-col md:flex-row gap-2">
        <Input @update="game=$event" title="اسم بازی" />
        <fwb-button @click="addGame">اضافه کردن</fwb-button>
      </div>
    </main>
  </main>
<!--  payment methods-->
  <main class="flex flex-col gap-2 bg-white w-100 p-4 rounded-lg">
    <header>
      <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">تنظیمات پرداخت</h5>
      <p class="font-normal text-gray-700 dark:text-gray-400">این قسمت مربوط به تنظیمات پرداخت میباشد در این قسمت می توانید روش پرداخت را انتخاب کنید همچنین می توانید اطلاعات پرداخت خود را وارد کنید.</p>
    </header>
    <main class="flex flex-col gap-2">
      <div class="flex flex-col md:flex-row gap-2">
        <Input @update="payment_card['number']=$event" title="شماره کارت:" :disabled="payment_card['edit']" :value="payment_card['number']"/>
        <Input @update="payment_card['name']=$event" title="نام و نام حانوادگی درج شده روی کارت:" :disabled="payment_card['edit']" :value="payment_card['name']"/>
        <Input @update="payment_card['price']=$event" title="مبلغ قرعه کشی (تومان):" :disabled="payment_card['edit']" :value="payment_card['price']"/>
      </div>
      <div class="">
        <h1 class="mb-2 sm:text-xl md:text-2xl font-bold tracking-tight text-gray-900 dark:text-white">روش پرداخت</h1>
        <div class="flex items-center mb-4">
          <input type="radio" id="default-radio-1" value="card-to-card" v-model="selectedPaymentMethod" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
          <label for="default-radio-1" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">کارت به کارت</label>
        </div>
        <div class="flex items-center">
          <input type="radio" id="default-radio-2" value="payment-gateway" v-model="selectedPaymentMethod" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
          <label for="default-radio-2" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">درگاه پرداخت</label>
        </div>
      </div>
      <div class="w-50 flex flex-row gap-2">
        <fwb-button @click="payment_card['edit']=false">ویرایش</fwb-button>
        <fwb-button @click="setCard">ثبت کردن</fwb-button>
        <fwb-button @click="updateCard">آپدیت کردن</fwb-button>
      </div>

    </main>
  </main>
<!--  lottery-->
  <main class="flex flex-col gap-2 bg-white w-100 p-4 rounded-lg">
    <header>
      <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">تنظیمات قرعه کشی</h5>
      <p class="font-normal text-gray-700 dark:text-gray-400">در این قسمت تاریخ و زمان قرعه کشی را می توانید تنظیم کنید.</p>
    </header>
    <main class="flex flex-col gap-2 bg-white w-100 p-4 rounded-lg">
      <div class="flex flex-col md:flex-row md:items-end gap-4">
          <DatePicker Title="شروع ثبت نام" v-model="date.start"/>
          <DatePicker Title="پایان ثبت نام" v-model="date.end"></DatePicker>
          <DatePicker Title="زمان قرعه کشی" v-model="date.lottery"></DatePicker>
      </div>

      <div class="flex flex-col md:flex-row  gap-2">
        <fwb-button @click="setDate">ثبت کردن</fwb-button>
        <fwb-button @click="generateExcel">دریافت فایل اکسل</fwb-button>
        <fwb-button @click="endLottery">پایان قرعه کشی</fwb-button>
      </div>
    </main>
  </main>
<!--  channel -->
  <main class="flex flex-col gap-2 bg-white w-100 p-4 rounded-lg">
    <header>
      <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">تنظیمات کانال</h5>
      <p class="font-normal text-gray-700 dark:text-gray-400">این قسمت مربوط به کانال است در این قست آیدی عددی/یوزر آیدی(همراه با '@') کانال را وارد کرده.توجه داشته باشید که ابتدا ربات را عضو کنال خود کنید</p>
    </header>
    <main class="flex flex-col gap-2">
      <div class="flex flex-col md:flex-row gap-2">
        <Input @update="settingsDatum['channel']=$event" title="آیدی کانال" :value="settingsDatum['channel']"/>
        <Input @update="settingsDatum['link']=$event" title="لینک ویدیو آموژش" :value="settingsDatum['link']"/>
        <fwb-button @click="updateChannelSettings">ثبت کردن</fwb-button>
      </div>
    </main>
  </main>
</div>
</template>
