<template>
  <div class="config-container">
    <h2>系统参数与报警配置</h2>
    <div v-if="isLoading" class="loading-message">加载配置中...</div>
    <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-else class="config-grid">
      <!-- 接口参数配置 -->
      <div class="config-card">
        <h3>数据集成接口配置</h3>
        <form @submit.prevent="saveConfigurations" class="config-form">
          <div v-for="(config, interfaceId) in configurations" :key="interfaceId" class="interface-config-section">
            <h4>{{ interfaceId }}</h4>
            <div class="input-row">
              <div class="input-group">
                <label :for="`${interfaceId}-ip`">IP地址:</label>
                <input type="text" :id="`${interfaceId}-ip`" v-model="config.ip" />
              </div>
              <div class="input-group">
                <label :for="`${interfaceId}-port`">端口:</label>
                <input type="number" :id="`${interfaceId}-port`" v-model="config.port" />
              </div>
            </div>
          </div>
          <button type="submit" class="save-button">保存接口配置</button>
        </form>
      </div>

      <!-- 报警阈值配置 -->
      <div class="config-card">
        <h3>安全报警阈值设置</h3>
        <form @submit.prevent="saveAlarms" class="config-form">
          <div v-for="(thresholds, metric) in alarmConfigs" :key="metric" class="interface-config-section">
            <h4>{{ metric.toUpperCase() }} 阈值</h4>
            <div class="input-row">
              <div class="input-group">
                <label>红色预警 (RED):</label>
                <input type="number" step="0.1" v-model="thresholds.red" />
              </div>
              <div class="input-group">
                <label>黄色预警 (YELLOW):</label>
                <input type="number" step="0.1" v-model="thresholds.yellow" />
              </div>
            </div>
          </div>
          <button type="submit" class="save-button alarm-btn">保存报警阈值</button>
        </form>
      </div>
    </div>
    
    <div v-if="saveMessage" :class="['global-status', saveStatusClass]">
      {{ saveMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const configurations = ref({});
const alarmConfigs = ref({});
const isLoading = ref(true);
const errorMessage = ref('');
const saveMessage = ref('');
const saveStatusClass = ref('');

async function fetchData() {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const [configRes, alarmRes] = await Promise.all([
      api.getInterfaceConfig(),
      api.getAlarmConfig()
    ]);
    configurations.value = configRes.data;
    alarmConfigs.value = alarmRes.data;
  } catch (error) {
    console.error('Error fetching configurations:', error);
    errorMessage.value = '加载配置失败，请确保您具有管理员权限。';
  } finally {
    isLoading.value = false;
  }
}

async function saveConfigurations() {
  saveMessage.value = '正在保存接口配置...';
  try {
    await api.saveInterfaceConfig(configurations.value);
    showStatus('接口配置保存成功！', 'success');
  } catch (error) {
    showStatus('接口配置保存失败！', 'error');
  }
}

async function saveAlarms() {
  saveMessage.value = '正在保存报警阈值...';
  // 转换格式以适配后端 POST /alarms/config
  const payload = {
    "alarm_pressure_red": alarmConfigs.value.pressure.red,
    "alarm_pressure_yellow": alarmConfigs.value.pressure.yellow,
    "alarm_deformation_red": alarmConfigs.value.deformation.red,
    "alarm_deformation_yellow": alarmConfigs.value.deformation.yellow,
    "alarm_seismic_red": alarmConfigs.value.seismic.red,
    "alarm_seismic_yellow": alarmConfigs.value.seismic.yellow,
  };
  
  try {
    await api.saveAlarmConfig(payload);
    showStatus('报警阈值更新成功！', 'success');
  } catch (error) {
    showStatus('阈值更新失败！', 'error');
  }
}

function showStatus(msg, type) {
  saveMessage.value = msg;
  saveStatusClass.value = type;
  setTimeout(() => {
    saveMessage.value = '';
  }, 3000);
}

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.config-container {
  padding: 2rem;
}

h2 {
  margin-bottom: 2rem;
  color: #fff;
}

.config-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.config-card {
  background-color: #1a2952;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.config-card h3 {
  color: #a0d911;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #2a3f78;
  padding-bottom: 0.5rem;
}

.interface-config-section {
  margin-bottom: 1.5rem;
}

.interface-config-section h4 {
  color: #c0c5d6;
  margin-bottom: 0.75rem;
}

.input-row {
  display: flex;
  gap: 1rem;
}

.input-group {
  flex: 1;
}

.input-group label {
  display: block;
  margin-bottom: 0.4rem;
  font-size: 0.9rem;
  color: #8fa3cf;
}

input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #2a3f78;
  border-radius: 4px;
  background-color: #0d1a3c;
  color: #fff;
}

.save-button {
  width: 100%;
  padding: 0.75rem;
  margin-top: 1rem;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.alarm-btn {
  background-color: #f44336;
}

.global-status {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 2rem;
  border-radius: 8px;
  color: white;
  font-weight: bold;
  z-index: 100;
}

.global-status.success { background-color: #4CAF50; }
.global-status.error { background-color: #f44336; }
</style>

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
