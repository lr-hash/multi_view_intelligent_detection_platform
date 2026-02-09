import numpy as np
from app.services.processing_service import DataCleaner, CoordinateTransformer

def test_remove_outliers():
    """验证异常值剔除逻辑"""
    # 使用大量正常数据使标准差变小，从而使 100 成为显著异常
    data = [10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 100]
    cleaned = DataCleaner.remove_outliers(data, threshold=2)
    assert 100 not in cleaned

def test_fill_missing_values():
    """验证缺失值填充逻辑"""
    data = [10, np.nan, 12]
    filled = DataCleaner.fill_missing_values(data, strategy='mean')
    assert filled[1] == 11.0 # (10+12)/2

def test_coordinate_transformation():
    """验证坐标转换逻辑"""
    x, y, z = 100, 200, 50
    ge, gn, gz = CoordinateTransformer.local_to_global(x, y, z, offset_e=1000, offset_n=2000)
    assert ge == 1100
    assert gn == 2200
    assert gz == 50

def test_distance_calculation():
    """验证距离计算逻辑"""
    p1 = (0, 0, 0)
    p2 = (3, 4, 0)
    dist = CoordinateTransformer.calculate_distance(p1, p2)
    assert dist == 5.0

def test_fuse_api(client):
    """测试融合 API 接口"""
    payload = {
        "pressure": 30.0,
        "seismic": 10000.0,
        "deformation": 5.0
    }
    response = client.post('/api/v1/processing/fuse', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'stability_score' in data
    assert 'risk_level' in data
    # 压力 30MPa -> p_score = 75
    # 微震 10^4J -> s_score = 80
    # 变形 5mm/d -> d_score = 60
    # 0.4*75 + 0.35*80 + 0.25*60 = 30 + 28 + 15 = 73
    assert data['stability_score'] == 73.0
    assert data['risk_level'] == 'Green'
