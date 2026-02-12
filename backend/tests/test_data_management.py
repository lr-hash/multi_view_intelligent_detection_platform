import pytest
import json
from app.models import User, WorkingFace, MonitoringStation
from app import db

def get_admin_token(client):
    # Setup admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', role='ADMIN')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    
    response = client.post('/api/v1/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    return response.get_json()['token']

def test_get_management_list_admin(client, app):
    with app.app_context():
        token = get_admin_token(client)
        
        # Add some data
        wf = WorkingFace(name="Test Face 1")
        db.session.add(wf)
        db.session.commit()
        
        response = client.get('/api/v1/management/working-face', headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['items']) >= 1
        # Check if "Test Face 1" is in the results
        names = [item['name'] for item in data['items']]
        assert "Test Face 1" in names

def test_get_management_list_unauthorized(client):
    response = client.get('/api/v1/management/working-face')
    assert response.status_code == 401

def test_create_data_admin(client, app):
    with app.app_context():
        token = get_admin_token(client)
        
        payload = {
            'station_id': 'MS-001',
            'type': '矿压',
            'location': '巷道1'
        }
        response = client.post('/api/v1/management/monitoring-station', 
                               json=payload,
                               headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 201
        
        ms = MonitoringStation.query.filter_by(station_id='MS-001').first()
        assert ms is not None
        assert ms.location == '巷道1'

def test_update_data_admin(client, app):
    with app.app_context():
        token = get_admin_token(client)
        
        wf = WorkingFace(name="Old Name")
        db.session.add(wf)
        db.session.commit()
        wf_id = wf.id
        
        payload = {'name': 'New Name'}
        response = client.put(f'/api/v1/management/working-face/{wf_id}', 
                              json=payload,
                              headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        
        wf_updated = WorkingFace.query.get(wf_id)
        assert wf_updated.name == "New Name"

def test_delete_data_admin(client, app):
    with app.app_context():
        token = get_admin_token(client)
        
        wf = WorkingFace(name="To Delete")
        db.session.add(wf)
        db.session.commit()
        wf_id = wf.id
        
        response = client.delete(f'/api/v1/management/working-face/{wf_id}', 
                                 headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        
        assert WorkingFace.query.get(wf_id) is None

def test_import_data_admin(client, app):
    with app.app_context():
        token = get_admin_token(client)
        
        # Create a dummy CSV for testing
        import io
        csv_data = "station_id,type,location\nIMP-001,矿压,巷道2\nIMP-002,微震,巷道3"
        data = {
            'file': (io.BytesIO(csv_data.encode()), 'test.csv')
        }
        
        response = client.post('/api/v1/management/import/monitoring-station',
                                data=data,
                                content_type='multipart/form-data',
                                headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        assert response.get_json()['imported'] == 2
        
        from app.models import MonitoringStation
        ms = MonitoringStation.query.filter_by(station_id='IMP-001').first()
        assert ms is not None
        assert ms.location == '巷道2'
