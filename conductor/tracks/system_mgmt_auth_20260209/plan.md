# Implementation Plan - 系统管理、权限控制与配置界面

## Phase 1: 身份验证体系 (Authentication Framework)
- [ ] **Task: 实现 JWT 登录与拦截**
    - [ ] 在 `backend/app/api/auth.py` 中完善登录逻辑。
    - [ ] 实现 `@auth_required` 装饰器用于保护 API。
- [ ] **Task: 完善前端权限状态管理**
    - [ ] 在 `frontend/src/store/auth.js` 中完善 Pinia 状态。
    - [ ] 实现 axios 请求拦截器自动注入 Token。
- [ ] **Task: 编写认证流程测试**
    - [ ] 验证登录流程及受保护接口的访问限制。
- [ ] **Task: Conductor - User Manual Verification '身份验证体系' (Protocol in workflow.md)**

## Phase 2: 系统动态配置服务 (System Dynamic Configuration)
- [ ] **Task: 建立配置表模型**
    - [ ] 在 `models.py` 中添加 `SystemConfig` 类（键值对存储）。
- [ ] **Task: 实现配置 CRUD 接口**
    - [ ] 实现获取和更新系统参数的 API 接口。
- [ ] **Task: 联动报警与集成逻辑**
    - [ ] 修改 `auxiliary_service.py` 使其从数据库读取阈值而非模拟。
- [ ] **Task: Conductor - User Manual Verification '系统动态配置服务' (Protocol in workflow.md)**

## Phase 3: 前端管理视图 (Frontend Admin Views)
- [ ] **Task: 开发登录与重定向**
    - [ ] 实现 `LoginView.vue` 交互。
- [ ] **Task: 开发参数设置界面**
    - [ ] 实现 `InterfaceConfigView.vue` 用于管理接口与阈值。
- [ ] **Task: Conductor - User Manual Verification '前端管理视图' (Protocol in workflow.md)**
