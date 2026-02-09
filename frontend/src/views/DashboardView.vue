<template>
  <div class="dashboard">
    <div class="metrics-grid">
      <!-- Metric cards remain the same -->
      <div class="metric-card">
        <div class="icon-wrapper pressure"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg></div>
        <div class="text-wrapper"><h3>支架平均阻力</h3><p class="value">{{ pressure }} <span>MPa</span></p></div>
      </div>
      <div class="metric-card">
        <div class="icon-wrapper microseismic"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10s5 2 7 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18.5a.5.5 0 100-1 .5.5 0 000 1zM12 12.5a.5.5 0 100-1 .5.5 0 000 1zM12 6.5a.5.5 0 100-1 .5.5 0 000 1z" /></svg></div>
        <div class="text-wrapper"><h3>最新微震能量</h3><p class="value">{{ microseismic }} <span>J</span></p></div>
      </div>
      <div class="metric-card">
        <div class="icon-wrapper deformation"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v-4m0 0h-4m4 0l-5-5" /></svg></div>
        <div class="text-wrapper"><h3>巷道累计位移</h3><p class="value">{{ deformation }} <span>mm</span></p></div>
      </div>
      <div class="metric-card">
        <div class="icon-wrapper alarms"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg></div>
        <div class="text-wrapper"><h3>今日报警次数</h3><p class="value">{{ alarms }}</p></div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-container">
        <h3>矿压实时趋势</h3>
        <Line v-if="pressureChartData.datasets.length" :data="pressureChartData" :options="chartOptions" />
      </div>
      <div class="chart-container">
        <h3>近24小时微震频次</h3>
        <Bar v-if="frequencyChartData.datasets.length" :data="frequencyChartData" :options="chartOptions" />
      </div>
      <div class="chart-container full-width">
        <h3>巷道变形多点趋势</h3>
        <Line v-if="deformationChartData.datasets.length" :data="deformationChartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import api from '@/services/api';
import { Line, Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

// --- Data ---
const pressure = ref('N/A'), microseismic = ref('N/A'), deformation = ref('N/A'), alarms = ref('N/A');
const pressureChartData = reactive({ labels: [], datasets: [] });
const frequencyChartData = reactive({ labels: [], datasets: [] });
const deformationChartData = reactive({ labels: [], datasets: [] });
let metricsIntervalId, trendsIntervalId;

const chartOptions = reactive({
  responsive: true, maintainAspectRatio: false,
  scales: { y: { beginAtZero: false, ticks: { color: '#c0c5d6' } }, x: { ticks: { color: '#c0c5d6' } } },
  plugins: { legend: { labels: { color: '#c0c5d6' } } }
});

// --- Methods ---
async function fetchAllData() {
  try {
    const [metricsRes, pressureRes, freqRes, deformRes] = await Promise.all([
      api.getDashboardCoreMetrics(),
      api.getPressureTrendData('1h'),
      api.getMicroseismicFrequency('24h'),
      api.getDeformationTrend('24h')
    ]);
    
    // Metrics
    const metrics = metricsRes.data;
    pressure.value = metrics.strata_pressure.current_val;
    microseismic.value = metrics.microseismic.latest_energy;
    deformation.value = metrics.deformation.total_offset;
    alarms.value = metrics.microseismic.daily_count;

    // Pressure Chart
    pressureChartData.labels = pressureRes.data.map(p => new Date(p.x).toLocaleTimeString());
    pressureChartData.datasets = [{ label: '矿压 (MPa)', data: pressureRes.data.map(p => p.y), backgroundColor: 'hsla(198, 100%, 50%, 0.3)', borderColor: 'hsla(198, 100%, 50%, 1)', tension: 0.3, fill: true }];

    // Frequency Chart
    frequencyChartData.labels = freqRes.data.map(p => p.x);
    frequencyChartData.datasets = [{ label: '微震次数', data: freqRes.data.map(p => p.y), backgroundColor: '#ffc107' }];
    
    // Deformation Chart
    const colors = ['#28a745', '#17a2b8', '#fd7e14'];
    deformationChartData.labels = deformRes.data.labels;
    deformationChartData.datasets = deformRes.data.datasets.map((ds, index) => ({
        ...ds,
        borderColor: colors[index % colors.length],
        tension: 0.1,
        fill: false,
    }));

  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  }
}

// --- Lifecycle ---
onMounted(() => {
  fetchAllData();
  metricsIntervalId = setInterval(fetchAllData, 10000); // Refresh all data every 10s
});

onUnmounted(() => {
  clearInterval(metricsIntervalId);
});
</script>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.metric-card {
  background-color: #1a2952;
  border: 1px solid #2a3f78;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.icon-wrapper {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1.5rem;
}
.icon-wrapper svg { width: 28px; height: 28px; color: #fff; }
.pressure { background-color: #007bff; }
.microseismic { background-color: #ffc107; }
.deformation { background-color: #28a745; }
.alarms { background-color: #dc3545; }
.text-wrapper h3 { margin: 0 0 0.5rem 0; color: #c0c5d6; font-size: 1rem; font-weight: 400; }
.text-wrapper .value { font-size: 1.8rem; font-weight: bold; color: #fff; margin: 0; }
.text-wrapper .value span { font-size: 1rem; color: #c0c5d6; margin-left: 0.25rem; }

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.chart-container {
  background-color: #1a2952;
  border: 1px solid #2a3f78;
  border-radius: 8px;
  padding: 1.5rem;
  height: 400px;
}
.chart-container.full-width {
  grid-column: 1 / -1;
}

.chart-container h3 {
  margin-bottom: 1.5rem;
}
</style>
