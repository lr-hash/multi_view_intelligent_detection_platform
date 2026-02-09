from . import bp
from flask import jsonify, request
from app.services import processing_service

#==============================================================================
# 5.2 数据处理模块
#==============================================================================

@bp.route('/processing/validate', methods=['POST'])
def validate_data_endpoint():
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
def standardize_data_endpoint():
    """
    Endpoint to trigger data alignment and standardization.
    """
    data = request.json
    standardized_data = processing_service.align_and_standardize(data)
    return jsonify(standardized_data)


@bp.route('/processing/fuse', methods=['POST'])
def fuse_data_endpoint():
    """
    Endpoint to trigger data fusion.
    Expects a dictionary of data streams.
    """
    data_streams = request.json
    fusion_result = processing_service.fuse_data(data_streams)
    return jsonify(fusion_result)
