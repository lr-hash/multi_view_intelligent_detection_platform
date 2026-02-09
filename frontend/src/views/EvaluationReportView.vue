<template>
  <div class="report-container" v-if="report && !isLoading">
    <div class="report-header">
      <h2>钻孔 #{{ report.borehole_id }} 压裂效果评价</h2>
      <button @click="downloadPDF" class="download-btn">下载 PDF 报告</button>
    </div>

    <div class="report-section">
      <h3>核心量化指标</h3>
      <div class="metrics-grid">
        <div class="metric-card">
          <h4>矿压降低率</h4>
          <p class="value">{{ report.metrics.pressure_reduction }}%</p>
        </div>
        <div class="metric-card">
          <h4>变形控制率</h4>
          <p class="value">{{ report.metrics.deformation_control }}%</p>
        </div>
        <div class="metric-card highlight">
          <h4>压裂有效率</h4>
          <p class="value">{{ report.metrics.efficiency }}%</p>
        </div>
        <div class="metric-card highlight">
          <h4>顶板稳定性指数</h4>
          <p class="value">{{ report.metrics.stability_index }}</p>
          <p class="level" :class="report.level">等级: {{ report.level }}</p>
        </div>
      </div>
    </div>

    <div class="report-section disclaimer">
      <p>说明：本评价结果基于多源监测数据融合算法自动计算。红色表示高度关注，黄色表示预警，绿色表示稳定。</p>
    </div>
  </div>
  <div v-else-if="isLoading" class="loading">分析数据中...</div>
  <div v-else class="error">
    <p>无法加载评价数据。</p>
    <button @click="fetchReport" class="retry-btn">重试</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/services/api';

const report = ref(null);
const isLoading = ref(true);
const route = useRoute();

async function fetchReport() {
  isLoading.value = true;
  const boreholeId = route.params.boreholeId || 1;
  try {
    const response = await api.getEvaluationReport(boreholeId);
    report.value = response.data;
  } catch (error) {
    console.error(`Error fetching evaluation report:`, error);
  } finally {
    isLoading.value = false;
  }
}

async function downloadPDF() {
  const boreholeId = report.value.borehole_id;
  const url = `/api/v1/evaluation/report/${boreholeId}/download`;
  
  // 使用 a 标签下载
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `Report_Borehole_${boreholeId}.pdf`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
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
  color: #fff;
}
.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  border-bottom: 1px solid #2a3f78;
  padding-bottom: 1rem;
}
.download-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}
.download-btn:hover { background-color: #0056b3; }

.report-section {
  margin-bottom: 2.5rem;
}
.report-section h3 {
  color: #c0c5d6;
  margin-bottom: 1.5rem;
}
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}
.metric-card {
  background: #1a2952;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #2a3f78;
  text-align: center;
}
.metric-card h4 { margin: 0 0 1rem 0; font-weight: normal; color: #c0c5d6; }
.metric-card .value {
  font-size: 2.2rem;
  font-weight: bold;
  color: #fff;
  margin: 0;
}
.metric-card.highlight {
  background: linear-gradient(145deg, #1a2952, #2a3f78);
  border-color: #007bff;
}
.metric-card .level {
  margin-top: 0.5rem;
  font-weight: bold;
}
.level.稳定 { color: #28a745; }
.level.一般 { color: #ffc107; }
.level.危险 { color: #dc3545; }

.disclaimer {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #c0c5d6;
}
.loading, .error {
  text-align: center;
  padding: 5rem;
  color: #c0c5d6;
}
.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 2rem;
  background: #2a3f78;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>