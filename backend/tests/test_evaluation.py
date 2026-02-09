from app.services.evaluation_service import calculate_evaluation_metrics

def test_calculate_evaluation_metrics():
    """验证评价算法的计算结果"""
    res = calculate_evaluation_metrics(1)
    assert 'metrics' in res
    assert 'efficiency' in res['metrics']
    assert 0 <= res['metrics']['efficiency'] <= 100
    assert res['borehole_id'] == 1
    assert res['level'] in ["稳定", "一般", "危险"]
