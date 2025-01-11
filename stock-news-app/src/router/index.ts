import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router';
import StockNews from '../components/StockNews.vue';
import About from '../components/About.vue'

const routes: Array<RouteRecordRaw> = [
  {
      path: '/',
      name: 'Home',
      component: StockNews,
  },
  {
      path: '/about',
      name: 'About',
      component: About,
  },
  {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../components/NotFound.vue'), // Lazy-loaded 404 page
  },
];

// Create router instance
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'), // Ensure BASE_URL is defined
  routes,
});

export default router;
