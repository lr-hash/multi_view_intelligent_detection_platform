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
