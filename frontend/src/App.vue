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
        <h1>多视域智能侦测平台！！</h1>
      </div>
      <nav>
        <RouterLink to="/" class="nav-link">主页！！！</RouterLink>
        
        <!-- 监控看板 -->
        <div class="nav-dropdown">
          <span class="dropdown-trigger">实时监控 ▼</span>
          <div class="dropdown-content">
            <RouterLink to="/dashboard">数据看板</RouterLink>
            <RouterLink to="/visualize">压裂设计可视化</RouterLink>
          </div>
        </div>

        <!-- 评价分析 -->
        <div class="nav-dropdown">
          <span class="dropdown-trigger">分析评价 ▼</span>
          <div class="dropdown-content">
            <RouterLink :to="{ name: 'evaluation-report', params: { boreholeId: 1 }}">压裂效果评价</RouterLink>
            <RouterLink to="/data-query">综合数据查询</RouterLink>
          </div>
        </div>

        <!-- 系统运维 -->
        <div class="nav-dropdown">
          <span class="dropdown-trigger">系统运维 ▼</span>
          <div class="dropdown-content">
            <RouterLink to="/interface-status">接口运行状态</RouterLink>
            <RouterLink to="/interface-logs">接口调用日志</RouterLink>
            <RouterLink to="/alarm-history">安全报警历史</RouterLink>
          </div>
        </div>

        <!-- 配置管理 -->
        <div class="nav-dropdown" v-if="authStore.user?.role === 'ADMIN'">
          <span class="dropdown-trigger">后台管理 ▼</span>
          <div class="dropdown-content">
            <RouterLink to="/interface-config">参数/阈值配置</RouterLink>
            <RouterLink to="/data-management">基础数据管理</RouterLink>
            <RouterLink to="/user-management">人员权限管理</RouterLink>
          </div>
        </div>

        <a href="#" @click.prevent="handleLogout" class="logout-link">退出</a>
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
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
  padding: 0 2rem;
  height: 4rem;
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 50;
}

header .wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.title h1 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-main);
  letter-spacing: 1px;
  background: linear-gradient(to right, #fff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-link, .dropdown-trigger {
  padding: 0.5rem 1rem;
  color: var(--color-text-muted);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  font-weight: 500;
}

.nav-link:hover, .dropdown-trigger:hover {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.05);
}

.nav-link.router-link-exact-active {
  color: var(--color-primary);
  background-color: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

/* Dropdown Logic */
.nav-dropdown {
  position: relative;
}

.dropdown-content {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 180px;
  background: var(--color-bg-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
  z-index: 100;
  padding: 0.5rem 0;
  backdrop-filter: blur(16px);
}

/* 增加一个不可见的桥接层，防止鼠标移动时因间隙导致菜单消失 */
.dropdown-content::before {
  content: '';
  position: absolute;
  top: -15px; /* 向上延伸覆盖间隙 */
  left: 0;
  width: 100%;
  height: 15px;
  background: transparent;
}

.nav-dropdown:hover .dropdown-content {
  display: block;
  animation: slideDown 0.2s ease-out;
}

.dropdown-content a {
  display: block;
  padding: 0.75rem 1.5rem;
  color: var(--color-text-muted);
  font-size: 0.85rem;
  transition: all 0.2s;
  text-decoration: none;
}

.dropdown-content a:hover {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  padding-left: 1.75rem;
}

.logout-link {
  margin-left: 1rem;
  padding: 0.4rem 1rem;
  border: 1px solid var(--color-border);
  color: var(--color-danger) !important;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  text-decoration: none;
}

.logout-link:hover {
  background: var(--color-danger);
  color: white !important;
  border-color: var(--color-danger);
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

main {
  padding: 2rem;
  flex-grow: 1;
  /* background managed by body */
  min-height: calc(100vh - 4rem);
}

main.full-page {
  padding: 0;
}
</style>

