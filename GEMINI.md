# Gemini Project: 多视域智能侦测平台 - 开发纪实 (2026-02-09)

## 1. 项目概览
本项目是一个全栈式煤矿安全监测平台，旨在集成多源监测数据（矿压、微震、变形、压裂），提供 3D 可视化场景、数据看板、自动化评价报告及实时报警功能。

## 2. 本次会话完成的任务轨道 (Archived Tracks)
所有计划中的核心开发轨道已圆满完成并归档：
- **init_db_integration_20260209**: 数据库架构初始化与多源数据集成接口。
- **data_processing_fusion_20260209**: 数据清洗、标准化与顶板稳定性加权融合算法。
- **3d_visualization_scene_20260209**: 3D 可视化场景构建与轨迹渲染基础。
- **fracture_3d_visualization_20260209**: 压裂施工 3D 动态效果实现。
- **dashboard_metrics_trends_20260209**: 数据看板、核心指标展示与历史趋势分析。
- **fracture_evaluation_report_20260209**: 压裂效果量化评价模型与 PDF 报告生成。
- **alarm_history_query_20260209**: 报警记录持久化与多维数据综合查询。
- **system_mgmt_auth_20260209**: JWT 身份验证、角色权限控制与系统动态配置。
- **realtime_alarm_push_20260209**: 基于 WebSocket 的实时异常报警推送。

## 3. 关键技术变更与升级
### 3.1 数据库架构
- **迁移**: 从 SQLite 全面迁移至 **PostgreSQL**。
- **库名**: `multi_view_db`
- **连接字符串**: `postgresql://postgres:postgres@localhost:5432/multi_view_db`
- **模型补充**: 
    - `User`: 增加 `role` 字段 (ADMIN/USER)。
    - `AlarmRecord`: 存储报警历史。
    - `SystemConfig`: 存储动态系统参数（IP、端口、报警阈值）。

### 3.2 安全与认证
- **机制**: 基于 `PyJWT` 的令牌验证。
- **保护**: 后端所有 `/api/v1/*` 接口均已挂载 `@token_required` 装饰器。
- **前端**: 实现 axios 请求拦截器，自动从 `localStorage` 获取并注入 Token。

### 3.3 实时通信
- **技术栈**: `Flask-SocketIO` + `socket.io-client`。
- **功能**: 当后端触发报警时，自动向所有已登录的前端客户端广播 `new_alarm` 事件。
- **UI**: 前端实现全局 `AlarmNotification.vue` 组件，支持呼吸红光背景、蜂鸣警报音（模拟）和模态强制确认。

## 4. 运行与调试信息
- **后端地址**: `http://127.0.0.1:5000` (监听 127.0.0.1)
- **前端地址**: `http://localhost:5173` (通过 Vite 代理访问 API)
- **默认管理员账号**:
    - **用户名**: `admin`
    - **密码**: `admin123`
- **网络状态**: 经核实，后端服务运行正常，端口 5000 正处于 LISTENING 状态。

## 5. 项目结构摘要
- `backend/app/api/`: 包含 auth, integration, processing, visualization, evaluation, auxiliary 分组路由。
- `backend/app/services/`: 核心业务逻辑、融合算法与 PDF 生成服务。
- `frontend/src/views/`: 涵盖监控、看板、3D、报表、查询、配置及登录等所有功能页面。
- `frontend/src/components/`: 封装了 Three.js 场景 (`ThreeScene.vue`) 和 报警提醒 (`AlarmNotification.vue`) 等组件。

---
*文档更新于: 2026年2月9日*