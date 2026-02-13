<template>
  <div class="user-mgmt-container">
    <div class="page-header">
      <h2>用户权限管理</h2>
      <button @click="openAddModal" class="add-btn">
        <span>+</span> 新增人员
      </button>
    </div>

    <div v-if="isLoading" class="loading-box">加载人员列表中...</div>
    <div v-else class="table-wrapper">
      <table class="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>角色权限</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td class="username">{{ user.username }}</td>
            <td>
              <span :class="['role-badge', user.role.toLowerCase()]">
                {{ user.role === 'ADMIN' ? '系统管理员' : '普通用户' }}
              </span>
            </td>
            <td class="actions">
              <button @click="openEditModal(user)" class="edit-link">编辑</button>
              <button @click="confirmDelete(user)" class="delete-link" :disabled="user.id === currentUserId">
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 新增/编辑 弹窗 -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-card">
        <h3>{{ isEdit ? '编辑人员信息' : '新增平台人员' }}</h3>
        <form @submit.prevent="saveUser">
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="form.username" required :disabled="isEdit">
          </div>
          <div class="form-group">
            <label>{{ isEdit ? '修改密码 (留空则不修改)' : '登录密码' }}</label>
            <input type="password" v-model="form.password" :required="!isEdit">
          </div>
          <div class="form-group">
            <label>角色权限</label>
            <select v-model="form.role">
              <option value="USER">普通用户</option>
              <option value="ADMIN">系统管理员</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showModal = false" class="cancel-btn">取消</button>
            <button type="submit" class="submit-btn">保存生效</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();
const currentUserId = authStore.user?.id;

const users = ref([]);
const isLoading = ref(true);
const showModal = ref(false);
const isEdit = ref(false);
const editingId = ref(null);

const form = reactive({
  username: '',
  password: '',
  role: 'USER'
});

async function fetchUsers() {
  isLoading.value = true;
  try {
    const res = await api.getDataList('auth/users'); // Note: We need to ensure api.js has a generic way or add this
    // Since api.js is currently structured for management/, we might need to add specific call
    const response = await axios_instance.get('/api/v1/auth/users');
    users.value = response.data;
  } catch (error) {
    // Fallback to direct axios if api object doesn't have it yet
    try {
        const response = await api.getUsers(); // We will add this to api.js
        users.value = response.data;
    } catch (e) {
        console.error("Failed to fetch users:", e);
    }
  } finally {
    isLoading.value = false;
  }
}

// Reuse the existing api client pattern
import axios from 'axios';
const axios_instance = axios.create({ baseURL: '/api/v1' });
axios_instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

async function loadUsers() {
    isLoading.value = true;
    try {
        const res = await axios_instance.get('/auth/users');
        users.value = res.data;
    } catch (e) {
        alert("只有管理员可以访问此页面");
    } finally {
        isLoading.value = false;
    }
}

function openAddModal() {
  isEdit.value = false;
  form.username = '';
  form.password = '';
  form.role = 'USER';
  showModal.value = true;
}

function openEditModal(user) {
  isEdit.value = true;
  editingId.value = user.id;
  form.username = user.username;
  form.password = '';
  form.role = user.role;
  showModal.value = true;
}

async function saveUser() {
  try {
    if (isEdit.value) {
      await axios_instance.put(`/auth/users/${editingId.value}`, form);
    } else {
      await axios_instance.post('/auth/users', form);
    }
    showModal.value = false;
    loadUsers();
  } catch (e) {
    alert(e.response?.data?.message || "操作失败");
  }
}

async function confirmDelete(user) {
  if (confirm(`确定要删除用户 "${user.username}" 吗？此操作不可撤销。`)) {
    try {
      await axios_instance.delete(`/auth/users/${user.id}`);
      loadUsers();
    } catch (e) {
      alert("删除失败");
    }
  }
}

onMounted(() => {
  loadUsers();
});
</script>

<style scoped>
.user-mgmt-container {
  padding: 1rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.add-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.table-wrapper {
  background: #1a2952;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #2a3f78;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  color: #fff;
}

.user-table th, .user-table td {
  padding: 1.2rem;
  text-align: left;
  border-bottom: 1px solid #2a3f78;
}

.user-table th {
  background: rgba(255,255,255,0.05);
  color: #94a3b8;
  font-size: 0.9rem;
}

.username { font-weight: bold; color: #3b82f6; }

.role-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}
.role-badge.admin { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
.role-badge.user { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }

.actions button {
  background: none;
  border: none;
  margin-right: 1rem;
  cursor: pointer;
  font-size: 0.9rem;
}
.edit-link { color: #3b82f6; }
.delete-link { color: #ef4444; }
.delete-link:disabled { opacity: 0.3; cursor: not-allowed; }

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.7);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}

.modal-card {
  background: #1a2952;
  width: 400px;
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid #3b82f6;
}

.form-group { margin-bottom: 1.2rem; }
.form-group label { display: block; margin-bottom: 0.5rem; color: #94a3b8; font-size: 0.9rem; }
.form-group input, .form-group select {
  width: 100%;
  background: #0f172a;
  border: 1px solid #2a3f78;
  padding: 0.8rem;
  border-radius: 8px;
  color: white;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}
.modal-actions button { flex: 1; padding: 0.8rem; border-radius: 8px; cursor: pointer; border: none; font-weight: bold; }
.cancel-btn { background: #334155; color: white; }
.submit-btn { background: #3b82f6; color: white; }
</style>