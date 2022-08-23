import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: '/',
    name: 'VmIndex',
    redirect: '/editor',
  },
  {
    path: '/editor',
    component: () => import('@/components/element/VmIde'),
    meta: { title: 'Vm Web IDE' },
  },
]

export const router = createRouter({
  // history: createWebHashHistory(), // Hash Mode
  history: createWebHistory(), // HTML5 Mode
  routes: routes
})

export default router
