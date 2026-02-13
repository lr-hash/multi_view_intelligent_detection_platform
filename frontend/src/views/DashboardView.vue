<template>
  <div class="dashboard">
    <!-- 顶部操作栏 -->
    <div class="dashboard-header">
      <h2 class="title">煤矿安全智能看板</h2>
      <div class="controls">
        <select v-model="timeRange" @change="fetchAllData" class="range-selector">
          <option value="1h">最近 1 小时</option>
          <option value="24h">最近 24 小时</option>
          <option value="7d">最近 7 天</option>
        </select>
        <button @click="fetchAllData" class="refresh-btn">手动刷新</button>
      </div>
    </div>

    <!-- 核心指标栅格 -->
    <div class="metrics-grid">
      <!-- 综合稳定指数 (融合算法体现) -->
      <div class="metric-card gauge-card">
        <stability-gauge :score="fusionData.score" :level="fusionData.level" />
      </div>

      <metric-card title="支架平均阻力" :value="metrics.pressure" unit="MPa" type="pressure">
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
        </template>
      </metric-card>
      
      <metric-card title="最新微震能量" :value="metrics.microseismic" unit="J" type="microseismic">
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10s5 2 7 0z" /></svg>
        </template>
      </metric-card>

      <metric-card title="巷道累计位移" :value="metrics.deformation" unit="mm" type="deformation">
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v-4m0 0h-4m4 0l-5-5" /></svg>
        </template>
      </metric-card>
    </div>

    <!-- 图表区域 -->
    <div class="charts-grid">
      <div class="chart-container">
        <h3 class="chart-title">矿压实时趋势</h3>
        <div class="canvas-wrapper">
          <Line v-if="pressureChartData.datasets.length" :data="pressureChartData" :options="pressureOptions" />
        </div>
      </div>
      <div class="chart-container">
        <h3 class="chart-title">微震频次分布</h3>
        <div class="canvas-wrapper">
          <Bar v-if="frequencyChartData.datasets.length" :data="frequencyChartData" :options="frequencyOptions" />
        </div>
      </div>
      <div class="chart-container full-width">
        <h3 class="chart-title">巷道变形演化速率</h3>
        <div class="canvas-wrapper">
          <Line v-if="deformationChartData.datasets.length" :data="deformationChartData" :options="deformationOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue';
import api from '@/services/api';
import MetricCard from '@/components/MetricCard.vue';
import StabilityGauge from '@/components/StabilityGauge.vue';
import { Line, Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler } from 'chart.js';
import annotationPlugin from 'chartjs-plugin-annotation';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler, annotationPlugin);

// --- State ---
const timeRange = ref('24h');
const metrics = reactive({
  pressure: 'N/A',
  microseismic: 'N/A',
  deformation: 'N/A',
  alarms: 'N/A'
});

const fusionData = reactive({
  score: 100,
  level: 'Green'
});

const thresholds = reactive({
  pressure: { yellow: 35, red: 45 },
  deformation: { yellow: 8, red: 15 },
  seismic: { yellow: 50000, red: 100000 }
});

const pressureChartData = reactive({ labels: [], datasets: [] });
const frequencyChartData = reactive({ labels: [], datasets: [] });
const deformationChartData = reactive({ labels: [], datasets: [] });

let autoRefreshId;

// --- Chart Options Factories ---
const createBaseOptions = (unit, thresholdKey = null) => {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: { 
        grid: { color: '#2a3f78' }, 
        ticks: { color: '#c0c5d6' },
        title: {
          display: true,
          text: `单位: ${unit}`,
          color: '#8fa3cf',
          font: { size: 12 }
        }
      },
      x: { grid: { display: false }, ticks: { color: '#c0c5d6' } }
    },
    plugins: {
      legend: { position: 'top', labels: { color: '#c0c5d6', boxWidth: 12 } },
      annotation: {
        annotations: {}
      }
    }
  };

  if (thresholdKey && thresholds[thresholdKey]) {
    options.plugins.annotation.annotations = {
      yellowLine: {
        type: 'line',
        yMin: thresholds[thresholdKey].yellow,
        yMax: thresholds[thresholdKey].yellow,
        borderColor: 'rgba(255, 193, 7, 0.8)',
        borderWidth: 2,
        borderDash: [6, 6],
        label: {
          display: true,
          content: `警告: ${thresholds[thresholdKey].yellow}${unit}`,
          position: 'end',
          backgroundColor: 'rgba(255, 193, 7, 0.8)',
          color: '#000',
          font: { size: 10 }
        }
      },
      redLine: {
        type: 'line',
        yMin: thresholds[thresholdKey].red,
        yMax: thresholds[thresholdKey].red,
        borderColor: 'rgba(220, 53, 69, 0.8)',
        borderWidth: 2,
        label: {
          display: true,
          content: `异常: ${thresholds[thresholdKey].red}${unit}`,
          position: 'end',
          backgroundColor: 'rgba(220, 53, 69, 0.8)',
          color: '#fff',
          font: { size: 10 }
        }
      }
    };
  }
  return options;
};

