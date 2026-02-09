<template>
  <div class="report-container" v-if="report && !isLoading">
    <h2>{{ report.report_title }}</h2>
    <p class="meta-info">报告生成时间: {{ new Date(report.generated_at).toLocaleString() }}</p>

    <div class="report-section">
      <h3>结论与建议</h3>
      <p><strong>结论:</strong> {{ report.summary.conclusion }}</p>
      <p><strong>建议:</strong> {{ report.summary.recommendation }}</p>
    </div>

    <div class="report-section">
      <h3>评价指标</h3>
      <div class="metrics-grid">
        <div class="metric-card" v-for="(metric, key) in report.evaluation_indices" :key="key">
          <h4>{{ getMetricName(key) }}</h4>
          <p class="value">{{ metric.value }} {{ metric.unit || '' }}</p>
          <p class="level" :class="metric.level.toLowerCase()">等级: {{ metric.level }}</p>
        </div>
      </div>
    </div>

    <div class="report-section">
      <h3>数据对比分析</h3>
      <div v-for="(comparison, key) in report.data_comparison" :key="key" class="comparison-section">
        <h4>{{ getComparisonName(key) }}</h4>
        <table class="comparison-table">
          <thead>
            <tr>
              <th>指标</th>
              <th>压裂前</th>
              <th>压裂后</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, metric_key) in comparison.pre_fracturing" :key="metric_key">
              <td>{{ getSubMetricName(metric_key) }}</td>
              <td>{{ comparison.pre_fracturing[metric_key] }}</td>
              <td>{{ comparison.post_fracturing[metric_key] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div v-else-if="isLoading" class="loading">加载报告中...</div>
  <div v-else class="error">无法加载报告。</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/services/api';

const report = ref(null);
const isLoading = ref(true);
const route = useRoute();

const metricNames = {
  roof_stability_index: '顶板稳定系数',
  fracturing_efficiency: '压裂有效率',
  pressure_control_effect: '矿压控制效果',
};

const comparisonNames = {
  pressure: '矿压数据对比',
  microseismic: '微震数据对比',
  deformation: '变形数据对比',
};

const subMetricNames = {
  max: '最大值',
  avg: '平均值',
  fluctuation: '波动系数',
  count: '事件数',
  total_energy: '总能量',
  max_rate: '最大速率',
  total: '累计总量'
};

const getMetricName = (key) => metricNames[key] || key;
const getComparisonName = (key) => comparisonNames[key] || key;
const getSubMetricName = (key) => subMetricNames[key] || key;

async function fetchReport() {
  isLoading.value = true;
  const boreholeId = route.params.boreholeId;
  try {
    const response = await api.getEvaluationReport(boreholeId);
    report.value = response.data;
  } catch (error) {
    console.error(`Error fetching evaluation report for borehole ${boreholeId}:`, error);
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  fetchReport();
});
</script>

<style scoped>
.report-container {
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}
.meta-info {
  font-size: 0.9rem;
  color: #c0c5d6;
  margin-bottom: 2rem;
}
.report-section {
  margin-bottom: 2.5rem;
}
.report-section h3 {
  border-bottom: 2px solid hsla(198, 100%, 50%, 0.3);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
.metric-card {
  background: #1a2952;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
}
.metric-card .value {
  font-size: 1.8rem;
  font-weight: bold;
  color: hsla(198, 100%, 70%, 1);
}
.metric-card .level {
  font-weight: bold;
}
.level.稳定, .level.有效, .level.良好 { color: #4CAF50; }
.level.一般 { color: #ffeb3b; }
.level.无效, .level.不合格 { color: #f44336; }

.comparison-section {
  margin-bottom: 2rem;
}
.comparison-table {
  width: 100%;
  border-collapse: collapse;
}
.comparison-table th, .comparison-table td {
  border: 1px solid #2a3f78;
  padding: 0.5rem 1rem;
}
.comparison-table th {
  background-color: #1a2952;
}
</style>
