import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/components/Home.vue';
import login from "@/components/login";
import register from "@/components/register";
import AddProduct from "@/components/AddProduct";
import AddCategory from "@/components/AddCategory";
import AdminPage from '@/components/AdminPage.vue';
import UserPage from '@/components/UserPage.vue';
import ManagerPage from '@/components/ManagerPage.vue';
import EditCategory from '@/components/EditCategory.vue';
import ManagerCategory from '@/components/ManagerCategory.vue';
import CategoryChanges from '@/components/CategoryChanges.vue';
import ManagerEditCategory from '@/components/ManagerEditCategory.vue';
import UserDashboard from '@/components/UserDashboard.vue';
import UserCart from '@/components/UserCart.vue';
import UserOrders from '@/components/UserOrders.vue';
import ManagerProduct from '@/components/ManagerProduct.vue';
import ManagerEditProduct from '@/components/ManagerEditProduct.vue';

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "login",
    component: login,
  },
  {
    path: "/register",
    name: "register",
    component: register,
  },
  {
    path: '/adminpage',
    name: 'AdminPage',
    component: AdminPage,
    meta: { requiresAuth: true, isAdmin: true }, 
  },
  {
    path: '/categorychanges',
    name: 'CategoryChanges',
    component: CategoryChanges,
    meta: { requiresAuth: true, isAdmin: true },
  },
  {
    path: '/add-product/:categoryId',
    name: 'AddProduct',
    component: AddProduct,
  },
  {
    path: '/add-category',
    name: 'AddCategory',
    component: AddCategory,
  },
  {
    path: '/edit-category/:categoryId',
    name: 'EditCategory',
    component: EditCategory,
  },
  {
    path: '/userspage',
    name: 'Userpage',
    component: UserPage,
    meta: { requiresAuth: true, isManager: true }, 
  },
  {
    path: '/managerpage',
    name: 'Managerpage',
    component: ManagerPage,
    meta: { requiresAuth: true, isManager: true }, 
  },
  {
    path: '/manager/add-category',
    name: 'ManagerCategory',
    component: ManagerCategory,
    meta: { requiresAuth: true, isManager: true }, 
  },
  {
    path: '/manager/edit-category/:categoryId',
    name: 'ManagerEditCategory',
    component: ManagerEditCategory,
    meta: { requiresAuth: true, isManager: true }, 
  },
  {
    path: '/manager/products',
    name: 'ManagerProduct',
    component: ManagerProduct,
    meta: { requiresAuth: true, isManager: true },
  },
  {
    path: '/manager/edit-product/:productId',
    name: 'ManagerEditProduct',
    component: ManagerEditProduct,
    meta: { requiresAuth: true, isManager: true },
  },
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/user/cart',
    name: 'UserCart',
    component: UserCart,
    meta: { requiresAuth: true },
  },
  {
    path: '/user/orders',
    name: 'UserOrders',
    component: UserOrders,
    meta: { requiresAuth: true },
  },
];
Vue.use(VueRouter);
const router = new VueRouter({
  mode: 'history', // or 'hash' for hash mode
  routes,
});
export default router;