const pressureOptions = computed(() => createBaseOptions('MPa', 'pressure'));
const frequencyOptions = computed(() => createBaseOptions('次', null)); // Frequency usually doesn't have fixed safety thresholds in same way
const deformationOptions = computed(() => createBaseOptions('mm/d', 'deformation'));

// --- Methods ---
async function fetchAllData() {
  try {
    const [metricsRes, pressureRes, freqRes, deformRes, alarmConfigRes, fusionRes] = await Promise.all([
      api.getDashboardCoreMetrics(),
      api.getPressureTrendData(timeRange.value),
      api.getMicroseismicFrequency(timeRange.value),
      api.getDeformationTrend(timeRange.value),
      api.getAlarmConfig(),
      api.getDashboardFusionScore()
    ]);
    
    // Update fusion data
    fusionData.score = fusionRes.data.stability_score;
    fusionData.level = fusionRes.data.risk_level;

    // Update thresholds from server
    if (alarmConfigRes.data) {
      Object.assign(thresholds.pressure, alarmConfigRes.data.pressure);
      Object.assign(thresholds.deformation, alarmConfigRes.data.deformation);
      Object.assign(thresholds.seismic, alarmConfigRes.data.seismic);
    }

    // Update numerical metrics
    metrics.pressure = metricsRes.data.strata_pressure.current_val;
    metrics.microseismic = metricsRes.data.microseismic.latest_energy;
    metrics.deformation = metricsRes.data.deformation.total_offset;
    metrics.alarms = metricsRes.data.microseismic.daily_count;

    // Update charts
    updatePressureChart(pressureRes.data);
    updateFrequencyChart(freqRes.data);
    updateDeformationChart(deformRes.data);

  } catch (error) {
    console.error('Failed to sync dashboard:', error);
  }
}

function updatePressureChart(data) {
  pressureChartData.labels = data.map(p => new Date(p.x).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
  pressureChartData.datasets = [{
    label: '矿压 (MPa)',
    data: data.map(p => p.y),
    backgroundColor: 'rgba(0, 123, 255, 0.2)',
    borderColor: '#007bff',
    borderWidth: 2,
    pointRadius: 0,
    tension: 0.4,
    fill: true
  }];
}

function updateFrequencyChart(data) {
  frequencyChartData.labels = data.map(p => p.x);
  frequencyChartData.datasets = [{
    label: '事件频次',
    data: data.map(p => p.y),
    backgroundColor: '#ffc107'
  }];
}

function updateDeformationChart(data) {
  const colors = ['#28a745', '#17a2b8', '#fd7e14'];
  deformationChartData.labels = data.labels;
  deformationChartData.datasets = data.datasets.map((ds, index) => ({
    ...ds,
    borderColor: colors[index % colors.length],
    backgroundColor: 'transparent',
    borderWidth: 2,
    pointRadius: 2,
    tension: 0.1
  }));
}

onMounted(() => {
  fetchAllData();
  autoRefreshId = setInterval(fetchAllData, 30000); // 30s 自动刷新
});

onUnmounted(() => {
  clearInterval(autoRefreshId);
});
</script>

<style scoped>
.dashboard {
  padding: 1rem;
  color: var(--color-text-main);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 1rem;
}

.title {
  margin: 0;
  font-weight: 600;
  letter-spacing: 1px;
  font-size: 1.5rem;
}

.controls {
  display: flex;
  gap: 1rem;
}

.range-selector {
  background-color: var(--color-bg-panel);
  color: var(--color-text-main);
  border: 1px solid var(--color-border);
  padding: 0.4rem 1rem;
  border-radius: var(--radius-sm);
  outline: none;
}

.refresh-btn {
  background-color: rgba(59, 130, 246, 0.2);
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
  padding: 0.4rem 1.2rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.3s;
}

.refresh-btn:hover {
  background-color: var(--color-primary);
  color: #fff;
  box-shadow: 0 0 10px var(--color-primary-glow);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.gauge-card {
  padding: 0.5rem !important;
  justify-content: center;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.chart-container {
  background-color: var(--color-bg-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  height: 400px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.chart-container.full-width {
  grid-column: 1 / -1;
}

.chart-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--color-text-muted);
}

.canvas-wrapper {
  flex-grow: 1;
  min-height: 300px;
}
</style>
