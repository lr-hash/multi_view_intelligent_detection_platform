from app.models import FractureConstructionData, InterfaceLog, Borehole, DrillingSite
from app import db

def test_new_interface_log(app):
    """验证接口日志模型的创建"""
    log = InterfaceLog(
        interface_name='TEST_IF',
        status='SUCCESS',
        message='Test message',
        payload='{"key": "value"}'
    )
    db.session.add(log)
    db.session.commit()
    
    retrieved = InterfaceLog.query.filter_by(interface_name='TEST_IF').first()
    assert retrieved is not None
    assert retrieved.status == 'SUCCESS'
    assert retrieved.message == 'Test message'

def test_new_fracture_data(app):
    """验证压裂施工数据模型的创建"""
    # 需要先创建钻场和钻孔
    site = DrillingSite(name='Test Site')
    db.session.add(site)
    db.session.commit()
    
    hole = Borehole(drilling_site_id=site.id, borehole_no='H001')
    db.session.add(hole)
    db.session.commit()
    
    data = FractureConstructionData(
        borehole_id=hole.id,
        segment_no=1,
        pressure=15.5,
        flow_rate=2.0,
        total_volume=100.5,
        sand_concentration=50.0
    )
    db.session.add(data)
    db.session.commit()
    
    retrieved = FractureConstructionData.query.filter_by(borehole_id=hole.id).first()
    assert retrieved is not None
    assert retrieved.pressure == 15.5
    assert retrieved.segment_no == 1
