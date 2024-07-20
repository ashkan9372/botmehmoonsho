import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/tailwind.css'
import 'flowbite'
import axios from 'axios';
import VueAxios from 'vue-axios';
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import { useToast } from "vue-toastification";
import Vue3PersianDatetimePicker from 'vue3-persian-datetime-picker'

const options = {
    // You can set your default options here
};

axios.interceptors.request.use(
    // Add a request interceptor
    (config) => {
      // Do something before request is sent
      if (config.confirmBeforeSend) {
            // console.log('confirm')
          // return new Promise((resolve, reject) => {
        //   Vue.$confirm('Are you sure you want to proceed?', 'Confirmation Required')
        //     .then(() => resolve(config)) // User confirms, proceed with request
        //     .catch(() => reject(new Error('Request cancelled by user'))); // User cancels, reject promise
        // });
      }
      return config;
    },
    (error) => {
      // Do something with request error
      return Promise.reject(error);
    }
);

// Add a response interceptor
axios.interceptors.response.use(
  (response) => {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    // Handle successful responses (optional)
    return response;
  },
  (error) => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    const { message } = error.response?.data || {}; // Extract error message

    // Get toast interface
    const toast = useToast();
    // Display error toast notification
    if (message){
        toast.error(message);
    } else {
        toast.error('خطای ناشناخته ای رخداده!');
    }
      return Promise.reject(error);
  }
);


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const app = createApp(App)
app.use(Vue3PersianDatetimePicker, {
  name: 'DatePicker',
  props: {
    format: 'YYYY-MM-DD HH:mm:ss',
    displayFormat: 'HH:mm jYYYY-jMM-jDD',
    editable: false,
    inputClass: 'form-control my-custom-class-name',
    placeholder: 'Please select a date',
    altFormat: 'YYYY-MM-DD HH:mm:ss',
    color: '#00acc1',
    autoSubmit: false,
    //...
    //... And whatever you want to set as default.
    //...
  }
})
app.use(Toast, options);
app.use(VueAxios, axios)
app.use(router)
app.mount('#app')

// createApp(App).use(router).mount('#app')
