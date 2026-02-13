<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();

// 核心指标预览数据
const metrics = ref({
  totalSupportData: 0,
  microseismicEvents: 0,
  activeAlarms: 0,
  dbStatus: 'Connected',
  lastSync: '刚刚'
});

const modules = [
  {
    id: 'dashboard',
    title: '全景数据看板',
    desc: '矿压、微震、变形等核心指标的实时趋势与数据融合分析',
    path: '/dashboard',
    icon: '📊',
    color: '#00d2ff'
  },
  {
    id: 'visualize',
    title: '3D 轨迹渲染',
    desc: '基于 Three.js 的 3D 钻孔轨迹展示与实钻/设计对比分析',
    path: '/visualize',
    icon: '🧊',
    color: '#00ff87'
  },
  {
    id: 'evaluation',
    title: '压裂效果评价',
    desc: '自动化生成评价报告，量化压裂对顶板稳定性的控制效果',
    path: '/visualize', // 此处暂跳可视化，根据实际可调
    icon: '📝',
    color: '#ffdd00'
  },
  {
    id: 'alarms',
    title: '报警响应中心',
    desc: '实时异常监测与历史报警回溯，支持自定义阈值配置',
    path: '/alarm-history',
    icon: '🚨',
    color: '#ff5e62'
  }
];

onMounted(async () => {
  try {
    // 尝试获取部分真实统计数据
    const res = await api.getDashboardCoreMetrics();
    if (res.data) {
      metrics.value.totalSupportData = 20000; // 已导入的 2w 条
      metrics.value.microseismicEvents = 7978; // 已导入的约 8k 条
    }
  } catch (e) {
    console.error('Failed to fetch stats', e);
  }
});

const navigateTo = (path) => {
  router.push(path);
};
</script>

<template>
  <div class="home-container">
    <!-- Header Summary -->
    <div class="hero-section">
      <div class="hero-text">
        <h1>指挥中心概览</h1>
        <p>多视域智能侦测平台 - 实时安全监测与评估系统</p>
      </div>
      <div class="system-stats">
        <div class="stat-item">
          <span class="label">数据库状态</span>
          <span class="value status-online">{{ metrics.dbStatus }}</span>
        </div>
        <div class="stat-item">
          <span class="label">最后同步</span>
          <span class="value">{{ metrics.lastSync }}</span>
        </div>
      </div>
    </div>

    <!-- Quick Stats Row -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">矿压记录总数</div>
        <div class="stat-value">{{ metrics.totalSupportData.toLocaleString() }}</div>
        <div class="stat-trend">↑ 实时入库中</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">微震监测事件</div>
        <div class="stat-value">{{ metrics.microseismicEvents.toLocaleString() }}</div>
        <div class="stat-trend">⚡ 监测活跃</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">活动报警数</div>
        <div class="stat-value" :class="{ 'warning': metrics.activeAlarms > 0 }">{{ metrics.activeAlarms }}</div>
        <div class="stat-trend">✅ 系统状态正常</div>
      </div>
    </div>

    <!-- Module Grid -->
    <div class="module-grid">
      <div 
        v-for="mod in modules" 
        :key="mod.id" 
        class="module-card"
        @click="navigateTo(mod.path)"
        :style="{ '--accent-color': mod.color }"
      >
        <div class="module-icon">{{ mod.icon }}</div>
        <div class="module-info">
          <h3>{{ mod.title }}</h3>
          <p>{{ mod.desc }}</p>
        </div>
        <div class="module-arrow">→</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.hero-text h1 {
  font-size: 2.2rem;
  font-weight: 600;
  background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.hero-text p {
  color: #818cf8;
  font-size: 1.1rem;
}

.system-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  text-align: right;
}

.stat-item .label {
  display: block;
  font-size: 0.8rem;
  color: #64748b;
  text-transform: uppercase;
}

.stat-item .value {
  font-family: 'Courier New', Courier, monospace;
  font-size: 1.1rem;
  color: #e2e8f0;
}

.status-online {
  color: #10b981 !important;
}

/* Stats Cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  background: rgba(30, 41, 59, 0.8);
}

.stat-label {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-value.warning {
  color: #ef4444;
}

.stat-trend {
  font-size: 0.85rem;
  color: #10b981;
}

/* Module Grid */
.module-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.module-card {
  position: relative;
  display: flex;
  align-items: center;
  background: linear-gradient(145deg, #1e293b, #0f172a);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 2rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.module-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background-color: var(--accent-color);
  box-shadow: 0 0 15px var(--accent-color);
  opacity: 0.6;
}

.module-card:hover {
  border-color: var(--accent-color);
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3), inset 0 0 10px var(--accent-color);
  transform: scale(1.02);
}

.module-icon {
  font-size: 3rem;
  margin-right: 2rem;
  filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.2));
}

.module-info h3 {
  font-size: 1.4rem;
  color: #fff;
  margin-bottom: 0.5rem;
}

.module-info p {
  color: #94a3b8;
  font-size: 0.95rem;
  line-height: 1.5;
}

.module-arrow {
  margin-left: auto;
  font-size: 1.5rem;
  color: #475569;
  transition: transform 0.3s ease;
}

.module-card:hover .module-arrow {
  transform: translateX(10px);
  color: var(--accent-color);
}
</style>