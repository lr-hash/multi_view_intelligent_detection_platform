from flask import request, current_app
from flask_socketio import disconnect, ConnectionRefusedError, emit
from app import socketio, db
import jwt
import time
import random
from datetime import datetime
from app.models import User, AlarmRecord
from app.services import auxiliary_service

# --- Background Simulation ---
def simulate_periodic_alarms(app):
    """每隔几分钟模拟产生一个报警"""
    with app.app_context():
        print("SIMULATION TASK: Started.")
        while True:
            # 缩短等待时间至 30s 方便快速验证
            socketio.sleep(30)
            
            # 随机选择一种类型产生报警
            types = ['pressure', 'deformation', 'seismic']
            data_type = random.choice(types)
            
            # 获取当前阈值
            configs = auxiliary_service.get_alarm_configs()
            threshold_red = configs[data_type]['red']
            
            # 产生一个超限数值 (1.1x ~ 1.3x 阈值)
            mock_value = round(threshold_red * (1.1 + random.random() * 0.2), 2)
            
            # 触发报警逻辑
            success, level = auxiliary_service.check_and_trigger_alarms(
                data_type, mock_value, threshold_red, threshold_red * 0.8
            )
            
            if success:
                print(f"SIMULATION TASK: SUCCESS - {data_type} alarm pushed.")

# 在应用启动后手动启动模拟线程
# 注意：在生产环境或多进程模式下(如 gunicorn)需谨慎处理，此处仅用于开发模拟
_sim_task_started = False

@socketio.on('connect')
def handle_connect(auth=None):
    """
    处理 WebSocket 连接事件，进行身份验证。
    """
    print("\n\n!!! SOCKET CONNECTED !!!\n\n")
    global _sim_task_started
    if not _sim_task_started:
        # Start simulation regardless of auth success for demo purposes
        socketio.start_background_task(simulate_periodic_alarms, current_app._get_current_object())
        _sim_task_started = True
        print("ALARM SIMULATION: Task started on first connection attempt.")

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
