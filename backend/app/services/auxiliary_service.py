from datetime import datetime, timedelta
import random
from app import db
from app.models import AlarmRecord

def check_and_trigger_alarms(data_type, value, threshold_red, threshold_yellow):
    """
    检查数值是否超过阈值，并触发报警记录。
    """
    level = None
    msg = ""
    
    if value >= threshold_red:
        level = "RED"
        msg = f"Critical {data_type} alarm: value {value} exceeded red threshold {threshold_red}."
    elif value >= threshold_yellow:
        level = "YELLOW"
        msg = f"Warning {data_type} alarm: value {value} exceeded yellow threshold {threshold_yellow}."
        
    if level:
        try:
            alarm = AlarmRecord(
                alarm_type=data_type,
                level=level,
                value=value,
                threshold=threshold_red if level == "RED" else threshold_yellow,
                message=msg
            )
            db.session.add(alarm)
            db.session.commit()
            print(f"ALARM TRIGGERED: {msg}")
            return True, level
        except Exception as e:
            db.session.rollback()
            print(f"FAILED TO TRIGGER ALARM: {e}")
            
    return False, None

def get_alarm_configs():
    """
    5.5.1.1 阈值设置 (获取)
    """
    # 模拟配置
    return {
        "pressure": {"red": 45.0, "yellow": 35.0},
        "deformation": {"red": 15.0, "yellow": 8.0},
        "seismic": {"red": 100000.0, "yellow": 50000.0}
    }

def get_alarm_history(limit=50):
    """
    从数据库获取历史报警记录。
    """
    records = AlarmRecord.query.order_by(AlarmRecord.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat(),
            "type": r.alarm_type,
            "level": r.level,
            "value": r.value,
            "threshold": r.threshold,
            "message": r.message,
            "status": r.status
        } for r in records
    ]

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
