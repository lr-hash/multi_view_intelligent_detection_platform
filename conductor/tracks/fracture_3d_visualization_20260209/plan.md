# Implementation Plan - 压裂施工 3D 可视化与动态效果实现

## Phase 1: 后端压裂数据 API (Backend Fracture Data API)
- [ ] **Task: 实现压裂数据查询服务**
    - [ ] 在 `backend/app/services/visualization_service.py` 中编写获取指定钻孔压裂数据的函数。
- [ ] **Task: 定义可视化数据接口**
    - [ ] 在 `backend/app/api/visualization.py` 中暴露相关 API 端点。
- [ ] **Task: 编写 API 单元测试**
    - [ ] 验证接口返回的数据结构正确。
- [ ] **Task: Conductor - User Manual Verification '后端压裂数据 API' (Protocol in workflow.md)**

## Phase 2: 动态 3D 压裂段渲染 (Dynamic 3D Fracture Rendering)
- [ ] **Task: 开发压裂球渲染工具**
    - [ ] 在 `frontend/src/utils/three-utils.js` 中添加 `createFractureSphere` 函数。
- [ ] **Task: 集成动态映射逻辑**
    - [ ] 在 `VisualizeView.vue` 中调用 API 获取数据。
    - [ ] 根据压力和流量计算球体的 scale 和 color。
- [ ] **Task: 实现点击交互**
    - [ ] 恢复 Raycaster 逻辑，支持选中压裂球并展示详情。
- [ ] **Task: Conductor - User Manual Verification '动态 3D 压裂段渲染' (Protocol in workflow.md)**
