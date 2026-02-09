from . import bp
from flask import jsonify, request, send_file
from app.services import evaluation_service
from .auth import token_required
import io

#==============================================================================
# 5.4 压裂效果评价模块
#==============================================================================

@bp.route('/evaluation/compare/<int:borehole_id>', methods=['GET'])
@token_required
def get_comparison_endpoint(current_user, borehole_id):
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
@token_required
def get_indices_endpoint(current_user, borehole_id):
    """
    5.4.2 评价指标计算
    Provides calculated evaluation indices for a borehole.
    """
    data = evaluation_service.calculate_evaluation_indices(borehole_id)
    return jsonify(data)

@bp.route('/evaluation/report/<int:borehole_id>', methods=['GET'])
@token_required
def get_report_endpoint(current_user, borehole_id):
    """
    5.4.3 评价报告生成 (JSON 概要)
    """
    metrics = evaluation_service.calculate_evaluation_metrics(borehole_id)
    return jsonify(metrics)

@bp.route('/evaluation/report/<int:borehole_id>/download', methods=['GET'])
@token_required
def download_report_pdf(current_user, borehole_id):
    """
    下载 PDF 版本的评价报告
    """
    metrics = evaluation_service.calculate_evaluation_metrics(borehole_id)
    pdf_content = evaluation_service.generate_pdf_report(borehole_id, metrics)
    
    return send_file(
        io.BytesIO(pdf_content),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Report_Borehole_{borehole_id}.pdf'
    )
