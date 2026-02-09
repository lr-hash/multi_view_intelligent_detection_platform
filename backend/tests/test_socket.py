from app import socketio

def test_socket_connection(client, app):
    """测试 WebSocket 连接"""
    socket_client = socketio.test_client(app, flask_test_client=client)
    assert socket_client.is_connected()
    socket_client.disconnect()

def test_alarm_broadcast(client, app):
    """测试报警广播"""
    socket_client = socketio.test_client(app, flask_test_client=client)
    
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
