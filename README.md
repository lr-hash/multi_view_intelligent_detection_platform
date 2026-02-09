# 多视域智能侦测平台 (Multi-view Intelligent Detection Platform)

本项目是一个基于 Flask 和 Vue.js 的全栈应用，旨在为煤矿安全生产提供智能化的多源数据监测、分析与可视化解决方案。本项目采用 **Conductor** 方法论进行管理。

## 核心愿景
集成多源监测数据（KJ653, SOS, 压裂施工），实现长水平孔压裂 3D 可视化及压裂效果的科学评价，解决矿压显现剧烈与数据孤岛问题。

## 项目结构
- `backend/`: 基于 Flask 的后端 API 与数据处理服务。
- `frontend/`: 基于 Vue 3 的前端可视化与监控看板。
- `conductor/`: 项目管理与任务轨道规范目录。
- `database/`: 原始数据文件存放。

## 技术栈
- **后端**: Flask (Python), PostgreSQL, Redis, Flask-Migrate, SQLAlchemy.
- **前端**: Vue 3 (Vite), Pinia, Vue Router, Three.js, Chart.js.
- **部署**: Nginx (反向代理与静态托管).

## 任务管理 (Conductor)
本项目使用 Gemini CLI 配合 Conductor 插件进行任务驱动式开发。
- **查看进度**: `/conductor:status`
- **开始新任务**: `/conductor:implement`
- **创建任务轨道**: `/conductor:newTrack`

## 开发环境设置

### 后端 (Backend)
1. 进入 `backend/` 目录。
2. 激活虚拟环境: `venv\Scripts\activate` (Windows)。
3. 安装依赖并启动: `pip install -r requirements.txt` (若有) 或手动安装。
4. 运行: `flask run`。

### 前端 (Frontend)
1. 进入 `frontend/` 目录。
2. 安装依赖: `npm install`。
3. 启动开发服务器: `npm run dev`。

## 下一步计划
请参考 `conductor/tracks.md` 查看当前的开发轨道及详细计划。

```