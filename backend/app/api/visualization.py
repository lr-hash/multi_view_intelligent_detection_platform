from . import bp
from flask import jsonify, request
from app.services import visualization_service
from .auth import token_required

#==============================================================================
# 5.3 可视化模块
#==============================================================================

@bp.route('/visualize/drilling_design', methods=['GET'])
@token_required
def get_drilling_design_data(current_user):
    """ 5.3.1 压裂设计可视化 """
    data = visualization_service.get_drilling_design_data()
    return jsonify(data)

@bp.route('/visualization/fracture-data/<int:borehole_id>', methods=['GET'])
@token_required
def get_borehole_fracture_data(current_user, borehole_id):
    """ 获取钻孔压裂详情数据 """
    data = visualization_service.get_borehole_fracture_data(borehole_id)
    return jsonify(data)

@bp.route('/visualization/microseismic-points', methods=['GET'])
@token_required
def get_microseismic_points(current_user):
    """ 获取微震事件 3D 点数据 """
    data = visualization_service.get_microseismic_points()
    return jsonify(data)

@bp.route('/dashboard/core_metrics', methods=['GET'])
@token_required
def get_dashboard_metrics(current_user):
    """ 5.3.2 数据看板 - 核心指标实时展示 """
    data = visualization_service.get_dashboard_core_metrics()
    return jsonify(data)

@bp.route('/dashboard/fusion_score', methods=['GET'])
@token_required
def get_dashboard_fusion_score(current_user):
    """ 获取实时融合稳定指数 """
    data = visualization_service.get_realtime_fusion_score()
    return jsonify(data)

@bp.route('/trends/pressure', methods=['GET'])
@token_required
def get_pressure_trends(current_user):
    """ 5.3.3 数据趋势图 - 矿压 """
    time_range = request.args.get('range', '24h')
    data = visualization_service.get_pressure_trend_data(time_range)
    return jsonify(data)

@bp.route('/trends/microseismic_frequency', methods=['GET'])
@token_required
def get_microseismic_frequency(current_user):
    """ 数据趋势图 - 微震频次 """
    time_range = request.args.get('range', '24h')
    data = visualization_service.get_microseismic_frequency_data(time_range)
    return jsonify(data)

@bp.route('/trends/deformation', methods=['GET'])
@token_required
def get_deformation_trends(current_user):
    """ 数据趋势图 - 巷道变形 """
    time_range = request.args.get('range', '24h')
    data = visualization_service.get_deformation_trend_data(time_range)
    return jsonify(data)
