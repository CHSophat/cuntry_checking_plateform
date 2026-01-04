import { createRouter, createWebHistory } from 'vue-router';
import DefaultLayout from '../layouts/DefaultLayout.vue';
import Home from '../pages/Home.vue';
import About from '../pages/About.vue';
import AiTool from '../pages/AiTool.vue';

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '',
        component: Home,
        name: 'Home'
      },
      {
        path: '/ai-tool',
        component: AiTool,
        name: 'AiTool'
      },
      {
        path: '/about',
        component: About,
        name: 'About'
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
