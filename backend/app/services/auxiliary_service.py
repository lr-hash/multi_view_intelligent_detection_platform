from datetime import datetime, timedelta
import random
from app import db, socketio
from app.models import AlarmRecord, SupportPressureData, MicroseismicEvent, RoadwayDeformation, FractureConstructionData, SystemConfig

def get_system_config(key, default=None):
    """获取单个配置项"""
    config = SystemConfig.query.filter_by(config_key=key).first()
    return config.config_value if config else default

def set_system_config(key, value, description=None):
    """更新或创建配置项"""
    config = SystemConfig.query.filter_by(config_key=key).first()
    if config:
        config.config_value = str(value)
        if description:
            config.description = description
    else:
        config = SystemConfig(config_key=key, config_value=str(value), description=description)
        db.session.add(config)
    
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

def get_all_configs():
    """获取所有系统配置"""
    configs = SystemConfig.query.all()
    return {c.config_key: c.config_value for c in configs}

def check_and_trigger_alarms(data_type, value, threshold_red, threshold_yellow, sid=None):
    """
    检查数值是否超过阈值，并触发报警记录。
    如果提供了 sid，则仅向该会话发送；否则全局广播。
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
            
            # WebSocket 推送
            alarm_data = {
                "id": alarm.id,
                "timestamp": alarm.timestamp.isoformat(),
                "type": alarm.alarm_type,
                "level": alarm.level,
                "value": alarm.value,
                "threshold": alarm.threshold,
                "message": alarm.message
            }
            
            if sid:
                socketio.emit('new_alarm', alarm_data, to=sid)
            else:
                socketio.emit('new_alarm', alarm_data)
            
            return True, level
        except Exception as e:
            db.session.rollback()
            print(f"FAILED TO TRIGGER ALARM: {e}")
            
    return False, None

def get_alarm_configs():
    """
    5.5.1.1 阈值设置 (获取)
    从数据库读取阈值，如果不存在则使用硬编码默认值。
    """
    return {
        "pressure": {
            "red": float(get_system_config("alarm_pressure_red", 45.0)),
            "yellow": float(get_system_config("alarm_pressure_yellow", 35.0))
        },
        "deformation": {
            "red": float(get_system_config("alarm_deformation_red", 15.0)),
            "yellow": float(get_system_config("alarm_deformation_yellow", 8.0))
        },
        "seismic": {
            "red": float(get_system_config("alarm_seismic_red", 100000.0)),
            "yellow": float(get_system_config("alarm_seismic_yellow", 50000.0))
        }
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
    通用多维数据查询服务。
    params: {
        "target": "pressure" | "seismic" | "deformation" | "fracture" | "alarm",
        "start_time": iso_str,
        "end_time": iso_str,
        "filters": { "key": "value" },
        "limit": int
    }
    """
    target = params.get('target')
    start_time = params.get('start_time')
    end_time = params.get('end_time')
    limit = params.get('limit', 100)
    
    # 映射目标到模型类和时间字段名
    mapping = {
        "pressure": (SupportPressureData, "record_time"),
        "seismic": (MicroseismicEvent, "event_time"),
        "deformation": (RoadwayDeformation, "record_time"),
        "fracture": (FractureConstructionData, "record_time"),
        "alarm": (AlarmRecord, "timestamp")
    }
    
    if target not in mapping:
        return {"error": f"Invalid query target: {target}"}
        
    model_class, time_field_name = mapping[target]
    query = model_class.query
    
    # 时间过滤
    time_field = getattr(model_class, time_field_name)
    if start_time:
        query = query.filter(time_field >= datetime.fromisoformat(start_time))
    if end_time:
        query = query.filter(time_field <= datetime.fromisoformat(end_time))
        
    # 执行查询
    records = query.order_by(time_field.desc()).limit(limit).all()
    
    # 简单序列化
    results = []
    for r in records:
        data = {c.name: getattr(r, c.name) for c in r.__table__.columns}
        for k, v in data.items():
            if isinstance(v, datetime):
                data[k] = v.isoformat()
        results.append(data)
        
    return results

def get_system_logs(level='INFO', limit=100):
    """
    5.5.3.2 系统日志
    """
    return [
        {"timestamp": "2026-02-02 23:01:00", "level": "INFO", "message": "User 'admin' logged in."},
        {"timestamp": "2026-02-02 23:02:00", "level": "WARNING", "message": "Interface 'FRACTURE_DB' is offline."},
    ]