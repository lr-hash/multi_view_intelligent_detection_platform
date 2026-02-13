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
              <div class="label-row">
                <span class="label">矿压降低率</span>
                <div class="help-icon">?
                  <div class="tooltip">反映压裂后支架受力的下降程度。数值越大卸压效果越明显。通常 >15% 为良好。</div>
                </div>
              </div>
              <span class="value">{{ report.metrics.pressure_reduction }}%</span>
              <div class="trend-bar"><div class="fill" :style="{width: report.metrics.pressure_reduction + '%'}"></div></div>
            </div>

            <div class="metric-card">
              <div class="label-row">
                <span class="label">变形控制率</span>
                <div class="help-icon">?
                  <div class="tooltip">反映巷道围岩变形速度的减缓程度。数值越大支护环境越稳定。通常 >30% 为理想。</div>
                </div>
              </div>
              <span class="value">{{ report.metrics.deformation_control }}%</span>
              <div class="trend-bar"><div class="fill" :style="{width: report.metrics.deformation_control + '%'}"></div></div>
            </div>

            <div class="metric-card highlight-blue">
              <div class="label-row">
                <span class="label">压裂有效率</span>
                <div class="help-icon">?
                  <div class="tooltip">结合压力降、变形改善及施工规模的综合评分。>60% 说明施工非常成功。</div>
                </div>
              </div>
              <span class="value">{{ report.metrics.efficiency }}%</span>
              <span class="status-tag">综合评分</span>
            </div>

            <div class="metric-card highlight-green">
              <div class="label-row">
                <span class="label">稳定性指数</span>
                <div class="help-icon">?
                  <div class="tooltip">对施工后该区域顶板安全性的最终评分。>70 分属于稳定状态。</div>
                </div>
              </div>
              <span class="value">{{ report.metrics.stability_index }}</span>
              <span class="level-indicator" :class="report.level">等级: {{ report.level }}</span>
            </div>
          </div>
        </div>

        <!-- 详细评价建议 -->
        <div class="analysis-section">
          <h3>2. 专家分析结论 (基于多源数据证据)</h3>
          <div class="analysis-box">
            <div class="analysis-text">
              {{ report.expert_analysis }}
            </div>
            <div class="evidence-footer">
              <span class="data-source">证据来源：KJ653顶板系统、巷道变形监测点、施工排量记录</span>
            </div>
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

    // 2. 确定当前 ID (从路由获取，若无则取列表第一个)
    const routeId = parseInt(route.params.boreholeId);
    if (!isNaN(routeId)) {
      currentBoreholeId.value = routeId;
    } else if (list.length > 0) {
      currentBoreholeId.value = list[0].id;
    }
    
    // 3. 加载报告
    await fetchReport();
  } catch (error) {
    console.error("Error init report view:", error);
    isLoading.value = false;
  }
}

async function fetchReport() {
  if (!currentBoreholeId.value) return;
  isLoading.value = true;
  report.value = null; // 清空旧数据
  try {
    const response = await api.getEvaluationReport(currentBoreholeId.value);
    // 检查返回数据是否包含有效指标
    if (response.data && response.data.metrics) {
      report.value = response.data;
    } else {
      report.value = null;
    }
  } catch (error) {
    console.error(`Error fetching evaluation report:`, error);
    report.value = null;
  } finally {
    isLoading.value = false;
  }
}

function onBoreholeChange() {
  // 更新路由但不刷新页面，手动调用 fetchReport
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
  overflow: visible; /* Changed to visible for tooltips */
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.help-icon {
  width: 18px;
  height: 18px;
  background: #334155;
  border-radius: 50%;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  cursor: help;
  position: relative;
}

.help-icon:hover {
  background: #3b82f6;
  color: #fff;
}

.tooltip {
  visibility: hidden;
  width: 200px;
  background-color: #1e293b;
  color: #f1f5f9;
  text-align: left;
  border-radius: 6px;
  padding: 10px;
  position: absolute;
  z-index: 100;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.8rem;
  line-height: 1.4;
  border: 1px solid #3b82f6;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
  font-weight: normal;
}

.tooltip::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #3b82f6 transparent transparent transparent;
}

.help-icon:hover .tooltip {
  visibility: visible;
  opacity: 1;
}

.analysis-text {
  line-height: 2;
  font-size: 1.05rem;
  color: #e2e8f0;
  white-space: pre-wrap; /* Preserve line breaks */
}

.evidence-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,0.05);
}

.data-source {
  font-size: 0.8rem;
  color: #64748b;
}

.metric-card .label { color: #94a3b8; font-size: 0.9rem; }
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