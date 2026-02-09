from datetime import datetime, timedelta
import random

def get_alarm_configs():
    """
    5.5.1.1 阈值设置 (获取)
    """
    print("SERVICE: Retrieving alarm thresholds (simulated).")
    return {
        "pressure_max": {"value": 60, "level": "critical"},
        "deformation_rate_max": {"value": 50, "level": "warning"}
    }

def get_alarm_history(limit=50):
    """
    5.5.1.2 报警触发与通知 (获取历史)
    """
    print(f"SERVICE: Retrieving last {limit} alarms (simulated).")
    history = []
    for i in range(limit):
        history.append({
            "id": 100+i,
            "timestamp": (datetime.utcnow() - timedelta(hours=i)).isoformat(),
            "metric": "pressure_max",
            "value": round(60 + random.random() * 5, 2),
            "level": "critical",
            "acknowledged": random.choice([True, False])
        })
    return history

def query_data(params):
    """
    5.5.2.1 多条件查询
    """
    print(f"SERVICE: Querying data with params: {params} (simulated).")
    # Simulate a database query
    return [
        {"timestamp": "2026-02-02 23:00:00", "sensor_id": "P1_045", "value": 34.5},
        {"timestamp": "2026-02-02 23:00:05", "sensor_id": "P1_046", "value": 35.1},
    ]

def get_system_logs(level='INFO', limit=100):
    """
    5.5.3.2 系统日志
    """
    print(f"SERVICE: Retrieving {level} system logs (simulated).")
    return [
        {"timestamp": "2026-02-02 23:01:00", "level": "INFO", "message": "User 'admin' logged in."},
        {"timestamp": "2026-02-02 23:02:00", "level": "WARNING", "message": "Interface 'FRACTURE_DB' is offline."},
    ]
