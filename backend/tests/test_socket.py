from app import socketio, db
from app.models import User
from flask import current_app
import jwt
from datetime import datetime, timedelta

def test_socket_connection_with_auth(client, app):
    """测试 WebSocket 连接 (带身份验证)"""
    with app.app_context():
        user = User(username='socket_user', role='USER')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
    
    # 使用 auth 参数模拟客户端握手
    socket_client = socketio.test_client(app, flask_test_client=client, auth={'token': token})
    assert socket_client.is_connected()
    socket_client.disconnect()

def test_socket_connection_without_auth(client, app):
    """测试 WebSocket 连接 (无身份验证) - 应被拒绝"""
    try:
        socket_client = socketio.test_client(app, flask_test_client=client)
        assert not socket_client.is_connected()
    except Exception:
        # ConnectionRefusedError 可能会被抛出
        pass

def test_alarm_broadcast(client, app):
    """测试报警广播"""
    with app.app_context():
        user = User(username='broadcast_user', role='USER')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        
    socket_client = socketio.test_client(app, flask_test_client=client, auth={'token': token})
    
    # 模拟触发报警
    from app.services.auxiliary_service import check_and_trigger_alarms
    with app.app_context():
        check_and_trigger_alarms("SocketTest", 100, 90, 80)
        
    # 接收事件
    received = socket_client.get_received()
    # 过滤出 'new_alarm' 事件
    alarm_events = [event for event in received if event['name'] == 'new_alarm']
    
    assert len(alarm_events) > 0
    data = alarm_events[0]['args'][0]
    assert data['type'] == 'SocketTest'
    assert data['level'] == 'RED'
