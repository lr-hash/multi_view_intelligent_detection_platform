<template>
  <div class="logs-container">
    <div class="header-row">
      <h2>报警历史记录</h2>
      <button @click="fetchAlarms" class="refresh-btn">刷新</button>
    </div>
    
    <div class="log-table-container">
      <table class="log-table">
        <thead>
          <tr>
            <th>报警时间</th>
            <th>类型</th>
            <th>触发值</th>
            <th>阈值</th>
            <th>级别</th>
            <th>处理状态</th>
            <th>报警描述</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alarm in alarms" :key="alarm.id">
            <td>{{ new Date(alarm.timestamp).toLocaleString() }}</td>
            <td>{{ alarm.type }}</td>
            <td class="numeric">{{ alarm.value }}</td>
            <td class="numeric">{{ alarm.threshold }}</td>
            <td>
              <span class="level-badge" :class="alarm.level.toLowerCase()">
                {{ alarm.level }}
              </span>
            </td>
            <td>
              <span class="status-badge" :class="alarm.status.toLowerCase()">
                {{ alarm.status }}
              </span>
            </td>
            <td class="msg-cell">{{ alarm.message }}</td>
          </tr>
          <tr v-if="alarms.length === 0 && !isLoading">
            <td colspan="7" class="empty-row">没有可显示的报警历史。</td>
          </tr>
           <tr v-if="isLoading">
            <td colspan="7" class="loading-row">数据分析中...</td>
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
.logs-container {
  padding: 2rem;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.refresh-btn {
  background-color: #2a3f78;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.log-table-container {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #2a3f78;
}

.log-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #1a2952;
}

.log-table th, .log-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #2a3f78;
  color: #c0c5d6;
}

.log-table th {
  background-color: #2a3f78;
  font-weight: 600;
  color: #fff;
}

.numeric {
  font-family: monospace;
  font-size: 1.1rem;
}

.level-badge {
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: bold;
}

.level-badge.red { background-color: #dc3545; color: #fff; }
.level-badge.yellow { background-color: #ffc107; color: #333; }

.status-badge {
  font-size: 0.85rem;
  text-transform: uppercase;
}
.status-badge.pending { color: #ffc107; }
.status-badge.acknowledged { color: #17a2b8; }

.msg-cell {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.empty-row, .loading-row {
  text-align: center;
  padding: 3rem !important;
}
</style>

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
