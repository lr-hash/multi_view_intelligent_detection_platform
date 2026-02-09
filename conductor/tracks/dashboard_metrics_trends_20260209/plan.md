# Implementation Plan - 数据看板核心指标与趋势分析展示

## Phase 1: 数据看板组件开发 (Dashboard Component Development)
- [ ] **Task: 设计看板基础布局**
    - [ ] 在 `frontend/src/views/DashboardView.vue` 中定义 2x2 或 3x2 的栅格布局。
    - [ ] 创建可复用的指标卡片组件 `MetricCard.vue`。
- [ ] **Task: 集成 Chart.js 工具库**
    - [ ] 确认 `vue-chartjs` 配置。
    - [ ] 封装基础图表组件（LineChart, BarChart）。
- [ ] **Task: 编写 UI 组件单元测试**
    - [ ] 验证指标卡片的数据渲染。
- [ ] **Task: Conductor - User Manual Verification '数据看板组件开发' (Protocol in workflow.md)**

## Phase 2: 后端数据对接与动态化 (Data Integration & Dynamic Updates)
- [ ] **Task: 对接看板 API**
    - [ ] 在 `DashboardView.vue` 中调用 `getDashboardCoreMetrics`。
    - [ ] 在 `DashboardView.vue` 中调用趋势图 API（Pressure, Seismic, Deformation）。
- [ ] **Task: 实现时间维度切换逻辑**
    - [ ] 增加时间范围选择器，触发 API 参数更新。
- [ ] **Task: 验证数据一致性**
    - [ ] 确保前端图表展示与后端返回的数据点完全对应。
- [ ] **Task: Conductor - User Manual Verification '后端数据对接与动态化' (Protocol in workflow.md)**
