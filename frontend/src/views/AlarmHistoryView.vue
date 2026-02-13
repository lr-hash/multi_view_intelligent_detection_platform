<template>
  <div class="logs-container animate-fade-in">
    <div class="header-row">
      <h2>报警历史记录</h2>
      <div class="header-controls">
        <div v-if="authStore.user?.role === 'ADMIN'" class="admin-actions">
          <button @click="confirmClearAll" class="btn btn-outline-danger">清空所有</button>
          <button 
            @click="confirmBulkDelete" 
            class="btn btn-danger" 
            :disabled="selectedIds.length === 0"
          >
            删除选中 ({{ selectedIds.length }})
          </button>
        </div>
        <button @click="fetchAlarms" class="btn btn-primary">刷新数据</button>
      </div>
    </div>
    
    <div class="log-table-container card-panel">
      <table class="log-table">
        <thead>
          <tr>
            <th v-if="authStore.user?.role === 'ADMIN'" class="checkbox-col">
              <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll" />
            </th>
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
          <tr v-for="alarm in alarms" :key="alarm.id" :class="{ selected: selectedIds.includes(alarm.id) }">
            <td v-if="authStore.user?.role === 'ADMIN'" class="checkbox-cell">
              <input type="checkbox" :value="alarm.id" v-model="selectedIds" />
            </td>
            <td class="time-cell">{{ new Date(alarm.timestamp).toLocaleString() }}</td>
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
            <td class="msg-cell" :title="alarm.message">{{ alarm.message }}</td>
          </tr>
          <tr v-if="alarms.length === 0 && !isLoading">
            <td :colspan="authStore.user?.role === 'ADMIN' ? 8 : 7" class="empty-row">
              <div class="empty-state">
                <span>📭</span>
                <p>暂无报警历史记录</p>
              </div>
            </td>
          </tr>
           <tr v-if="isLoading">
            <td :colspan="authStore.user?.role === 'ADMIN' ? 8 : 7" class="loading-row">
              <div class="spinner"></div>
              <span>正在分析历史轨迹...</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';
import axios from 'axios';

const authStore = useAuthStore();
const alarms = ref([]);
const isLoading = ref(true);
const selectedIds = ref([]);

const axios_instance = axios.create({ baseURL: '/api/v1' });
axios_instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

async function fetchAlarms() {
  isLoading.value = true;
  selectedIds.value = [];
  try {
    const response = await api.getAlarmHistory();
    alarms.value = response.data;
  } catch (error) {
    console.error('Error fetching alarm history:', error);
  } finally {
    isLoading.value = false;
  }
}

const isAllSelected = computed(() => {
  return alarms.value.length > 0 && selectedIds.value.length === alarms.value.length;
});

function toggleSelectAll() {
  if (isAllSelected.value) {
    selectedIds.value = [];
  } else {
    selectedIds.value = alarms.value.map(a => a.id);
  }
}

async function confirmBulkDelete() {
  if (confirm(`确定要删除选中的 ${selectedIds.length} 条报警记录吗？`)) {
    try {
      await axios_instance.post('/alarms/bulk-delete', { ids: selectedIds.value });
      fetchAlarms();
    } catch (e) {
      alert("删除失败");
    }
  }
}

async function confirmClearAll() {
  if (confirm('警告：确定要清空所有的报警历史吗？此操作不可撤销！')) {
    try {
      await axios_instance.post('/alarms/clear-all');
      fetchAlarms();
    } catch (e) {
      alert("清空失败");
    }
  }
}

onMounted(() => {
  fetchAlarms();
});
</script>

<style scoped>
.logs-container {
  padding: 1rem;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 1rem;
}

.header-controls {
  display: flex;
  gap: 1rem;
}

.admin-actions {
  display: flex;
  gap: 0.5rem;
  border-right: 1px solid var(--color-border);
  padding-right: 1rem;
}

.btn {
  padding: 0.6rem 1.2rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-weight: 600;
  border: none;
  transition: all 0.2s;
}

.btn-primary { background: var(--color-primary); color: white; }
.btn-danger { background: var(--color-danger); color: white; }
.btn-outline-danger { 
  background: transparent; 
  border: 1px solid var(--color-danger); 
  color: var(--color-danger); 
}
.btn-outline-danger:hover { background: var(--color-danger); color: white; }

.btn:disabled { opacity: 0.4; cursor: not-allowed; }

.log-table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 1rem;
  color: var(--color-text-muted);
  font-size: 0.9rem;
  border-bottom: 1px solid var(--color-border);
}

td {
  padding: 1rem;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-main);
  font-size: 0.95rem;
}

tr:hover td { background: rgba(255,255,255,0.02); }
tr.selected td { background: rgba(59, 130, 246, 0.1); }

.checkbox-col, .checkbox-cell { width: 50px; text-align: center; }

.time-cell { color: var(--color-info); font-family: monospace; }
.numeric { font-family: monospace; font-weight: bold; }

.level-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 800;
}
.level-badge.red { background: var(--color-danger); color: white; box-shadow: 0 0 10px rgba(239, 68, 68, 0.3); }
.level-badge.yellow { background: var(--color-warning); color: #000; }

.status-badge { font-size: 0.8rem; font-weight: bold; text-transform: uppercase; }
.status-badge.pending { color: var(--color-warning); }
.status-badge.acknowledged { color: var(--color-success); }

.msg-cell {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--color-text-muted);
}

.empty-row, .loading-row { text-align: center; padding: 5rem !important; }

.spinner {
  width: 24px; height: 24px;
  border: 3px solid rgba(255,255,255,0.1);
  border-left-color: var(--color-primary);
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
