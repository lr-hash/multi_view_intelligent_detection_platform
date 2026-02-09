def test_get_borehole_fracture_data(client):
    """测试获取钻孔压裂数据 API"""
    response = client.get('/api/v1/visualization/fracture-data/1')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if len(data) > 0:
        item = data[0]
        assert 'segment_no' in item
        assert 'pressure' in item
        assert 'position' in item
        assert 'x' in item['position']
