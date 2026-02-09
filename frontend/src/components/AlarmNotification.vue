<template>
  <div class="notification-container" v-if="alarms.length > 0">
    <transition-group name="list" tag="div">
      <div v-for="alarm in alarms" :key="alarm.id" :class="['alarm-card', alarm.level.toLowerCase()]">
        <div class="alarm-header">
          <span class="alarm-type">{{ alarm.type }}</span>
          <span class="alarm-time">{{ new Date(alarm.timestamp).toLocaleTimeString() }}</span>
          <button class="close-btn" @click="dismiss(alarm.id)">×</button>
        </div>
        <div class="alarm-body">
          <div class="alarm-message">{{ alarm.message }}</div>
          <div class="alarm-value">
            Value: {{ alarm.value }} (Threshold: {{ alarm.threshold }})
          </div>
        </div>
        <div class="alarm-actions">
          <button @click="viewDetails(alarm)" class="view-btn">查看详情</button>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import websocket from '@/services/websocket';

const alarms = ref([]);
const router = useRouter();

function handleNewAlarm(data) {
  // Add new alarm to the list
  alarms.value.push(data);
  
  // Auto-dismiss after 10 seconds
  setTimeout(() => {
    dismiss(data.id);
  }, 10000);
}

function dismiss(id) {
  const index = alarms.value.findIndex(a => a.id === id);
  if (index !== -1) {
    alarms.value.splice(index, 1);
  }
}

function viewDetails(alarm) {
  // Navigate to alarm history or relevant page
  router.push({ name: 'alarm-history' });
  dismiss(alarm.id);
}

onMounted(() => {
  websocket.on('new_alarm', handleNewAlarm);
});

onUnmounted(() => {
  websocket.off('new_alarm');
});
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 320px;
  z-index: 9999;
  pointer-events: none; /* Allow clicks to pass through empty space */
}

.alarm-card {
  pointer-events: auto; /* Re-enable clicks on cards */
  background-color: #1a2952;
  border-left: 5px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  margin-bottom: 10px;
  color: #fff;
  overflow: hidden;
}

.alarm-card.red {
  border-left-color: #f44336;
  background-color: #2c0b0e;
}

.alarm-card.yellow {
  border-left-color: #ffeb3b;
  background-color: #2c250b;
}

.alarm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: rgba(255, 255, 255, 0.1);
  font-weight: bold;
}

.alarm-type {
  text-transform: uppercase;
  font-size: 0.9rem;
}

.alarm-time {
  font-size: 0.8rem;
  color: #ccc;
}

.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.2rem;
  cursor: pointer;
  line-height: 1;
}

.alarm-body {
  padding: 10px 12px;
}

.alarm-message {
  font-size: 0.95rem;
  margin-bottom: 5px;
}

.alarm-value {
  font-size: 0.85rem;
  color: #aaa;
}

.alarm-actions {
  padding: 8px 12px;
  text-align: right;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.view-btn {
  background: none;
  border: 1px solid #4a90e2;
  color: #4a90e2;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s;
}

.view-btn:hover {
  background-color: #4a90e2;
  color: #fff;
}

/* Transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
