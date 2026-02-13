<template>
  <div class="data-management">
    <div class="management-header">
      <h2 class="title">数据管理中心</h2>
      <div class="controls" v-if="authStore.user?.role === 'ADMIN'">
        <button v-if="selectedIds.length > 0" @click="confirmBulkDelete" class="btn btn-danger">批量删除 ({{ selectedIds.length }})</button>
        <button @click="openImportModal" class="btn btn-secondary">批量导入</button>
        <button @click="openAddModal" class="btn btn-primary">手动新增</button>
      </div>
    </div>

    <div class="management-layout">
      <!-- 左侧表选择 -->
      <div class="table-sidebar">
        <div class="sidebar-title">数据分类</div>
        <ul class="table-list">
          <li 
            v-for="table in tables" 
            :key="table.name" 
            :class="{ active: selectedTable?.name === table.name }"
            @click="selectTable(table)"
          >
            {{ table.display_name }}
          </li>
        </ul>
      </div>

      <!-- 右侧内容 -->
      <div class="table-content">
        <div v-if="selectedTable" class="content-wrapper">
          <div class="table-controls">
            <h3 class="selected-table-name">{{ selectedTable.display_name }}</h3>
            <div class="search-box">
              <input v-model="searchQuery" @keyup.enter="fetchData" placeholder="按字段过滤 (字段=值)..." />
              <button @click="fetchData" class="btn btn-search">搜索</button>
            </div>
          </div>

          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th v-if="authStore.user?.role === 'ADMIN'" class="checkbox-col">
                    <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll" />
                  </th>
                  <th v-for="col in displayColumns" :key="col.name">{{ col.comment || col.name }}</th>
                  <th v-if="authStore.user?.role === 'ADMIN'" class="actions-col">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in dataItems" :key="item.id" :class="{ selected: selectedIds.includes(item.id) }">
                  <td v-if="authStore.user?.role === 'ADMIN'" class="checkbox-cell">
                    <input type="checkbox" :value="item.id" v-model="selectedIds" />
                  </td>
                  <td v-for="col in displayColumns" :key="col.name">
                    {{ formatValue(item[col.name], col.type) }}
                  </td>
                  <td v-if="authStore.user?.role === 'ADMIN'" class="actions-cell">
                    <button @click="openEditModal(item)" class="btn-icon edit-btn" title="编辑">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998.001z"/></svg>
                    </button>
                    <button @click="confirmDelete(item)" class="btn-icon delete-btn" title="删除">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg>
                    </button>
                  </td>
                </tr>
                <tr v-if="dataItems.length === 0">
                  <td :colspan="displayColumns.length + 2" class="text-center">暂无数据</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="pagination">
            <span>共 {{ totalItems }} 条记录</span>
            <div class="page-controls">
              <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">上一页</button>
              <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
              <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages || totalPages === 0">下一页</button>
            </div>
          </div>
        </div>
        <div v-else class="no-selection">
          请从左侧选择一个数据表进行管理
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ isEditing ? '编辑记录' : '新增记录' }} - {{ selectedTable.display_name }}</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveData">
            <div v-for="col in editableColumns" :key="col.name" class="form-group">
              <label :for="col.name">{{ col.comment || col.name }} <span v-if="!col.nullable" class="required">*</span></label>
              <input 
                v-if="getInputType(col.type) === 'text'"
                :id="col.name"
                v-model="formModel[col.name]"
                type="text"
                class="form-input"
                :required="!col.nullable"
              />
              <input 
                v-else-if="getInputType(col.type) === 'number'"
                :id="col.name"
                v-model.number="formModel[col.name]"
                type="number"
                step="any"
                class="form-input"
                :required="!col.nullable"
              />
              <input 
                v-else-if="getInputType(col.type) === 'datetime'"
                :id="col.name"
                v-model="formModel[col.name]"
                type="datetime-local"
                class="form-input"
                :required="!col.nullable"
              />
            </div>
            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn btn-cancel">取消</button>
              <button type="submit" class="btn btn-primary">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Import Modal -->
    <div v-if="showImportModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>批量导入 - {{ selectedTable.display_name }}</h3>
          <button @click="closeImportModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="import-instructions">
            <p>请上传 CSV 或 Excel (.xlsx) 文件。文件首行应包含与数据库字段对应的表头。</p>
            <p class="small text-muted">支持字段: {{ editableColumns.map(c => c.name).join(', ') }}</p>
          </div>
          <div class="file-upload">
            <input type="file" @change="handleFileChange" accept=".csv, .xlsx, .xls" />
          </div>
          <div v-if="importResults" class="import-results">
            <p class="success">成功导入: {{ importResults.imported }} 条</p>
            <p v-if="importResults.failed > 0" class="error">失败: {{ importResults.failed }} 条</p>
            <div v-if="importResults.errors && importResults.errors.length" class="error-list">
              <ul>
                <li v-for="(err, idx) in importResults.errors.slice(0, 5)" :key="idx">
                  第 {{ err.row }} 行: {{ err.errors.join(', ') }}
                </li>
                <li v-if="importResults.errors.length > 5">... 更多错误见日志</li>
              </ul>
            </div>
          </div>
          <div class="form-actions">
            <button @click="closeImportModal" class="btn btn-cancel">关闭</button>
            <button @click="executeImport" :disabled="!selectedFile || importing" class="btn btn-primary">
              {{ importing ? '导入中...' : '开始导入' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';
import api from '@/services/api';
import axios from 'axios';

const authStore = useAuthStore();
const axios_instance = axios.create({ baseURL: '/api/v1' });
axios_instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// --- State ---
const tables = ref([]);
const selectedTable = ref(null);
const dataItems = ref([]);
const totalItems = ref(0);
const currentPage = ref(1);
const totalPages = ref(1);
const searchQuery = ref('');
const selectedIds = ref([]);

const showModal = ref(false);
const isEditing = ref(false);
const formModel = reactive({});

const showImportModal = ref(false);
const selectedFile = ref(null);
const importing = ref(false);
const importResults = ref(null);

// --- Computed ---
const displayColumns = computed(() => {
  if (!selectedTable.value) return [];
  return selectedTable.value.columns;
});

const editableColumns = computed(() => {
  if (!selectedTable.value) return [];
  return selectedTable.value.columns.filter(c => !c.primary_key && !['updated_at'].includes(c.name));
});

const isAllSelected = computed(() => {
  return dataItems.value.length > 0 && selectedIds.value.length === dataItems.value.length;
});

// --- Methods ---
async function fetchTables() {
  try {
    const res = await api.getManageableTables();
    tables.value = res.data;
    if (tables.value.length > 0) {
      selectTable(tables.value[0]);
    }
  } catch (err) {
    console.error('获取表列表失败:', err);
  }
}

function selectTable(table) {
  selectedTable.value = table;
  currentPage.value = 1;
  searchQuery.value = '';
  selectedIds.value = [];
  fetchData();
}

async function fetchData() {
  if (!selectedTable.value) return;
  try {
    const params = {
      page: currentPage.value,
      per_page: 15
    };
    
    if (searchQuery.value) {
      const [key, value] = searchQuery.value.split('=');
      if (key && value) {
        params[key.trim()] = value.trim();
      }
    }

    const res = await api.getDataList(selectedTable.value.name, params);
    dataItems.value = res.data.items;
    totalItems.value = res.data.total;
    totalPages.value = res.data.pages;
    selectedIds.value = [];
  } catch (err) {
    console.error('获取数据失败:', err);
  }
}

function toggleSelectAll() {
  if (isAllSelected.value) {
    selectedIds.value = [];
  } else {
    selectedIds.value = dataItems.value.map(item => item.id);
  }
}

async function confirmBulkDelete() {
  if (confirm(`确定要删除选中的 ${selectedIds.value.length} 条记录吗? 此操作不可撤销。`)) {
    try {
      await axios_instance.post(`/management/bulk-delete/${selectedTable.value.name}`, { ids: selectedIds.value });
      fetchData();
    } catch (err) {
      alert('批量删除失败: ' + (err.response?.data?.message || err.message));
    }
  }
}

function changePage(page) {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  fetchData();
}

function formatValue(value, type) {
  if (value === null || value === undefined) return '-';
  if (type.includes('DATETIME')) {
    return new Date(value).toLocaleString();
  }
  return value;
}

function getInputType(dbType) {
  dbType = dbType.toUpperCase();
  if (dbType.includes('INT') || dbType.includes('FLOAT') || dbType.includes('DOUBLE') || dbType.includes('NUMERIC')) {
    return 'number';
  }
  if (dbType.includes('DATETIME') || dbType.includes('TIMESTAMP')) {
    return 'datetime';
  }
  return 'text';
}

// CRUD Operations
function openAddModal() {
  isEditing.value = false;
  Object.keys(formModel).forEach(key => delete formModel[key]);
  editableColumns.value.forEach(col => {
    formModel[col.name] = null;
  });
  showModal.value = true;
}

function openEditModal(item) {
  isEditing.value = true;
  Object.keys(formModel).forEach(key => delete formModel[key]);
  editableColumns.value.forEach(col => {
    let val = item[col.name];
    if (getInputType(col.type) === 'datetime' && val) {
      const d = new Date(val);
      const z = n => (n < 10 ? '0' : '') + n;
      val = `${d.getFullYear()}-${z(d.getMonth() + 1)}-${z(d.getDate())}T${z(d.getHours())}:${z(d.getMinutes())}`;
    }
    formModel[col.name] = val;
  });
  formModel.id = item.id;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
}

async function saveData() {
  try {
    if (isEditing.value) {
      await api.updateData(selectedTable.value.name, formModel.id, formModel);
    } else {
      await api.createData(selectedTable.value.name, formModel);
    }
    closeModal();
    fetchData();
  } catch (err) {
    alert('保存失败: ' + (err.response?.data?.message || err.message));
  }
}

async function confirmDelete(item) {
  if (confirm(`确定要删除这条记录吗?`)) {
    try {
      await api.deleteData(selectedTable.value.name, item.id);
      fetchData();
    } catch (err) {
      alert('删除失败: ' + (err.response?.data?.message || err.message));
    }
  }
}

// Import Operations
function openImportModal() {
  selectedFile.value = null;
  importResults.value = null;
  showImportModal.value = true;
}

function closeImportModal() {
  showImportModal.value = false;
}

function handleFileChange(event) {
  selectedFile.value = event.target.files[0];
}

async function executeImport() {
  if (!selectedFile.value) return;
  importing.value = true;
  importResults.value = null;
  try {
    const res = await api.importData(selectedTable.value.name, selectedFile.value);
    importResults.value = res.data;
    fetchData();
  } catch (err) {
    alert('导入出错: ' + (err.response?.data?.message || err.message));
  } finally {
    importing.value = false;
  }
}

onMounted(fetchTables);
</script>

<style scoped>
.data-management {
  color: #fff;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 8rem);
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.title { margin: 0; font-weight: 600; }

.management-layout {
  display: flex;
  gap: 1.5rem;
  flex-grow: 1;
  overflow: hidden;
}

/* Sidebar */
.table-sidebar {
  width: 240px;
  background-color: var(--color-bg-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
}

.sidebar-title {
  padding: 1rem;
  font-weight: bold;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-muted);
}

.table-list {
  list-style: none;
  padding: 0.5rem 0;
  margin: 0;
  overflow-y: auto;
}

.table-list li {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  color: var(--color-text-muted);
  transition: all 0.2s;
}

.table-list li:hover {
  background-color: rgba(255,255,255,0.05);
  color: #fff;
}

.table-list li.active {
  background-color: var(--color-primary);
  color: #fff;
}

/* Content */
.table-content {
  flex-grow: 1;
  background-color: var(--color-bg-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 1.5rem;
}

.table-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.selected-table-name { margin: 0; font-size: 1.2rem; }

.search-box { display: flex; gap: 0.5rem; }
.search-box input {
  background-color: var(--color-bg-deep);
  border: 1px solid var(--color-border);
  color: #fff;
  padding: 0.4rem 0.8rem;
  border-radius: var(--radius-sm);
  width: 250px;
}

/* Table */
.table-container {
  flex-grow: 1;
  overflow-y: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background-color: rgba(255,255,255,0.05);
  color: var(--color-text-muted);
  text-align: left;
  padding: 0.75rem;
  position: sticky;
  top: 0;
  font-size: 0.9rem;
}

td {
  padding: 0.75rem;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-main);
}

tr:hover td { background-color: rgba(255, 255, 255, 0.03); }
tr.selected td { background-color: rgba(59, 130, 246, 0.1); }

.checkbox-col, .checkbox-cell { width: 40px; text-align: center; }
.actions-col { width: 100px; text-align: center; }
.actions-cell { text-align: center; display: flex; justify-content: center; gap: 0.5rem; }

/* Buttons */
.btn {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  border: none;
  font-weight: 500;
  transition: all 0.2s;
}

.btn:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-primary { background-color: var(--color-primary); color: #fff; }
.btn-secondary { background-color: #334155; color: #fff; }
.btn-danger { background-color: var(--color-danger); color: #fff; }
.btn-cancel { background-color: #334155; color: #fff; }
.btn-search { background-color: #334155; color: #fff; }

.btn-icon {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
}

.edit-btn:hover { color: var(--color-primary); }
.delete-btn:hover { color: var(--color-danger); }

/* Pagination */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.page-controls { display: flex; align-items: center; gap: 1rem; }
.page-controls button {
  background-color: var(--color-bg-deep);
  color: #fff;
  border: 1px solid var(--color-border);
  padding: 0.3rem 0.6rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
}
.page-controls button:disabled { opacity: 0.5; }

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background-color: var(--color-bg-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  width: 500px;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid var(--color-border);
  display: flex; justify-content: space-between; align-items: center;
}

.modal-header h3 { margin: 0; color: var(--color-text-main); }
.close-btn { background: none; border: none; color: var(--color-text-muted); font-size: 1.5rem; cursor: pointer; }

.modal-body { padding: 1.5rem; overflow-y: auto; }

.form-group { margin-bottom: 1.2rem; }
.form-group label { display: block; margin-bottom: 0.5rem; color: var(--color-text-muted); font-size: 0.9rem; }
.form-input {
  width: 100%;
  background-color: var(--color-bg-deep);
  border: 1px solid var(--color-border);
  color: #fff;
  padding: 0.75rem;
  border-radius: var(--radius-sm);
  outline: none;
}
.form-input:focus { border-color: var(--color-primary); }
.required { color: var(--color-danger); }

.form-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; }

/* Import specific */
.import-instructions { margin-bottom: 1.5rem; color: var(--color-text-muted); font-size: 0.9rem; }
.file-upload { margin-bottom: 1.5rem; }
.import-results { margin-top: 1rem; padding: 1rem; background-color: var(--color-bg-deep); border-radius: var(--radius-sm); }
.success { color: var(--color-success); }
.error { color: var(--color-danger); }
.text-center { text-align: center; color: var(--color-text-muted); padding: 2rem; }
</style>
