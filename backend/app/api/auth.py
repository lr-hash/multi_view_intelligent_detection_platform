import jwt
import datetime
from flask import request, jsonify, current_app
from functools import wraps
from . import bp
from app.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(f"Login attempt: username={username}, password={password}")

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
    })

# --- User Management APIs (Admin Only) ---

@bp.route('/auth/users', methods=['GET'])
@token_required
def get_users(current_user):
    if current_user.role != 'ADMIN':
        return jsonify({'message': 'Admin privilege required!'}), 403
    
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'role': u.role
    } for u in users])

@bp.route('/auth/users', methods=['POST'])
@token_required
def create_user(current_user):
    if current_user.role != 'ADMIN':
        return jsonify({'message': 'Admin privilege required!'}), 403
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'USER')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    
    new_user = User(username=username, role=role)
    new_user.set_password(password)
    from app import db
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully', 'id': new_user.id}), 201

@bp.route('/auth/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    if current_user.role != 'ADMIN':
        return jsonify({'message': 'Admin privilege required!'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'username' in data:
        user.username = data['username']
    if 'role' in data:
        user.role = data['role']
    if 'password' in data and data['password']:
        user.set_password(data['password'])
        
    from app import db
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@bp.route('/auth/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if current_user.role != 'ADMIN':
        return jsonify({'message': 'Admin privilege required!'}), 403
    
    if current_user.id == user_id:
        return jsonify({'message': 'Cannot delete yourself!'}), 400
        
    user = User.query.get_or_404(user_id)
    from app import db
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
