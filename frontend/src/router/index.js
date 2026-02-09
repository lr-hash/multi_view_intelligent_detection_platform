import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '@/store/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { public: true } // Mark this route as public
    },
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue')
    },
    {
      path: '/visualize',
      name: 'visualize',
      component: () => import('../views/VisualizeView.vue')
    },
    {
      path: '/interface-status',
      name: 'interface-status',
      component: () => import('../views/InterfaceStatusView.vue')
    },
    {
      path: '/interface-logs',
      name: 'interface-logs',
      component: () => import('../views/InterfaceLogsView.vue')
    },
    {
      path: '/evaluation-report/:boreholeId',
      name: 'evaluation-report',
      component: () => import('../views/EvaluationReportView.vue'),
      props: true // Pass route params as component props
    },
    {
      path: '/alarm-history',
      name: 'alarm-history',
      component: () => import('../views/AlarmHistoryView.vue')
    },
    {
      path: '/interface-config',
      name: 'interface-config',
      component: () => import('../views/InterfaceConfigView.vue')
    },
    {
      path: '/data-query',
      name: 'data-query',
      component: () => import('../views/DataQueryView.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;
  const isPublic = to.matched.some(record => record.meta.public);

  if (!isAuthenticated && !isPublic) {
    // If not authenticated and the route is not public, redirect to login
    return next({ name: 'login' });
  }

  if (isAuthenticated && to.name === 'login') {
    // If authenticated and trying to access login page, redirect to home
    return next({ name: 'home' });
  }

  next();
});

export default router
