<template>
  <div class="config-container">
    <h2>接口参数配置</h2>
    <div v-if="isLoading" class="loading-message">加载配置中...</div>
    <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-else class="config-form-wrapper">
      <form @submit.prevent="saveConfigurations" class="config-form">
        <div v-for="(config, interfaceId) in configurations" :key="interfaceId" class="interface-config-section">
          <h3>{{ interfaceId }}</h3>
          <div class="input-group">
            <label :for="`${interfaceId}-ip`">IP地址:</label>
            <input type="text" :id="`${interfaceId}-ip`" v-model="config.ip" />
          </div>
          <div class="input-group">
            <label :for="`${interfaceId}-port`">端口:</label>
            <input type="number" :id="`${interfaceId}-port`" v-model="config.port" />
          </div>
          <!-- Add more fields as per requirements -->
        </div>
        <button type="submit" class="save-button">保存配置</button>
        <div v-if="saveMessage" :class="['save-status-message', saveStatusClass]">
          {{ saveMessage }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const configurations = ref({});
const isLoading = ref(true);
const errorMessage = ref('');
const saveMessage = ref('');
const saveStatusClass = ref('');

async function fetchConfigurations() {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const response = await api.getInterfaceConfig();
    configurations.value = response.data;
  } catch (error) {
    console.error('Error fetching interface configurations:', error);
    errorMessage.value = '加载配置失败，请检查网络或稍后再试。';
  } finally {
    isLoading.value = false;
  }
}

async function saveConfigurations() {
  saveMessage.value = '正在保存...';
  saveStatusClass.value = '';
  try {
    const response = await api.saveInterfaceConfig(configurations.value);
    saveMessage.value = response.data.message || '配置保存成功！';
    saveStatusClass.value = 'success';
  } catch (error) {
    console.error('Error saving interface configurations:', error);
    saveMessage.value = error.response?.data?.message || '配置保存失败！';
    saveStatusClass.value = 'error';
  }
}

onMounted(() => {
  fetchConfigurations();
});
</script>

<style scoped>
.config-container {
  padding: 1rem;
}

h2 {
  margin-bottom: 1.5rem;
}

.loading-message, .error-message {
  text-align: center;
  padding: 1rem;
  font-size: 1.1rem;
}

.error-message {
  color: #f44336;
}

.config-form-wrapper {
  background-color: #1a2952;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 700px;
  margin: 0 auto;
}

.interface-config-section {
  margin-bottom: 2rem;
  border-bottom: 1px solid #2a3f78;
  padding-bottom: 1.5rem;
}

.interface-config-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.interface-config-section h3 {
  color: #a0d911; /* A distinct color for section titles */
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}

.input-group {
  margin-bottom: 1rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #c0c5d6;
  font-weight: bold;
}

.input-group input[type="text"],
.input-group input[type="number"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #2a3f78;
  border-radius: 4px;
  background-color: #0d1a3c;
  color: #ffffff;
  font-size: 1rem;
}

.save-button {
  display: block;
  width: 100%;
  padding: 0.8rem 1.5rem;
  margin-top: 2rem;
  background-color: hsla(198, 100%, 50%, 0.8);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button:hover {
  background-color: hsla(198, 100%, 50%, 1);
}

.save-status-message {
  margin-top: 1rem;
  text-align: center;
  font-weight: bold;
}

.save-status-message.success {
  color: #4CAF50;
}

.save-status-message.error {
  color: #f44336;
}
</style>
