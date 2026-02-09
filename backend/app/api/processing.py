from . import bp
from flask import jsonify, request
from app.services import processing_service
from .auth import token_required

#==============================================================================
# 5.2 数据处理模块
#==============================================================================

@bp.route('/processing/validate', methods=['POST'])
@token_required
def validate_data_endpoint(current_user):
    """
    Endpoint to trigger data validation.
    Expects data and a source identifier in the request body.
    """
    data = request.json.get('data')
    source = request.json.get('source')
    if not data or not source:
        return jsonify({"status": "error", "message": "Missing 'data' or 'source' in request"}), 400

    is_valid, message = processing_service.validate_data(data, source)
    if is_valid:
        return jsonify({"status": "success", "message": message})
    else:
        return jsonify({"status": "error", "message": message}), 422 # Unprocessable Entity

@bp.route('/processing/standardize', methods=['POST'])
@token_required
def standardize_data_endpoint(current_user):
    """
    Endpoint to trigger data alignment and standardization.
    """
    data = request.json
    standardized_data = processing_service.align_and_standardize(data)
    return jsonify(standardized_data)


@bp.route('/processing/fuse', methods=['POST'])
@token_required
def fuse_data_endpoint(current_user):
    """
    Endpoint to trigger data fusion.
    Expects JSON: {"pressure": float, "seismic": float, "deformation": float}
    """
    data = request.json
    pressure = data.get('pressure', 0)
    seismic = data.get('seismic', 0)
    deformation = data.get('deformation', 0)
    
    fusion_result = processing_service.fuse_data(pressure, seismic, deformation)
    return jsonify(fusion_result)
