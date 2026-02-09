from . import bp
from flask import jsonify, request
from app.services import auxiliary_service
from .auth import token_required

#==============================================================================
# 5.5 辅助功能模块
#==============================================================================

@bp.route('/alarms/config', methods=['GET'])
@token_required
def get_alarm_config(current_user):
    """ 5.5.1.1 阈值设置 (获取) """
    data = auxiliary_service.get_alarm_configs()
    return jsonify(data)

@bp.route('/alarms/history', methods=['GET'])
@token_required
def get_alarm_history(current_user):
    """ 5.5.1.2 报警触发与通知 (获取历史) """
    limit = request.args.get('limit', 50, type=int)
    data = auxiliary_service.get_alarm_history(limit)
    return jsonify(data)

@bp.route('/query', methods=['POST'])
@token_required
def query_data_endpoint(current_user):
    """ 5.5.2.1 多条件查询 """
    query_params = request.json
    data = auxiliary_service.query_data(query_params)
    return jsonify(data)

@bp.route('/logs/system', methods=['GET'])
@token_required
def get_system_logs(current_user):
    """ 5.5.3.2 系统日志 """
    level = request.args.get('level', 'INFO')
    limit = request.args.get('limit', 100, type=int)
    data = auxiliary_service.get_system_logs(level, limit)
    return jsonify(data)
