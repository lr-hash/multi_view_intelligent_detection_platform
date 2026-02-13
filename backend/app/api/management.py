import datetime
import pandas as pd
import io
from flask import request, jsonify
from . import bp
from .auth import token_required
from app import db
from app.models import (
    WorkingFace, DrillingSite, Borehole, BoreholeTrajectory,
    SupportPressureData, MicroseismicEvent, RoadwayDeformation,
    FractureConstructionData, SystemConfig, MonitoringStation,
    InterfaceLog, AlarmRecord
)

MODEL_MAP = {
    'working-face': WorkingFace,
    'drilling-site': DrillingSite,
    'borehole': Borehole,
    'borehole-trajectory': BoreholeTrajectory,
    'support-pressure': SupportPressureData,
    'microseismic': MicroseismicEvent,
    'deformation': RoadwayDeformation,
    'fracture-construction': FractureConstructionData,
    'system-config': SystemConfig,
    'monitoring-station': MonitoringStation,
    'interface-log': InterfaceLog,
    'alarm-record': AlarmRecord
}

def serialize_model(item):
    """通用序列化函数，处理 datetime 对象"""
    data = {}
    for c in item.__table__.columns:
        value = getattr(item, c.name)
        if isinstance(value, datetime.datetime):
            data[c.name] = value.isoformat()
        else:
            data[c.name] = value
    return data

def validate_data(model, data):
    """通用数据校验"""
    errors = []
    for key, value in data.items():
        if not hasattr(model, key):
            continue
        
        column = getattr(model, key).property.columns[0]
        
        # 必填项检查
        if not column.nullable and not column.primary_key and value is None:
            errors.append(f"字段 '{key}' 不能为空")
            
        # 物理量程校验
        if any(keyword in key.lower() for keyword in ['pressure', 'energy', 'flow_rate', 'volume', 'diameter', 'length']):
            if isinstance(value, (int, float)) and value < 0:
                errors.append(f"字段 '{key}' 不能为负数")
                
    return errors

@bp.route('/management/<table_name>', methods=['GET'])
@token_required
def get_data_list(current_user, table_name):
    model = MODEL_MAP.get(table_name)
    if not model:
        return jsonify({'message': 'Invalid table name'}), 404
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Basic filtering
    query = model.query
    for key, value in request.args.items():
        if key in ['page', 'per_page']:
            continue
        if hasattr(model, key):
            query = query.filter(getattr(model, key) == value)
    
    # Add default ordering if possible
    if hasattr(model, 'id'):
        query = query.order_by(model.id.desc())
    elif hasattr(model, 'timestamp'):
        query = query.order_by(model.timestamp.desc())
    elif hasattr(model, 'record_time'):
        query = query.order_by(model.record_time.desc())
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    items = [serialize_model(item) for item in pagination.items]
    
    return jsonify({
        'items': items,
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages
    })

