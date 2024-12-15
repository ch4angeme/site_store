import HomePage from '../views/HomePage.vue';
import LoginPage from '../views/LoginPage.vue';
import ProductsPage from '../views/ProductsPage.vue';
import RegistrationPage from '../views/RegistrationPage.vue';
import ProfilePage from '../views/ProfilePage.vue';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
    {
    path: '/catalog',
    name: 'Catalog',
    component: ProductsPage,
  },
    {
    path: '/registration',
    name: 'Registration',
    component: RegistrationPage,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;