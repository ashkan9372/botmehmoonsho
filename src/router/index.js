import { createRouter, createWebHistory } from 'vue-router'
import UsersView from "@/views/UsersView.vue";
import Profile from "@/views/ProfileView.vue";
import Messages from "@/views/Messages.vue";
import Winning from "@/views/Winning.vue";
import Settings from "@/views/Settings.vue";
import Login from "@/views/Login.vue";


const routes = [
  {
    path: '/',
    name: 'Users',
    component: UsersView
  },
  {
    path: '/Profile',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/Messages',
    name: 'Messages',
    component: Messages
  },
  {
    path: '/Winning',
    name: 'Winning',
    component: Winning
  },
  {
    path: '/Settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/Login',
    name: 'Login',
    component: Login
  }
]

const router = createRouter({
  // history: createWebHistory(process.env.BASE_URL),
  history: createWebHistory(),
  routes,
})
export default router
