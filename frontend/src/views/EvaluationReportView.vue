<template>
  <div class="report-container">
    <div class="selection-bar">
      <div class="input-group">
        <label>选择钻孔进行评价：</label>
        <select v-model="currentBoreholeId" @change="onBoreholeChange" class="borehole-select">
          <option v-for="bh in boreholes" :key="bh.id" :value="bh.id">
            {{ bh.borehole_no }} ({{ bh.site_name }})
          </option>
        </select>
      </div>
    </div>

    <div v-if="report && !isLoading" class="report-content animate-fade-in">
      <div class="report-header">
        <h2>钻孔 {{ report.borehole_no }} 压裂效果综合评价报告</h2>
        <button @click="downloadPDF" class="download-btn">
          <svg style="width:18px;height:18px;margin-right:8px" viewBox="0 0 24 24"><path fill="currentColor" d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z" /></svg>
          下载 PDF 报告
        </button>
      </div>

      <div class="report-grid">
        <!-- 核心指标卡片 -->
        <div class="metrics-section">
          <h3>1. 核心量化指标</h3>
          <div class="metrics-cards">
            <div class="metric-card">
              <span class="label">矿压降低率</span>
              <span class="value">{{ report.metrics.pressure_reduction }}%</span>
              <div class="trend-bar"><div class="fill" :style="{width: report.metrics.pressure_reduction + '%'}"></div></div>
            </div>
            <div class="metric-card">
              <span class="label">变形控制率</span>
              <span class="value">{{ report.metrics.deformation_control }}%</span>
              <div class="trend-bar"><div class="fill" :style="{width: report.metrics.deformation_control + '%'}"></div></div>
            </div>
            <div class="metric-card highlight-blue">
              <span class="label">压裂有效率</span>
              <span class="value">{{ report.metrics.efficiency }}%</span>
              <span class="status-tag">综合评分</span>
            </div>
            <div class="metric-card highlight-green">
              <span class="label">稳定性指数</span>
              <span class="value">{{ report.metrics.stability_index }}</span>
              <span class="level-indicator" :class="report.level">等级: {{ report.level }}</span>
            </div>
          </div>
        </div>

        <!-- 详细评价建议 -->
        <div class="analysis-section">
          <h3>2. 专家分析结论</h3>
          <div class="analysis-box">
            <p><strong>评价结果：</strong>钻孔 {{ report.borehole_no }} 压裂施工后，支架平均工作阻力显著下降，围岩变形速率趋于平稳。综合评价等级为 <span :class="report.level">{{ report.level }}</span>。</p>
            <p><strong>处理建议：</strong>{{ report.level === '稳定' ? '维持当前开采速度，定期进行常规巡检。' : '建议加强监测频率，必要时采取补充卸压措施。' }}</p>
          </div>
        </div>
      </div>

      <div class="report-section disclaimer">
        <p>※ 本报告由多视域智能侦测平台自动生成，计算模型基于：支架压力、微震能量、巷道累计位移等多源异构数据。</p>
      </div>
    </div>
    
    <div v-else-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>正在调取多源数据并执行融合算法...</p>
    </div>
    
    <div v-else class="error-state">
      <p>无法加载该钻孔的评价数据，可能由于监测样本不足。</p>
      <button @click="fetchReport" class="retry-btn">重新尝试</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';

const report = ref(null);
const isLoading = ref(true);
const boreholes = ref([]);
const currentBoreholeId = ref(1);

const route = useRoute();
const router = useRouter();

async function fetchInitialData() {
  try {
    // 1. 获取所有钻孔列表用于下拉选择
    const sitesRes = await api.getDrillingDesign();
    const list = [];
    sitesRes.data.forEach(site => {
      site.boreholes.forEach(bh => {
        list.push({ id: bh.id, borehole_no: bh.borehole_no, site_name: site.name });
      });
    });
    boreholes.value = list;

    // 2. 确定当前 ID
    currentBoreholeId.value = parseInt(route.params.boreholeId) || (list.length > 0 ? list[0].id : 1);
    
    await fetchReport();
  } catch (error) {
    console.error("Error init report view:", error);
  }
}

async function fetchReport() {
  isLoading.value = true;
  try {
    const response = await api.getEvaluationReport(currentBoreholeId.value);
    report.value = response.data;
  } catch (error) {
    console.error(`Error fetching evaluation report:`, error);
    report.value = null;
  } finally {
    isLoading.value = false;
  }
}

function onBoreholeChange() {
  router.push({ name: 'evaluation-report', params: { boreholeId: currentBoreholeId.value } });
  fetchReport();
}

async function downloadPDF() {
  if (!report.value) return;
  const boreholeId = report.value.borehole_id;
  const url = `/api/v1/evaluation/report/${boreholeId}/download`;
  window.open(url, '_blank');
}

onMounted(() => {
  fetchInitialData();
});
</script>

<style scoped>
.report-container {
  max-width: 1100px;
  margin: 0 auto;
  color: #fff;
}

.selection-bar {
  background: #1a2952;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 1px solid #2a3f78;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.borehole-select {
  background: #0f172a;
  color: #fff;
  border: 1px solid #3b82f6;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  min-width: 300px;
  outline: none;
}

.report-content {
  background: #1a2952;
  border-radius: 16px;
  padding: 2.5rem;
  border: 1px solid #2a3f78;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #2a3f78;
}

.report-header h2 { margin: 0; font-size: 1.6rem; color: #f1f5f9; }

.download-btn {
  display: flex;
  align-items: center;
  background: linear-gradient(to right, #3b82f6, #2563eb);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}
.download-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); }

.metrics-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.metric-card {
  background: #0f172a;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #2a3f78;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.metric-card .label { color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.8rem; }
.metric-card .value { font-size: 2.4rem; font-weight: 800; color: #fff; }

.trend-bar {
  height: 4px;
  background: #1e293b;
  border-radius: 2px;
  margin-top: 1rem;
}
.trend-bar .fill {
  height: 100%;
  background: #3b82f6;
  border-radius: 2px;
}

.highlight-blue { border-color: #3b82f6; background: linear-gradient(145deg, #0f172a, #1e3a8a); }
.highlight-green { border-color: #10b981; background: linear-gradient(145deg, #0f172a, #064e3b); }

.level-indicator {
  margin-top: 0.8rem;
  font-weight: bold;
  font-size: 1.1rem;
}
.level-indicator.稳定 { color: #10b981; }
.level-indicator.一般 { color: #f59e0b; }
.level-indicator.危险 { color: #ef4444; }

.analysis-box {
  background: #0f172a;
  padding: 1.5rem;
  border-radius: 12px;
  line-height: 1.8;
  color: #cbd5e1;
}

.disclaimer { margin-top: 3rem; font-size: 0.85rem; color: #64748b; font-style: italic; }

.loading-state, .error-state {
  padding: 10rem 0;
  text-align: center;
  color: #94a3b8;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255,255,255,0.1);
  border-left-color: #3b82f6;
  border-radius: 50%;
  margin: 0 auto 1.5rem;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10deg); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.5s ease-out; }
</style>