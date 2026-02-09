import json
from app.models import SupportPressureData, MicroseismicEvent, InterfaceLog

def test_ingest_kj653(client, app):
    """测试 KJ653 数据摄入 API"""
    payload = {
        "records": [
            {
                "support_no": 101,
                "p1": 25.5,
                "record_time": "2026-02-09T12:30:00"
            }
        ]
    }
    response = client.post('/api/v1/ingest/kj653', json=payload)
    assert response.status_code == 201
    
    with app.app_context():
        # 验证数据
        data = SupportPressureData.query.filter_by(support_no=101).first()
        assert data is not None
        assert data.p1 == 25.5
        
        # 验证日志
        log = InterfaceLog.query.filter_by(interface_name='KJ653_API').first()
        assert log is not None
        assert log.status == 'SUCCESS'

def test_ingest_sos(client, app):
    """测试 SOS 数据摄入 API"""
    payload = {
        "events": [
            {
                "energy": 5000.0,
                "coord_x": 123.4,
                "event_time": "2026-02-09T12:35:00"
            }
        ]
    }
    response = client.post('/api/v1/ingest/sos', json=payload)
    assert response.status_code == 201
    
    with app.app_context():
        event = MicroseismicEvent.query.filter_by(energy=5000.0).first()
        assert event is not None
        
        log = InterfaceLog.query.filter_by(interface_name='SOS_API').first()
        assert log is not None

def test_get_interface_status(client, app):
    """测试获取接口状态 API"""
    # 先发送一次数据以产生日志
    client.post('/api/v1/ingest/kj653', json={"records": []})
    
    response = client.get('/api/v1/interfaces/status')
    assert response.status_code == 200
    data = response.get_json()
    assert 'KJ653_API' in data
    assert data['KJ653_API']['status'] == 'Online'
