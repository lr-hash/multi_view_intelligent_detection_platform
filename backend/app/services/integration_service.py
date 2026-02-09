import json
from app import db
from app.models import SupportPressureData, MicroseismicEvent, InterfaceLog
from datetime import datetime

def _log_interface_call(name, status, message, payload=None):
    """辅助函数：记录接口调用日志"""
    try:
        log = InterfaceLog(
            interface_name=name,
            status=status,
            message=message,
            payload=json.dumps(payload) if payload else None
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"FAILED TO LOG: {e}")

def save_kj653_data(data):
    """
    Saves KJ653 data to the database.
    Expects data format: {"records": [...list of SupportPressureData fields...]}
    """
    try:
        records = data.get('records', [])
        count = 0
        for r in records:
            # 转换时间字符串为 datetime 对象 (假设输入是 ISO 格式)
            if 'record_time' in r and isinstance(r['record_time'], str):
                r['record_time'] = datetime.fromisoformat(r['record_time'])
            
            new_record = SupportPressureData(**r)
            db.session.add(new_record)
            count += 1
        
        db.session.commit()
        msg = f"Successfully saved {count} KJ653 records."
        _log_interface_call("KJ653_API", "SUCCESS", msg)
        return True, msg
    except Exception as e:
        db.session.rollback()
        err_msg = f"KJ653 Save Error: {str(e)}"
        _log_interface_call("KJ653_API", "ERROR", err_msg, payload=data)
        return False, err_msg

def save_sos_data(data):
    """
    Saves SOS data to the database.
    Expects data format: {"events": [...list of MicroseismicEvent fields...]}
    """
    try:
        events = data.get('events', [])
        count = 0
        for e in events:
            if 'event_time' in e and isinstance(e['event_time'], str):
                e['event_time'] = datetime.fromisoformat(e['event_time'])
            
            new_event = MicroseismicEvent(**e)
            db.session.add(new_event)
            count += 1
            
        db.session.commit()
        msg = f"Successfully saved {count} SOS events."
        _log_interface_call("SOS_API", "SUCCESS", msg)
        return True, msg
    except Exception as e:
        db.session.rollback()
        err_msg = f"SOS Save Error: {str(e)}"
        _log_interface_call("SOS_API", "ERROR", err_msg, payload=data)
        return False, err_msg

def get_all_interface_statuses():
    """
    Checks and returns the status of all data interfaces by checking the last update time.
    """
    interfaces = ["KJ653_API", "SOS_API"]
    results = {}
    
    for name in interfaces:
        last_log = InterfaceLog.query.filter_by(interface_name=name).order_by(InterfaceLog.timestamp.desc()).first()
        if last_log:
            results[name] = {
                "status": "Online" if last_log.status == "SUCCESS" else "Error",
                "details": f"Last sync: {last_log.timestamp.isoformat()}, Message: {last_log.message}"
            }
        else:
            results[name] = { "status": "Unknown", "details": "No logs found for this interface." }
            
    return results

def get_all_interface_logs(limit=100):
    """
    Retrieves the latest interface logs from the database.
    """
    logs = InterfaceLog.query.order_by(InterfaceLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "timestamp": log.timestamp.isoformat(),
            "interface": log.interface_name,
            "status": log.status,
            "message": log.message
        } for log in logs
    ]

def get_interface_configurations():
    """
    Retrieves the current interface configurations.
    """
    # This is a placeholder. It would read from a configuration file or database table.
    print("SERVICE: Retrieving interface configurations (simulated).")
    return {
        "kj653": {"ip": "192.168.1.10", "port": 1433, "interval": 10},
        "sos": {"ip": "192.168.1.20", "port": 1433, "interval": 5}
    }

def save_interface_configurations(config_data):
    """
    Saves new interface configurations.
    """
    # This is a placeholder.
    print(f"SERVICE: Saving new interface configurations (simulated): {config_data}")
    return True
