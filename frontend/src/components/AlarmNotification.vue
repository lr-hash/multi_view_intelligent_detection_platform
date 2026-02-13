<template>
  <div class="notification-system">
    <!-- Toast 容器 (黄色预警) -->
    <div class="toast-container" v-if="yellowAlarms.length > 0">
      <transition-group name="list" tag="div">
        <div v-for="alarm in yellowAlarms" :key="alarm.id" class="alarm-card yellow">
          <div class="alarm-header">
            <span class="alarm-type">⚠️ {{ alarm.type }}</span>
            <span class="alarm-time">{{ formatTime(alarm.timestamp) }}</span>
            <button class="close-btn" @click="dismiss(alarm.id)">×</button>
          </div>
          <div class="alarm-body">
            <div class="alarm-message">{{ alarm.message }}</div>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- 全屏模态框 (红色危急报警) -->
    <div class="alarm-modal-overlay" v-if="activeRedAlarm">
      <div class="alarm-modal">
        <div class="modal-header">
          <div class="warning-icon">🚨</div>
          <h2 class="modal-title">危急报警：{{ activeRedAlarm.type }}</h2>
        </div>
        <div class="modal-body">
          <div class="alarm-main-info">
            <div class="info-label">报警信息</div>
            <div class="info-text">{{ activeRedAlarm.message }}</div>
          </div>
          <div class="alarm-stats">
            <div class="stat-item">
              <span class="label">当前数值:</span>
              <span class="value">{{ activeRedAlarm.value }}</span>
            </div>
            <div class="stat-item">
              <span class="label">安全阈值:</span>
              <span class="value">{{ activeRedAlarm.threshold }}</span>
            </div>
            <div class="stat-item">
              <span class="label">触发时间:</span>
              <span class="value">{{ formatTime(activeRedAlarm.timestamp) }}</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="ignoreAlarm" class="action-btn ignore">忽略 (暂不处理)</button>
          <button @click="viewData" class="action-btn view">查看实时数据</button>
          <button @click="viewLogs" class="action-btn logs">查看报警日志</button>
        </div>
      </div>
    </div>
    
    <!-- 音频提示 -->
    <audio ref="alertAudio" src="https://assets.mixkit.co/active_storage/sfx/951/951-preview.mp3" loop></audio>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import websocket from '@/services/websocket';

const router = useRouter();
const alarms = ref([]);
const alertAudio = ref(null);

// 分类报警
const yellowAlarms = computed(() => alarms.value.filter(a => a.level === 'YELLOW'));
const redAlarms = computed(() => alarms.value.filter(a => a.level === 'RED'));
const activeRedAlarm = computed(() => redAlarms.value[0] || null);

// 监听红色报警播放声音
watch(activeRedAlarm, (newVal) => {
  if (newVal && alertAudio.value) {
    alertAudio.value.play().catch(e => console.log("Audio play blocked by browser"));
  } else if (!newVal && alertAudio.value) {
    alertAudio.value.pause();
    alertAudio.value.currentTime = 0;
  }
});

function handleNewAlarm(data) {
  console.log("ALARM RECEIVED:", data);
  // 防止重复
  if (alarms.value.some(a => a.id === data.id)) return;
  
  alarms.value.push(data);
  
  // 黄色预警 15秒后自动关闭
  if (data.level === 'YELLOW') {
    setTimeout(() => {
      dismiss(data.id);
    }, 15000);
  }
}

function dismiss(id) {
  const index = alarms.value.findIndex(a => a.id === id);
  if (index !== -1) {
    alarms.value.splice(index, 1);
  }
}

function formatTime(ts) {
  return new Date(ts).toLocaleTimeString();
}

// 按钮操作
function ignoreAlarm() {
  if (activeRedAlarm.value) {
    dismiss(activeRedAlarm.value.id);
  }
}

function viewData() {
  const type = activeRedAlarm.value?.type?.toLowerCase();
  if (type.includes('pressure') || type.includes('deformation')) {
    router.push({ name: 'dashboard' });
  } else {
    router.push({ name: 'visualization' });
  }
  ignoreAlarm();
}

function viewLogs() {
  router.push({ name: 'alarm-history' });
  ignoreAlarm();
}

onMounted(() => {
  websocket.on('new_alarm', handleNewAlarm);
});

onUnmounted(() => {
  websocket.off('new_alarm');
});
</script>

<style scoped>
.notification-system {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 10000;
}

/* Toast Container */
.toast-container {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 320px;
  pointer-events: auto;
}

.alarm-card {
  background-color: #1a2952;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
  margin-bottom: 12px;
  color: #fff;
  border-left: 6px solid #ccc;
  overflow: hidden;
}

.alarm-card.yellow {
  border-left-color: #ffc107;
  background: linear-gradient(145deg, #1a2952, #2c250b);
}

.alarm-header {
  display: flex;
  justify-content: space-between;
  padding: 10px 15px;
  background: rgba(255, 255, 255, 0.05);
  font-weight: bold;
}

.alarm-body {
  padding: 12px 15px;
}

/* Modal Overlay */
.alarm-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(220, 53, 69, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: auto;
  backdrop-filter: blur(4px);
  animation: pulse-bg 2s infinite;
}

@keyframes pulse-bg {
  0% { background-color: rgba(220, 53, 69, 0.1); }
  50% { background-color: rgba(220, 53, 69, 0.3); }
  100% { background-color: rgba(220, 53, 69, 0.1); }
}

.alarm-modal {
  background-color: #1a2952;
  width: 500px;
  border: 2px solid #dc3545;
  border-radius: 12px;
  box-shadow: 0 0 40px rgba(220, 53, 69, 0.6);
  color: #fff;
  overflow: hidden;
  animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}

.modal-header {
  background-color: #dc3545;
  padding: 20px;
  text-align: center;
}

.warning-icon {
  font-size: 3rem;
  margin-bottom: 10px;
}

.modal-title {
  margin: 0;
  font-size: 1.5rem;
}

.modal-body {
  padding: 25px;
}

.alarm-main-info {
  margin-bottom: 20px;
  border-bottom: 1px solid #2a3f78;
  padding-bottom: 15px;
}

.info-label {
  color: #8fa3cf;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.info-text {
  font-size: 1.2rem;
  font-weight: bold;
}

.alarm-stats {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
}

.stat-item .label { color: #8fa3cf; }
.stat-item .value { font-family: monospace; font-size: 1.1rem; color: #ffc107; }

.modal-footer {
  padding: 20px;
  background: rgba(0,0,0,0.2);
  display: flex;
  gap: 12px;
}

.action-btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.ignore { background-color: #6c757d; color: white; }
.action-btn.view { background-color: #007bff; color: white; }
.action-btn.logs { background-color: #17a2b8; color: white; }

.action-btn:hover {
  filter: brightness(1.2);
  transform: translateY(-2px);
}

.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.5rem;
  cursor: pointer;
}

/* List Transitions */
.list-enter-active, .list-leave-active { transition: all 0.5s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateX(30px); }
</style>
