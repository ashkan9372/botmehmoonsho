<script>
import {FwbButton} from "flowbite-vue";
import {useToast} from "vue-toastification";

export default {
  name: "Login",
  components: {FwbButton},
  data(){
    return {
      detum: {
        username: null,
        password: null
      }
    }
  },
  methods:{
    Login(){
      const params = {
        'username': this.detum.username,
        'password': this.detum.password,
      }
      this.axios.post('/Login/', {params: params}, {params: params}).then((response) => {
        console.log(response)
        console.log(response.data['message'])
        if (response.data['status_code']==200){
            const toast = useToast();
            toast.success("ورود با موفقیت انجام شد");
            this.$router.replace({ path: '/'}).then(()=>{
              // location.reload();
            });
        }
      }).catch(()=>{})
    }
  },
}
</script>

<template>
  <div>
    <teleport to="body">
      <section class="fixed inset-0 bg-gray-50 dark:bg-gray-900 z-50">
        <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
            <div class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                    <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                      ورود به پنل مدیریت
                    </h1>
                    <form class="space-y-4 md:space-y-6" action="#">
                        <div>
                            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">نام کاربری</label>
                            <input v-model="detum.username" class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="نام کاربری" required="">
                        </div>
                        <div>
                            <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">کلمه عبور</label>
                            <input v-model="detum.password" type="password" placeholder="••••••••" class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required="">
                        </div>
                    </form>
                    <button @click="Login" class="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-blue-800">ورود</button>
                </div>
            </div>
        </div>
      </section>
    </teleport>
  </div>
</template>
