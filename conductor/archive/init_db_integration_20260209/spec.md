# Specification - 初始化数据库架构与多源数据集成接口

## 1. 概述
本任务轨道旨在完善后端数据库模型，并实现与外部监测系统（KJ653 顶板监测、SOS 微震监测）的数据接入逻辑。这是实现平台多源数据融合与可视化的基础。

## 2. 需求分析
### 2.1 数据库扩展
- **压裂施工数据 (`fracture_construction_data`)**：记录压裂过程中的压力、流量、累计排量等实时数据。
- **接口日志 (`interface_log`)**：记录每次接口调用的时间、来源、状态及简要消息，用于监控接口运行状况。

### 2.2 接口功能实现
- **KJ653 数据接入**：完善 `/ingest/kj653` 接口，将传入的 JSON 数据解析并存入 `support_pressure_data` 表。
- **SOS 数据接入**：完善 `/ingest/sos` 接口，将传入的 JSON 数据解析并存入 `microseismic_event` 表。
- **状态监测**：实现 `get_all_interface_statuses` 逻辑，通过查询各表最后一条记录的时间来判断接口状态。

## 3. 验收标准
- [ ] 在 `models.py` 中成功定义 `FractureConstructionData` 和 `InterfaceLog` 模型。
- [ ] 成功执行数据库迁移，在 PostgreSQL 中创建对应表。
- [ ] 编写测试用例，验证 KJ653 和 SOS 数据能够通过 API 正确存入数据库。
- [ ] `interfaces/status` 接口能返回真实的数据库连接与数据更新状态。
