<script setup>
import { RouterView, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { computed, watch, onMounted } from 'vue';
import websocket from '@/services/websocket';
import AlarmNotification from '@/components/AlarmNotification.vue';

const authStore = useAuthStore();
const route = useRoute();

const isLoginPage = computed(() => route.name === 'login');

function handleLogout() {
  authStore.logout();
  websocket.disconnect();
}

// Watch for authentication changes to manage WebSocket connection
watch(() => authStore.isAuthenticated, (isAuthenticated) => {
  if (isAuthenticated) {
    websocket.connect();
  } else {
    websocket.disconnect();
  }
});

onMounted(() => {
  if (authStore.isAuthenticated) {
    websocket.connect();
  }
});
</script>

<template>
  <header v-if="authStore.isAuthenticated && !isLoginPage">
    <div class="wrapper">
      <div class="title">
        <h1>多视域智能侦测平台</h1>
      </div>
      <nav>
        <RouterLink to="/">主页</RouterLink>
        <RouterLink to="/dashboard">数据看板</RouterLink>
        <RouterLink to="/visualize">压裂设计可视化</RouterLink>
        <RouterLink to="/interface-status">接口状态</RouterLink>
        <RouterLink to="/interface-logs">接口日志</RouterLink>
        <RouterLink to="/alarm-history">报警历史</RouterLink>
        <RouterLink to="/interface-config">接口配置</RouterLink>
        <RouterLink to="/data-query">数据查询</RouterLink>
        <a href="#" @click.prevent="handleLogout">退出登录</a>
      </nav>
    </div>
  </header>

  <main :class="{ 'full-page': isLoginPage }">
    <AlarmNotification />
    <RouterView />
  </main>
</template>

<style scoped>
header {
  background-color: #1a2952; /* Lighter Dark Blue */
  border-bottom: 1px solid #2a3f78;
  padding: 0 2rem;
  height: 4rem;
  display: flex;
  align-items: center;
}

header .wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.title h1 {
  font-size: 1.5rem;
  font-weight: 500;
  color: #ffffff;
  margin: 0;
}

nav {
  display: flex;
  align-items: center;
  font-size: 1rem;
}

nav a {
  padding: 0.5rem 1rem;
  color: #c0c5d6; /* Light gray for non-active links */
  border-radius: 4px;
  margin-left: 0.5rem;
}

nav a.router-link-exact-active {
  color: #ffffff;
  background-color: hsla(198, 100%, 50%, 0.3);
}

nav a:not(.router-link-exact-active):hover {
  background-color: #2a3f78;
  color: #ffffff;
}

main {
  padding: 2rem;
  flex-grow: 1;
}

main.full-page {
  padding: 0;
}
</style>

