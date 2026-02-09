<template>
  <div class="logs-container">
    <h2>报警历史</h2>
    <div class="log-table-container">
      <table class="log-table">
        <thead>
          <tr>
            <th>时间戳</th>
            <th>指标</th>
            <th>报警值</th>
            <th>等级</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alarm in alarms" :key="alarm.id" :class="`level-${alarm.level.toLowerCase()}`">
            <td>{{ new Date(alarm.timestamp).toLocaleString() }}</td>
            <td>{{ alarm.metric }}</td>
            <td>{{ alarm.value }}</td>
            <td><span class="status-badge">{{ alarm.level }}</span></td>
            <td>{{ alarm.acknowledged ? '已确认' : '未确认' }}</td>
          </tr>
          <tr v-if="alarms.length === 0 && !isLoading">
            <td colspan="5">没有可显示的报警历史。</td>
          </tr>
           <tr v-if="isLoading">
            <td colspan="5">加载中...</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const alarms = ref([]);
const isLoading = ref(true);

async function fetchAlarms() {
  isLoading.value = true;
  try {
    const response = await api.getAlarmHistory();
    alarms.value = response.data;
  } catch (error) {
    console.error('Error fetching alarm history:', error);
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  fetchAlarms();
});
</script>

<style scoped>
/* Re-using styles from InterfaceLogsView for consistency */
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

.level-critical .status-badge {
  background-color: #f44336; /* Red */
}

.level-warning .status-badge {
  background-color: #ffeb3b; /* Yellow */
  color: #333;
}
</style>
