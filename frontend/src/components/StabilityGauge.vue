<template>
  <div class="gauge-container">
    <svg viewBox="0 0 100 60" class="gauge">
      <!-- Background Arc -->
      <path 
        d="M 10 50 A 40 40 0 0 1 90 50" 
        fill="none" 
        stroke="#1e293b" 
        stroke-width="8" 
        stroke-linecap="round"
      />
      <!-- Active Value Arc -->
      <path 
        d="M 10 50 A 40 40 0 0 1 90 50" 
        fill="none" 
        :stroke="gaugeColor" 
        stroke-width="8" 
        stroke-linecap="round"
        :stroke-dasharray="dashArray"
        class="value-path"
      />
      <!-- Center Text -->
      <text x="50" y="45" text-anchor="middle" class="score-text" :fill="gaugeColor">{{ Math.round(score) }}</text>
      <text x="50" y="55" text-anchor="middle" class="unit-text">稳定指数</text>
    </svg>
    <div class="risk-badge" :style="{ backgroundColor: gaugeColor + '22', color: gaugeColor, borderColor: gaugeColor }">
      {{ riskLabel }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  score: { type: Number, default: 0 },
  level: { type: String, default: 'Green' }
});

const gaugeColor = computed(() => {
  if (props.level === 'Red') return '#ef4444';
  if (props.level === 'Yellow') return '#f59e0b';
  return '#10b981';
});

const riskLabel = computed(() => {
  if (props.level === 'Red') return '高危风险';
  if (props.level === 'Yellow') return '处于预警';
  return '状态稳定';
});

const dashArray = computed(() => {
  const totalLength = 126; // Approx length of the arc
  const percentage = props.score / 100;
  return `${totalLength * percentage} ${totalLength}`;
});
</script>

<style scoped>
.gauge-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.gauge {
  width: 100%;
  max-width: 240px;
}

.value-path {
  transition: stroke-dasharray 1s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.5s;
}

.score-text {
  font-size: 16px;
  font-weight: 800;
  font-family: 'Inter', monospace;
}

.unit-text {
  font-size: 6px;
  fill: #94a3b8;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.risk-badge {
  margin-top: -5px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  border: 1px solid;
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>