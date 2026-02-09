from flask import request, jsonify
from . import bp
from app.services import integration_service
from .auth import token_required

#==============================================================================
# 5.1 集成接口模块
#==============================================================================

@bp.route('/ingest/kj653', methods=['POST'])
@token_required
def ingest_kj653_data(current_user):
    """
    5.1.1 (1) KJ653 煤矿顶板动态监测系统对接接口
    """
    data = request.json
    success, message = integration_service.save_kj653_data(data)
    if success:
        return jsonify({'status': 'success', 'message': message}), 201
    else:
        return jsonify({'status': 'error', 'message': message}), 500

@bp.route('/ingest/sos', methods=['POST'])
@token_required
def ingest_sos_data(current_user):
    """
    5.1.1 (2) SOS 微震系统对接接口
    """
    data = request.json
    success, message = integration_service.save_sos_data(data)
    if success:
        return jsonify({'status': 'success', 'message': message}), 201
    else:
        return jsonify({'status': 'error', 'message': message}), 500

@bp.route('/interfaces/status', methods=['GET'])
@token_required
def get_interface_status(current_user):
    """
    5.1.2 (1) 接口状态监测
    """
    statuses = integration_service.get_all_interface_statuses()
    return jsonify(statuses)

@bp.route('/interfaces/logs', methods=['GET'])
@token_required
def get_interface_logs(current_user):
    """
    5.1.2 (2) 接口日志记录
    """
    limit = request.args.get('limit', 100, type=int)
    logs = integration_service.get_all_interface_logs(limit)
    return jsonify(logs)

@bp.route('/interfaces/config', methods=['GET', 'POST'])
@token_required
def manage_interface_config(current_user):
    """
    5.1.2 (3) 接口参数配置
    """
    if request.method == 'POST':
        # 仅限管理员修改配置
        if current_user.role != 'ADMIN':
            return jsonify({'message': 'Admin privilege required!'}), 403
            
        config_data = request.json
        integration_service.save_interface_configurations(config_data)
        return jsonify({'status': 'success', 'message': 'Configuration saved.'})
    else:
        configs = integration_service.get_interface_configurations()
        return jsonify(configs)
