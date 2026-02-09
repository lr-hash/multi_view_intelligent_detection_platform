# 多视域智能侦测平台 (Multi-view Intelligent Detection Platform)

本项目是一个基于Flask和Vue.js的全栈应用，旨在为煤矿安全生产提供智能化的多源数据监测、分析与可视化解决方案。

## 项目结构

```
.
├── backend/      # Flask 后端应用
└── frontend/     # Vue.js 前端应用
```

## 技术栈

- **后端**: Flask, Python
- **前端**: Vue 3, Vite, Pinia, Vue Router, Three.js
- **数据库**: PostgreSQL (as recommended)
- **部署**: Nginx (as recommended)

## 开发环境设置

### 后端 (Backend)

1.  **进入后端目录**
    ```bash
    cd backend
    ```

2.  **创建并激活虚拟环境**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **安装依赖**
    ```bash
    pip install Flask Flask-SQLAlchemy Flask-Migrate
    ```

4.  **运行开发服务器**
    ```bash
    flask run
    ```
    后端服务将运行在 `http://127.0.0.1:5000`。

### 前端 (Frontend)

1.  **进入前端目录**
    ```bash
    cd frontend
    ```

2.  **安装依赖**
    ```bash
    npm install
    ```

3.  **运行开发服务器**
    ```bash
    npm run dev
    ```
    前端开发服务器将启动，并代理 `/api` 请求到后端。

## 下一步计划

1.  **数据库设计与实现**: 根据需求文档，设计并使用 Flask-Migrate 创建数据库表结构。
2.  **模拟数据接口**: 开发用于生成模拟监测数据的后端接口，以便前端进行开发和测试。
3.  **完善3D可视化**: 使用`Three.js`实现钻孔、巷道等三维模型的可视化。
4.  **实现核心分析功能**: 开发数据融合、效果评价等核心算法。
5.  **完善UI/UX**: 优化前端界面，提升用户体验。

```