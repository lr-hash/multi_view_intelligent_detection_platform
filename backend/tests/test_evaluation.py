from app.services.evaluation_service import calculate_evaluation_metrics

def test_calculate_evaluation_metrics():
    """验证评价算法的计算结果"""
    res = calculate_evaluation_metrics(1)
    assert 'metrics' in res
    assert 'efficiency' in res['metrics']
    assert 0 <= res['metrics']['efficiency'] <= 100
    assert res['borehole_id'] == 1
    assert res['level'] in ["稳定", "一般", "危险"]

def test_get_report_api(client):
    """测试获取评价概要 API"""
    response = client.get('/api/v1/evaluation/report/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'metrics' in data

def test_download_report_pdf(client):
    """测试下载 PDF 报告 API"""
    response = client.get('/api/v1/evaluation/report/1/download')
    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'
    assert len(response.data) > 0
    # 检查 PDF 魔数 (PDF 文件通常以 %PDF- 开头)
    assert response.data.startswith(b'%PDF-')
