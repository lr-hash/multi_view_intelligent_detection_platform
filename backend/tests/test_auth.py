import pytest
from app.models import User
from app import db

def test_login_success(client, app):
    """测试成功登录"""
    with app.app_context():
        user = User(username='testuser')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

    response = client.post('/api/v1/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert data['user']['username'] == 'testuser'

def test_login_failure(client, app):
    """测试登录失败"""
    response = client.post('/api/v1/auth/login', json={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_protected_route_missing_token(client):
    """测试未携带 Token 访问受保护接口"""
    response = client.get('/api/v1/interfaces/status')
    assert response.status_code == 401
