from app.models import DrillingSite, Borehole, BoreholeTrajectory, FractureConstructionData, MicroseismicEvent
import random
from datetime import datetime, timedelta

def get_borehole_fracture_data(borehole_id):
    """
    获取指定钻孔的压裂段数据及其对应的轨迹坐标。
    """
    # 尝试获取真实数据，若无则生成基于轨迹的模拟数据
    real_data = FractureConstructionData.query.filter_by(borehole_id=borehole_id).all()
    
    # 获取轨迹以确定位置
    trajectories = BoreholeTrajectory.query.filter_by(borehole_id=borehole_id).order_by(BoreholeTrajectory.measured_depth).all()
    if not trajectories:
        return []

    results = []
    if real_data:
        for seg in real_data:
            # 找到最接近的轨迹点 (简单逻辑：根据段号在轨迹中按比例找位置)
            # 假设段号从1开始，均匀分布在轨迹点中
            idx = min(len(trajectories) - 1, int((seg.segment_no / 12) * len(trajectories)))
            t = trajectories[idx]
            results.append({
                "segment_no": seg.segment_no,
                "pressure": seg.pressure,
                "flow_rate": seg.flow_rate,
                "total_volume": seg.total_volume,
                "position": {
                    "x": t.coord_e,
                    "y": t.coord_z,
                    "z": -t.coord_n
                }
            })
    else:
        # 如果没有真实压裂数据，在轨迹点上生成模拟压裂点用于展示
        # 每个钻孔生成 5 个模拟压裂段
        for i in range(1, 6):
            idx = min(len(trajectories) - 1, i * (len(trajectories) // 6))
            t = trajectories[idx]
            results.append({
                "segment_no": i,
                "pressure": 15 + random.random() * 10,
                "flow_rate": 1.5 + random.random() * 1.5,
                "total_volume": 100 + i * 50,
                "position": {
                    "x": t.coord_e,
                    "y": t.coord_z,
                    "z": -t.coord_n
                }
            })
    return results

def get_drilling_design_data():
    """获取所有钻场、钻孔及其轨迹数据"""
    sites = DrillingSite.query.all()
    data = []
    for site in sites:
        site_data = {
            "id": site.id,
            "name": site.name,
            "coord_e": site.coord_e,
            "coord_n": site.coord_n,
            "coord_z": site.coord_z,
            "boreholes": []
        }
        for bh in site.boreholes:
            trajs = BoreholeTrajectory.query.filter_by(borehole_id=bh.id).order_by(BoreholeTrajectory.measured_depth).all()
            site_data["boreholes"].append({
                "id": bh.id,
                "borehole_no": bh.borehole_no,
                "design_length": bh.design_length or 500,
                "trajectories": [
                    {"measured_depth": t.measured_depth, "coord_e": t.coord_e, "coord_n": t.coord_n, "coord_z": t.coord_z}
                    for t in trajs
                ]
            })
        data.append(site_data)
    return data

def get_microseismic_points():
    """获取最近的微震事件点用于 3D 展示"""
    events = MicroseismicEvent.query.order_by(MicroseismicEvent.event_time.desc()).limit(200).all()
    return [
        {
            "id": e.id,
            "time": e.event_time.isoformat(),
            "x": e.coord_x,
            "y": e.coord_z, # 映射到 3D 空间的 Y (高度)
            "z": -e.coord_y, # 映射到 3D 空间的 Z (北向取反)
            "energy": e.energy
        } for e in events
    ]

# 其余仪表盘和趋势函数暂保持模拟或后续对接...
def get_dashboard_core_metrics():
    return {
        "strata_pressure": { "current_val": round(32.5 + random.random() * 5, 1), "unit": "MPa" },
        "microseismic": { "latest_energy": random.randint(1000, 5000), "daily_count": random.randint(5, 20), "unit": "J" },
        "deformation": { "total_offset": round(142.8 + random.random() * 10, 1), "unit": "mm" },
        "fracturing": { "order": 5, "recorded_p": 22.4, "status": "COMPLETED" }
    }

def get_pressure_trend_data(time_range):
    data_points = []
    now = datetime.now()
    for i in range(100):
        timestamp = (now - timedelta(minutes=(100-i)*5)).isoformat()
        value = 30 + random.random() * 10
        data_points.append({"x": timestamp, "y": round(value, 2)})
    return data_points

def get_microseismic_frequency_data(time_range):
    data = []
    now = datetime.now()
    for i in range(24):
        hour = now - timedelta(hours=i)
        data.append({"x": hour.strftime('%H:00'), "y": random.randint(0, 15)})
    return data[::-1]

def get_deformation_trend_data(time_range):
    datasets = []
    labels = []
    now = datetime.now()
    for i in range(24): labels.append((now - timedelta(hours=24-i)).strftime('%H:00'))
    for station in ['测点A', '测点B', '测点C']:
        data_points = []
        base_deformation = random.uniform(20, 50)
        for _ in range(24):
            base_deformation += random.uniform(0.1, 1.5)
            data_points.append(round(base_deformation, 2))
        datasets.append({"label": station, "data": data_points})
    return {"labels": labels, "datasets": datasets}