from app.models import DrillingSite, Borehole, BoreholeTrajectory, FractureConstructionData
import random
from datetime import datetime, timedelta

def get_borehole_fracture_data(borehole_id):
    """
    获取指定钻孔的压裂段数据及其对应的轨迹坐标。
    """
    # 1. 查询压裂施工数据
    # fracture_data = FractureConstructionData.query.filter_by(borehole_id=borehole_id).all()
    # 模拟数据 (12 个压裂段)
    fracture_data = []
    for i in range(1, 13):
        fracture_data.append({
            "segment_no": i,
            "pressure": 15 + random.random() * 10,
            "flow_rate": 1.5 + random.random() * 1.5,
            "total_volume": 100 + i * 50,
            "sand_concentration": 50 + random.random() * 100
        })
    
    # 2. 查询钻孔轨迹以确定每个段的空间位置 (假设每个段等间距分布)
    # trajectories = BoreholeTrajectory.query.filter_by(borehole_id=borehole_id).order_by(BoreholeTrajectory.measured_depth).all()
    # 模拟轨迹点 (对应 550m 长度)
    trajectories = [{"measured_depth": i*50, "coord_e": 35400+i*5, "coord_n": 28000+i*50, "coord_z": -610+i*2} for i in range(11)]
    
    # 简单逻辑：将压裂段映射到轨迹点上 (此处仅为演示，实际应根据测深匹配)
    results = []
    for idx, seg in enumerate(fracture_data):
        # 循环复用模拟轨迹点作为位置
        traj_idx = idx % len(trajectories)
        t = trajectories[traj_idx]
        results.append({
            **seg,
            "position": {
                "x": t['coord_e'],
                "y": t['coord_z'],
                "z": -t['coord_n'] # 注意 Y/Z 轴转换
            }
        })
        
    return results

def get_drilling_design_data():
    """
    5.3.1 压裂设计可视化
    Retrieves data for fracturing design visualization.
    """
    print("SERVICE: Retrieving drilling design data (simulated).")
    # In a real application, this would query the database.
    # sites = DrillingSite.query.all()
    # data = [serialize(site) for site in sites]
    # For now, return mock data.
    return [
        {
            "id": 1, "name": "28联巷钻场", "coord_e": 35400, "coord_n": 28000, "coord_z": -610,
            "boreholes": [
                { "id": 1, "borehole_no": "1#", "design_length": 550, "diameter": 96, "azimuth": 270, "dip_angle": 14, "segments": 12, "trajectories": [{"measured_depth": i*50, "coord_e": 35400+i*5, "coord_n": 28000+i*50, "coord_z": -610+i*2} for i in range(11)] },
                { "id": 2, "borehole_no": "2#", "design_length": 560, "diameter": 96, "azimuth": 272, "dip_angle": 15, "segments": 12, "trajectories": [] },
            ]
        },
        {
            "id": 2, "name": "25联巷钻场", "coord_e": 35300, "coord_n": 27900, "coord_z": -612,
            "boreholes": []
        }
    ]

def get_dashboard_core_metrics():
    """
    5.3.2 数据看板 - 核心指标实时展示
    Retrieves core metrics for the real-time dashboard.
    """
    print("SERVICE: Retrieving dashboard core metrics (simulated).")
    return {
        "strata_pressure": { "current_val": round(32.5 + random.random() * 5, 1), "unit": "MPa" },
        "microseismic": { "latest_energy": random.randint(1000, 5000), "daily_count": random.randint(5, 20), "unit": "J" },
        "deformation": { "total_offset": round(142.8 + random.random() * 10, 1), "unit": "mm" },
        "fracturing": { "order": 5, "recorded_p": 22.4, "status": "COMPLETED" }
    }

def get_pressure_trend_data(time_range):
    """
    5.3.3 数据趋势图 - 矿压
    Retrieves time-series data for trend analysis.
    """
    print(f"SERVICE: Retrieving trend data for pressure in range {time_range} (simulated).")
    # Generate some random time-series data
    data_points = []
    now = datetime.utcnow()
    for i in range(100):
        timestamp = (now - timedelta(minutes=(100-i)*5)).isoformat()
        value = 30 + random.random() * 10
        data_points.append({"x": timestamp, "y": round(value, 2)})
    return data_points

def get_microseismic_frequency_data(time_range):
    """
    数据趋势图 - 微震频次
    Generates hourly microseismic event counts for the last 24 hours.
    """
    print(f"SERVICE: Retrieving microseismic frequency for range {time_range} (simulated).")
    data = []
    now = datetime.utcnow()
    for i in range(24):
        hour = now - timedelta(hours=i)
        data.append({
            "x": hour.strftime('%H:00'),
            "y": random.randint(0, 15)
        })
    return data[::-1] # Reverse to have chronological order

def get_deformation_trend_data(time_range):
    """
    数据趋势图 - 巷道变形
    Generates trend data for multiple deformation points.
    """
    print(f"SERVICE: Retrieving deformation trends for range {time_range} (simulated).")
    datasets = []
    labels = []
    now = datetime.utcnow()
    
    for i in range(24): # 24 data points
        labels.append((now - timedelta(hours=24-i)).strftime('%H:00'))

    for station in ['测点A', '测点B', '测点C']:
        data_points = []
        base_deformation = random.uniform(20, 50)
        for _ in range(24):
            base_deformation += random.uniform(0.1, 1.5)
            data_points.append(round(base_deformation, 2))
        datasets.append({
            "label": station,
            "data": data_points
        })
    return {"labels": labels, "datasets": datasets}

