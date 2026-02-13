# Tech Stack - 多视域智能侦测平台

## 1. 后端技术 (Backend)
- **核心框架**：[Flask](https://flask.palletsprojects.com/) (Python) - 轻量级且灵活的 Web 框架，适合快速开发和集成算法。
- **ORM**：SQLAlchemy - 处理与 PostgreSQL 的交互。
- **数据库迁移**：Flask-Migrate (Alembic) - 管理数据库版本控制。
- **实时处理缓冲**：Redis - 用于多源数据同步过程中的实时对齐与临时缓冲。

## 2. 前端技术 (Frontend)
- **核心框架**：[Vue 3](https://vuejs.org/) - 响应式且高性能的 UI 框架。
- **构建工具**：Vite - 极速的开发服务器与打包工具。
- **状态管理**：Pinia - Vue 官方推荐的轻量级状态管理。
- **路由**：Vue Router - 处理单页面应用跳转。
- **3D 渲染引擎**：[Three.js](https://threejs.org/) - 用于钻孔轨迹、巷道及压裂场景的 3D 可视化。
- **图表库**：Chart.js (配合 chartjs-plugin-annotation) - 用于矿压趋势与微震能量等数据的 2D 图表展示，支持阈值标注。

## 3. 数据库 (Database)
- **主数据库**：[PostgreSQL](https://www.postgresql.org/) - 开发环境与生产环境均统一使用，确保强一致性与空间数据处理能力。

## 4. 通信与协议 (Communication)
- **API 风格**：RESTful API - 前后端交互的标准模式。
- **跨域处理**：Flask-CORS - 解决开发环境下的跨域资源共享问题。
- **实时通信**：WebSocket - 用于秒级异常报警的即时推送。
- **HTTP 客户端**：Axios - 前端请求处理。

## 5. 部署与运维 (Deployment)
- **Web 服务器**：Nginx - 负责前端静态资源托管、SSL 终止以及向后端的反向代理。
- **虚拟环境**：Python venv - 隔离后端依赖。