@bp.route('/management/<table_name>', methods=['POST'])
@token_required
def create_data(current_user, table_name):
    if current_user.role != 'ADMIN':
        return jsonify({'message': 'Permission denied'}), 403
    
    model = MODEL_MAP.get(table_name)
    if not model:
        return jsonify({'message': 'Invalid table name'}), 404
    
    data = request.get_json()
    
    # 校验
    errors = validate_data(model, data)
    if errors:
        return jsonify({'message': 'Validation failed', 'errors': errors}), 400
        
    try:
        new_item = model()
        for key, value in data.items():
            if hasattr(model, key):
                # Handle datetime conversion if necessary
                column_type = getattr(model, key).type
                if 'DATETIME' in str(column_type).upper() and isinstance(value, str):
                    try:
                        value = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        pass
                setattr(new_item, key, value)
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify(serialize_model(new_item)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@bp.route('/management/<table_name>/<int:id>', methods=['PUT'])
@token_required
def update_data(current_user, table_name, id):
    if current_user.role != 'ADMIN':
        return jsonify({'message': 'Permission denied'}), 403
    
    model = MODEL_MAP.get(table_name)
    if not model:
        return jsonify({'message': 'Invalid table name'}), 404
    
    item = model.query.get_or_404(id)
    data = request.get_json()
    
    # 校验
    errors = validate_data(model, data)
    if errors:
        return jsonify({'message': 'Validation failed', 'errors': errors}), 400
        
    try:
        for key, value in data.items():
            if hasattr(model, key) and key != 'id':
                # Handle datetime conversion
                column_type = getattr(model, key).type
                if 'DATETIME' in str(column_type).upper() and isinstance(value, str):
                    try:
                        value = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        pass
                setattr(item, key, value)
        
        db.session.commit()
        return jsonify(serialize_model(item)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@bp.route('/management/<table_name>/<int:id>', methods=['DELETE'])
@token_required
def delete_data(current_user, table_name, id):
    if current_user.role != 'ADMIN':
        return jsonify({'message': 'Permission denied'}), 403
    
    model = MODEL_MAP.get(table_name)
    if not model:
        return jsonify({'message': 'Invalid table name'}), 404
    
    item = model.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@bp.route('/management/bulk-delete/<table_name>', methods=['POST'])
@token_required
def bulk_delete_data(current_user, table_name):
    if current_user.role != 'ADMIN':
        return jsonify({'message': 'Permission denied'}), 403
    
    model = MODEL_MAP.get(table_name)
    if not model:
        return jsonify({'message': 'Invalid table name'}), 404
    
    data = request.get_json()
    ids = data.get('ids', [])
    
    if not ids:
        return jsonify({'message': 'No IDs provided'}), 400
        
    try:
        model.query.filter(model.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'message': f'Successfully deleted {len(ids)} items'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@bp.route('/management/tables', methods=['GET'])
@token_required
def get_manageable_tables(current_user):
    """获取所有可管理的表列表及其元数据"""
    tables = []
    for key, model in MODEL_MAP.items():
        columns = []
        for c in model.__table__.columns:
            columns.append({
                'name': c.name,
                'type': str(c.type),
                'nullable': c.nullable,
                'primary_key': c.primary_key,
                'comment': c.comment or ''
            })
        tables.append({
            'name': key,
            'display_name': model.__doc__.strip().split('\n')[0] if model.__doc__ else key,
            'columns': columns
        })
    return jsonify(tables)

@bp.route('/management/import/<table_name>', methods=['POST'])
@token_required
def import_data(current_user, table_name):
    if current_user.role != 'ADMIN':
        return jsonify({'message': 'Permission denied'}), 403
    
    model = MODEL_MAP.get(table_name)
    if not model:
        return jsonify({'message': 'Invalid table name'}), 404
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    try:
        filename = file.filename.lower()
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file.read()))
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(file.read()))
        else:
            return jsonify({'message': 'Unsupported file format'}), 400
            
        df = df.where(pd.notnull(df), None) # Replace NaN with None
        
        imported_count = 0
        errors = []
        
        for index, row in df.iterrows():
            row_data = row.to_dict()
            # Basic validation for this row
            row_errors = validate_data(model, row_data)
            if row_errors:
                errors.append({'row': index + 2, 'errors': row_errors})
                continue
            
            try:
                item = model()
                for key, value in row_data.items():
                    if hasattr(model, key):
                        # Handle datetime
                        column_type = getattr(model, key).type
                        if 'DATETIME' in str(column_type).upper() and isinstance(value, str):
                            try:
                                # Try common formats
                                for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
                                    try:
                                        value = datetime.datetime.strptime(value, fmt)
                                        break
                                    except ValueError:
                                        continue
                            except Exception:
                                pass
                        setattr(item, key, value)
                db.session.add(item)
                imported_count += 1
            except Exception as e:
                errors.append({'row': index + 2, 'errors': [str(e)]})
        
        db.session.commit()
        
        return jsonify({
            'message': 'Import completed',
            'imported': imported_count,
            'failed': len(errors),
            'errors': errors
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
