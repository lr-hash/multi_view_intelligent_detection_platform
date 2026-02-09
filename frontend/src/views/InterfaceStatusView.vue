<template>
  <div class="interface-status-container">
    <h2>接口状态监测</h2>
    <div class="status-grid">
      <div v-for="(status, interfaceId) in interfaceStatuses" :key="interfaceId" class="status-card">
        <h3>{{ interfaceId }}</h3>
        <div :class="['status-indicator', status.status.toLowerCase()]"></div>
        <p class="status-text">{{ status.status }}</p>
        <p class="details-text">{{ status.latency || status.details || '无详细信息' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import api from '@/services/api';

const interfaceStatuses = ref({});
let intervalId;

async function fetchInterfaceStatuses() {
  try {
    const response = await api.getInterfaceStatus();
    interfaceStatuses.value = response.data;
  } catch (error) {
    console.error('Error fetching interface statuses:', error);
    // Set all statuses to error/offline on API call failure
    for (const key in interfaceStatuses.value) {
      interfaceStatuses.value[key].status = 'Error';
      interfaceStatuses.value[key].details = 'API调用失败';
    }
  }
}

onMounted(() => {
  fetchInterfaceStatuses();
  intervalId = setInterval(fetchInterfaceStatuses, 5000); // Refresh every 5 seconds
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<style scoped>
.interface-status-container {
  padding: 1rem;
}

h2 {
  color: var(--color-heading);
  margin-bottom: 1.5rem;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.status-card {
  background-color: var(--vt-c-black-soft);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.status-card h3 {
  color: var(--color-heading);
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.status-indicator {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  margin: 0.5rem auto;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.status-indicator.online {
  background-color: #4CAF50; /* Green */
}

.status-indicator.offline {
  background-color: #f44336; /* Red */
}

.status-indicator.unstable, .status-indicator.error {
  background-color: #ffeb3b; /* Yellow */
}

.status-text {
  font-size: 1.1rem;
  font-weight: bold;
  margin-top: 0.5rem;
  color: var(--color-text);
}

.details-text {
  font-size: 0.9rem;
  color: var(--vt-c-text-dark-2);
  margin-top: 0.5rem;
}
</style>
