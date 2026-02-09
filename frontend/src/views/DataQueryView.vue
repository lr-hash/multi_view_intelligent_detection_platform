<template>
  <div class="query-container">
    <h2>数据查询与导出</h2>

    <form @submit.prevent="executeQuery" class="query-form">
      <div class="input-group">
        <label for="dataType">数据类型:</label>
        <select id="dataType" v-model="queryParams.target">
          <option value="pressure">支架压力数据</option>
          <option value="seismic">微震事件数据</option>
          <option value="deformation">巷道变形数据</option>
          <option value="fracture">压裂施工数据</option>
          <option value="alarm">报警历史记录</option>
        </select>
      </div>
      <div class="input-group">
        <label for="startTime">开始时间:</label>
        <input type="datetime-local" id="startTime" v-model="queryParams.start_time" />
      </div>
      <div class="input-group">
        <label for="endTime">结束时间:</label>
        <input type="datetime-local" id="endTime" v-model="queryParams.end_time" />
      </div>
      <button type="submit" class="query-button">查询</button>
      <button type="button" @click="exportData" class="export-button" :disabled="!queryResults.length">导出 CSV</button>
    </form>

    <div v-if="isLoading" class="loading-message">加载查询结果中...</div>
    <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-else-if="queryResults.length" class="results-table-container">
      <h3>查询结果 ({{ queryResults.length }} 条)</h3>
      <table class="results-table">
        <thead>
          <tr>
            <th v-for="key in Object.keys(queryResults[0])" :key="key">{{ key }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in queryResults" :key="index">
            <td v-for="key in Object.keys(row)" :key="key">{{ row[key] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="no-results-message">
      {{ hasQueried ? '没有找到符合条件的数据。' : '请输入查询条件并点击查询。' }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';

const queryParams = ref({
  target: 'pressure',
  start_time: '',
  end_time: '',
});
const queryResults = ref([]);
const isLoading = ref(false);
const errorMessage = ref('');
const hasQueried = ref(false);

async function executeQuery() {
  isLoading.value = true;
  errorMessage.value = '';
  hasQueried.value = true;
  
  // 转换时间格式为 ISO (后端要求)
  const payload = {
    target: queryParams.value.target,
    start_time: queryParams.value.start_time ? new Date(queryParams.value.start_time).toISOString() : null,
    end_time: queryParams.value.end_time ? new Date(queryParams.value.end_time).toISOString() : null,
  };

  try {
    const response = await api.queryData(payload);
    queryResults.value = response.data;
  } catch (error) {
    console.error('Error executing query:', error);
    errorMessage.value = '查询数据失败，请检查网络或稍后再试。';
    queryResults.value = [];
  } finally {
    isLoading.value = false;
  }
}

function exportData() {
  if (!queryResults.value.length) return;

  const headers = Object.keys(queryResults.value[0]).join(',');
  const rows = queryResults.value.map(row => 
    Object.values(row).map(v => `"${v}"`).join(',')
  ).join('\n');
  
  const csvContent = "\uFEFF" + headers + "\n" + rows; // Add BOM for Excel compatibility
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", `data_export_${queryParams.value.target}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
</script>

<style scoped>
.query-container {
  padding: 1rem;
}

h2 {
  margin-bottom: 1.5rem;
}

.query-form {
  background-color: #1a2952;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #c0c5d6;
  font-weight: bold;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #2a3f78;
  border-radius: 4px;
  background-color: #0d1a3c;
  color: #ffffff;
  font-size: 1rem;
}

.query-button, .export-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 1.5rem; /* Align with input fields */
}

.query-button {
  background-color: hsla(198, 100%, 50%, 0.8);
  color: white;
}

.query-button:hover {
  background-color: hsla(198, 100%, 50%, 1);
}

.export-button {
  background-color: #4CAF50; /* Green */
  color: white;
  margin-left: 1rem;
}

.export-button:hover:not(:disabled) {
  background-color: #45a049;
}

.export-button:disabled {
  background-color: #666;
  cursor: not-allowed;
}

.loading-message, .error-message, .no-results-message {
  text-align: center;
  padding: 1rem;
  font-size: 1.1rem;
}

.error-message {
  color: #f44336;
}

.results-table-container {
  margin-top: 2rem;
  background-color: #1a2952;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow-x: auto;
}

.results-table h3 {
  padding: 1rem;
  border-bottom: 1px solid #2a3f78;
  margin-bottom: 1rem;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
}

.results-table th, .results-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #2a3f78;
  white-space: nowrap; /* Prevent text wrapping in cells */
}

.results-table th {
  background-color: #2a3f78;
  font-weight: bold;
}

.results-table tbody tr:hover {
  background-color: #2a3f78;
}
</style>
