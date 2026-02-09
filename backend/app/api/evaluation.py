from . import bp
from flask import jsonify, request
from app.services import evaluation_service

#==============================================================================
# 5.4 压裂效果评价模块
#==============================================================================

@bp.route('/evaluation/compare/<int:borehole_id>', methods=['GET'])
def get_comparison_endpoint(borehole_id):
    """
    5.4.1 数据对比分析
    Provides pre- and post-fracturing data for a specific data type.
    Query param 'type' can be 'pressure', 'microseismic', or 'deformation'.
    """
    data_type = request.args.get('type', 'pressure')
    if data_type not in ['pressure', 'microseismic', 'deformation']:
        return jsonify({"status": "error", "message": "Invalid data type specified"}), 400
    
    data = evaluation_service.get_comparison_data(borehole_id, data_type)
    return jsonify(data)

@bp.route('/evaluation/indices/<int:borehole_id>', methods=['GET'])
def get_indices_endpoint(borehole_id):
    """
    5.4.2 评价指标计算
    Provides calculated evaluation indices for a borehole.
    """
    data = evaluation_service.calculate_evaluation_indices(borehole_id)
    return jsonify(data)

@bp.route('/evaluation/report/<int:borehole_id>', methods=['GET'])
def get_report_endpoint(borehole_id):
    """
    5.4.3 评价报告生成
    Generates and returns a full evaluation report.
    """
    report = evaluation_service.generate_evaluation_report(borehole_id)
    return jsonify(report)
