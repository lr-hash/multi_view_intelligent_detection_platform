from app.services.auxiliary_service import check_and_trigger_alarms, get_alarm_history
from app.models import AlarmRecord, User
from app import db
from datetime import datetime

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
    with app.app_context():
        # 清理可能存在的冲突数据或确保环境干净
        db.session.add(SupportPressureData(support_no=999, p1=30.0, record_time=datetime.fromisoformat("2026-02-09T10:00:00")))
        user = User.query.filter_by(username='test_query_user').first()
        if not user:
            user = User(username='test_query_user')
            user.set_password('pass')
            db.session.add(user)
        db.session.commit()
        
    # 获取 Token
    login_resp = client.post('/api/v1/auth/login', json={'username': 'test_query_user', 'password': 'pass'})
    token = login_resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        "target": "pressure",
        "start_time": "2026-02-09T09:00:00",
        "end_time": "2026-02-09T11:00:00"
    }
    response = client.post('/api/v1/query', json=payload, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert data[0]['support_no'] == 999

def test_dynamic_config(client, app):
    """测试动态配置更新"""
    # 模拟管理员登录获取 Token
    with app.app_context():
        user = User.query.filter_by(username='admin_test').first()
        if not user:
            user = User(username='admin_test', role='ADMIN')
            user.set_password('admin123')
            db.session.add(user)
            db.session.commit()
    
    login_resp = client.post('/api/v1/auth/login', json={'username': 'admin_test', 'password': 'admin123'})
    token = login_resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # 更新阈值
    new_config = {"alarm_pressure_red": 55.5}
    resp = client.post('/api/v1/alarms/config', json=new_config, headers=headers)
    assert resp.status_code == 200

    # 验证获取到的阈值已更新
    resp = client.get('/api/v1/alarms/config', headers=headers)
    data = resp.get_json()
    assert data['pressure']['red'] == 55.5