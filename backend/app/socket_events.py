from flask import request, current_app
from flask_socketio import disconnect, ConnectionRefusedError
from app import socketio
import jwt
from app.models import User

@socketio.on('connect')
def handle_connect(auth=None):
    """
    处理 WebSocket 连接事件，进行身份验证。
    """
    token = None
    
    # 尝试从 auth payload 获取
    if auth and 'token' in auth:
        token = auth['token']
    
    # 尝试从 args 获取 (备用)
    if not token:
        token = request.args.get('token')
        
    if not token:
        raise ConnectionRefusedError('authentication failed: missing token')
        
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
        user = User.query.get(user_id)
        if not user:
            raise ConnectionRefusedError('authentication failed: user not found')
            
        # 可以将用户信息存储在 session 中，以便后续事件使用
        # from flask import session
        # session['user_id'] = user.id
        print(f"WebSocket connected: User {user.username}")
        
    except jwt.ExpiredSignatureError:
        raise ConnectionRefusedError('authentication failed: token expired')
    except jwt.InvalidTokenError:
        raise ConnectionRefusedError('authentication failed: invalid token')
    except Exception as e:
        print(f"WebSocket connection error: {e}")
        raise ConnectionRefusedError('authentication failed')

@socketio.on('disconnect')
def handle_disconnect():
    print('WebSocket disconnected')
