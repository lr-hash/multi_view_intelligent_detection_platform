from . import bp
from flask import jsonify, request
from app.services import visualization_service

#==============================================================================
# 5.3 可视化模块
#==============================================================================

@bp.route('/visualize/drilling_design', methods=['GET'])
def get_drilling_design_data():
    """ 5.3.1 压裂设计可视化 """
    data = visualization_service.get_drilling_design_data()
    return jsonify(data)

@bp.route('/dashboard/core_metrics', methods=['GET'])
def get_dashboard_metrics():
    """ 5.3.2 数据看板 - 核心指标实时展示 """
    data = visualization_service.get_dashboard_core_metrics()
    return jsonify(data)

@bp.route('/trends/pressure', methods=['GET'])
def get_pressure_trends():
    """ 5.3.3 数据趋势图 - 矿压 """
    time_range = request.args.get('range', '24h')
    data = visualization_service.get_pressure_trend_data(time_range)
    return jsonify(data)

@bp.route('/trends/microseismic_frequency', methods=['GET'])
def get_microseismic_frequency():
    """ 数据趋势图 - 微震频次 """
    time_range = request.args.get('range', '24h')
    data = visualization_service.get_microseismic_frequency_data(time_range)
    return jsonify(data)

@bp.route('/trends/deformation', methods=['GET'])
def get_deformation_trends():
    """ 数据趋势图 - 巷道变形 """
    time_range = request.args.get('range', '24h')
    data = visualization_service.get_deformation_trend_data(time_range)
    return jsonify(data)
