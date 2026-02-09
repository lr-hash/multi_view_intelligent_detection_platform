<template>
  <div class="logs-container">
    <h2>接口日志</h2>
    <div class="log-table-container">
      <table class="log-table">
        <thead>
          <tr>
            <th>时间戳</th>
            <th>接口</th>
            <th>状态</th>
            <th>信息</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.timestamp + log.interface" :class="`status-${log.status.toLowerCase()}`">
            <td>{{ log.timestamp }}</td>
            <td>{{ log.interface }}</td>
            <td><span class="status-badge">{{ log.status }}</span></td>
            <td>{{ log.message }}</td>
          </tr>
          <tr v-if="logs.length === 0 && !isLoading">
            <td colspan="4">没有可显示的日志。</td>
          </tr>
           <tr v-if="isLoading">
            <td colspan="4">加载中...</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const logs = ref([]);
const isLoading = ref(true);

async function fetchLogs() {
  isLoading.value = true;
  try {
    const response = await api.getInterfaceLogs();
    logs.value = response.data;
  } catch (error) {
    console.error('Error fetching interface logs:', error);
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  fetchLogs();
});
</script>

<style scoped>
.logs-container {
  padding: 1rem;
}

h2 {
  margin-bottom: 1.5rem;
}

.log-table-container {
  overflow-x: auto;
}

.log-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #1a2952;
}

.log-table th, .log-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #2a3f78;
}

.log-table th {
  background-color: #2a3f78;
  font-weight: bold;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  color: #fff;
}

.status-success .status-badge {
  background-color: #4CAF50; /* Green */
}

.status-failure .status-badge, .status-失败 .status-badge {
  background-color: #f44336; /* Red */
}
</style>
