from app.services.auxiliary_service import check_and_trigger_alarms, get_alarm_history
from app.models import AlarmRecord
from app import db

def test_alarm_triggering(app):
    """测试报警触发逻辑"""
    # 模拟触发黄色报警
    triggered, level = check_and_trigger_alarms("Pressure", 40.0, 45.0, 35.0)
    assert triggered is True
    assert level == "YELLOW"
    
    # 模拟触发红色报警
    triggered, level = check_and_trigger_alarms("Pressure", 50.0, 45.0, 35.0)
    assert triggered is True
    assert level == "RED"
    
    # 正常值不触发
    triggered, level = check_and_trigger_alarms("Pressure", 20.0, 45.0, 35.0)
    assert triggered is False
    assert level is None

def test_get_alarm_history(app):
    """测试报警历史查询"""
    # 先注入几条报警
    check_and_trigger_alarms("TestType", 100, 90, 80)
    check_and_trigger_alarms("TestType", 110, 90, 80)
    
    history = get_alarm_history()
    assert len(history) >= 2
    assert history[0]['type'] == "TestType"

def test_query_api(client, app):
    """测试多条件查询 API"""
    # 注入一条矿压数据
    from app.models import SupportPressureData
    from datetime import datetime
    with app.app_context():
        db.session.add(SupportPressureData(support_no=999, p1=30.0, record_time=datetime.fromisoformat("2026-02-09T10:00:00")))
        db.session.commit()
        
    payload = {
        "target": "pressure",
        "start_time": "2026-02-09T09:00:00",
        "end_time": "2026-02-09T11:00:00"
    }
    response = client.post('/api/v1/query', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert data[0]['support_no'] == 999
