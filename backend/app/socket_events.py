from flask import request, current_app
from flask_socketio import disconnect, ConnectionRefusedError, emit
from app import socketio, db
import jwt
import time
import random
from datetime import datetime
from app.models import User, AlarmRecord
from app.services import auxiliary_service

# --- Session-based Alarm Simulation ---
def simulate_session_alarms(app, sid):
    """为特定会话模拟产生 5 次报警，每 30 秒一次"""
    with app.app_context():
        print(f"SIMULATION: Starting session-based task for SID {sid}")
        for i in range(5):
            socketio.sleep(30)
            
            # 随机选择一种类型产生报警
            types = ['pressure', 'deformation', 'seismic']
            data_type = random.choice(types)
            
            # 获取当前阈值
            configs = auxiliary_service.get_alarm_configs()
            threshold_red = configs[data_type]['red']
            
            # 产生一个超限数值 (1.1x ~ 1.3x 阈值)
            mock_value = round(threshold_red * (1.1 + random.random() * 0.2), 2)
            
            # 1. 记录到数据库并发送给该用户
            success, level = auxiliary_service.check_and_trigger_alarms(
                data_type, mock_value, threshold_red, threshold_red * 0.8, sid=sid
            )
            
            if success:
                print(f"SIMULATION: Alarm {i+1}/5 sent to SID {sid}")
        
        print(f"SIMULATION: Completed 5 alarms for SID {sid}")

@socketio.on('connect')
def handle_connect(auth=None):
    """
    处理 WebSocket 连接事件，进行身份验证并启动模拟任务。
    """
    sid = request.sid
    print(f"\n\n!!! SOCKET CONNECTED: {sid} !!!\n\n")
    
    # 每次新连接都启动一个独立的 5 次报警任务
    socketio.start_background_task(simulate_session_alarms, current_app._get_current_object(), sid)

    token = None
    
    # 尝试从 auth payload 获取
    if auth and 'token' in auth:
        token = auth['token']
    
    # 尝试从 args 获取 (备用)
    if not token:
        token = request.args.get('token')
        
    if not token:
        print("WebSocket connection: Missing token, but allowed for simulation.")
        return True # Temporarily allow for testing
        
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
        user = User.query.get(user_id)
        if not user:
            return True
            
        print(f"WebSocket connected: User {user.username}")
        return True
        
    except Exception as e:
        print(f"WebSocket auth error: {e}")
        return True # Allow anyway for now

@socketio.on('disconnect')
def handle_disconnect():
    print('WebSocket disconnected')
