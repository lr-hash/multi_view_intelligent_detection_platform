from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """用户表"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='USER', comment='角色(ADMIN/USER)')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class WorkingFace(db.Model):
    """工作面基本参数"""
    __tablename__ = 'working_face'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, comment='工作面名称')
    length = db.Column(db.Float, comment='工作面长度(m)')
    advance_length = db.Column(db.Float, comment='推进长度(m)')
    mining_height = db.Column(db.Float, comment='采高(m)')
    start_date = db.Column(db.DateTime, comment='开采日期')
    description = db.Column(db.String(200))
    drilling_sites = db.relationship('DrillingSite', backref='working_face', lazy='dynamic')

    def __repr__(self):
        return f'<WorkingFace {self.name}>'

class DrillingSite(db.Model):
    """钻场信息"""
    __tablename__ = 'drilling_site'
    id = db.Column(db.Integer, primary_key=True)
    working_face_id = db.Column(db.Integer, db.ForeignKey('working_face.id'), comment='所属工作面ID')
    name = db.Column(db.String(100), nullable=False, comment='钻场名称')
    location = db.Column(db.String(200), comment='位置')
    coord_e = db.Column(db.Float, comment='大地坐标东坐标')
    coord_n = db.Column(db.Float, comment='大地坐标北坐标')
    coord_z = db.Column(db.Float, comment='巷道标高')
    boreholes = db.relationship('Borehole', backref='drilling_site', lazy='dynamic')

    def __repr__(self):
        return f'<DrillingSite {self.name}>'

class Borehole(db.Model):
    """钻孔信息"""
    __tablename__ = 'borehole'
    id = db.Column(db.Integer, primary_key=True)
    drilling_site_id = db.Column(db.Integer, db.ForeignKey('drilling_site.id'), nullable=False, comment='所属钻场ID')
    borehole_no = db.Column(db.String(50), nullable=False, comment='钻孔编号')
    diameter = db.Column(db.Float, comment='孔径(mm)')
    design_length = db.Column(db.Float, comment='设计长度(m)')
    azimuth = db.Column(db.Float, comment='设计方位角')
    dip_angle = db.Column(db.Float, comment='设计倾角')
    segments = db.Column(db.Integer, comment='计划压裂段数')
    trajectories = db.relationship('BoreholeTrajectory', backref='borehole', lazy='dynamic')

    def __repr__(self):
        return f'<Borehole {self.borehole_no}>'

class BoreholeTrajectory(db.Model):
    """钻孔轨迹"""
    __tablename__ = 'borehole_trajectory'
    id = db.Column(db.Integer, primary_key=True)
    borehole_id = db.Column(db.Integer, db.ForeignKey('borehole.id'), nullable=False, comment='所属钻孔ID')
    measured_depth = db.Column(db.Float, nullable=False, comment='测深(m)')
    dip_angle = db.Column(db.Float, comment='倾角')
    grid_azimuth = db.Column(db.Float, comment='方位角')
    coord_e = db.Column(db.Float, comment='坐标E')
    coord_n = db.Column(db.Float, comment='坐标N')
    coord_z = db.Column(db.Float, comment='坐标Z')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, comment='测量时间')

    def __repr__(self):
        return f'<BoreholeTrajectory {self.borehole_id} @ {self.measured_depth}m>'

class SupportPressureData(db.Model):
    """支架压力数据 (KJ653)"""
    __tablename__ = 'support_pressure_data'
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='记录时间')
    station_no = db.Column(db.Integer, comment='测站号')
    support_no = db.Column(db.Integer, comment='支架号')
    position = db.Column(db.String(50), comment='位置')
    p1 = db.Column(db.Float, comment='压力P1(MPa)')
    p2 = db.Column(db.Float, comment='压力P2(MPa)')
    p3 = db.Column(db.Float, comment='压力P3(MPa)')
    angle_x = db.Column(db.Float, comment='X方向角度')
    angle_y = db.Column(db.Float, comment='Y方向角度')
    status = db.Column(db.String(50), comment='状态')

    def __repr__(self):
        return f'<SupportPressureData {self.support_no} {self.p1}MPa>'

class MicroseismicEvent(db.Model):
    """微震事件数据 (SOS)"""
    __tablename__ = 'microseismic_event'
    id = db.Column(db.Integer, primary_key=True)
    event_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='事件时间')
    coord_x = db.Column(db.Float, comment='X坐标')
    coord_y = db.Column(db.Float, comment='Y坐标')
    coord_z = db.Column(db.Float, comment='Z坐标')
    energy = db.Column(db.Float, comment='能量(J)')

    def __repr__(self):
        return f'<MicroseismicEvent {self.event_time} {self.energy}J>'

class RoadwayDeformation(db.Model):
    """巷道变形数据"""
    __tablename__ = 'roadway_deformation'
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='记录时间')
    station_id = db.Column(db.String(100), comment='测站ID')
    top_bottom_deformation = db.Column(db.Float, comment='顶底板变形量(mm)')
    left_right_deformation = db.Column(db.Float, comment='两帮变形量(mm)')
    deformation_rate = db.Column(db.Float, comment='变形速率(mm/d)')

    def __repr__(self):
        return f'<RoadwayDeformation {self.station_id} {self.top_bottom_deformation}mm>'

class FractureConstructionData(db.Model):
    """压裂施工实时数据"""
    __tablename__ = 'fracture_construction_data'
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='记录时间')
    borehole_id = db.Column(db.Integer, db.ForeignKey('borehole.id'), nullable=False, comment='所属钻孔ID')
    segment_no = db.Column(db.Integer, comment='压裂段号')
    pressure = db.Column(db.Float, comment='施工压力(MPa)')
    flow_rate = db.Column(db.Float, comment='瞬时流量(m3/min)')
    total_volume = db.Column(db.Float, comment='累计排量(m3)')
    sand_concentration = db.Column(db.Float, comment='砂浓度(kg/m3)')

    def __repr__(self):
        return f'<FractureConstructionData {self.borehole_id} Seg {self.segment_no}>'

class InterfaceLog(db.Model):
    """接口调用日志"""
    __tablename__ = 'interface_log'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='日志时间')
    interface_name = db.Column(db.String(100), nullable=False, comment='接口名称/来源')
    status = db.Column(db.String(20), nullable=False, comment='状态(SUCCESS/ERROR)')
    message = db.Column(db.Text, comment='详细消息')
    payload = db.Column(db.Text, comment='原始数据载荷(可选)')

    def __repr__(self):
        return f'<InterfaceLog {self.interface_name} {self.status}>'

class AlarmRecord(db.Model):
    """报警历史记录"""
    __tablename__ = 'alarm_record'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='报警时间')
    alarm_type = db.Column(db.String(50), nullable=False, comment='报警类型(矿压/微震/变形/压裂)')
    level = db.Column(db.String(20), nullable=False, comment='报警级别(RED/YELLOW)')
    value = db.Column(db.Float, comment='触发值')
    threshold = db.Column(db.Float, comment='设定的阈值')
    message = db.Column(db.Text, comment='报警描述')
    status = db.Column(db.String(20), default='PENDING', comment='处理状态(PENDING/ACKNOWLEDGED/CLEARED)')
    handler_remark = db.Column(db.Text, comment='处理意见')

    def __repr__(self):
        return f'<AlarmRecord {self.alarm_type} {self.level} @ {self.timestamp}>'

class SystemConfig(db.Model):
    """系统运行配置 (键值对)"""
    __tablename__ = 'system_config'
    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    config_value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SystemConfig {self.config_key}: {self.config_value}>'

class MonitoringStation(db.Model):
    """监测测点信息"""
    __tablename__ = 'monitoring_station'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(50), unique=True, nullable=False, comment='测点编号/ID')
    type = db.Column(db.String(50), nullable=False, comment='测点类型(矿压/微震/变形)')
    location = db.Column(db.String(200), comment='安装位置')
    coord_x = db.Column(db.Float, comment='X坐标')
    coord_y = db.Column(db.Float, comment='Y坐标')
    coord_z = db.Column(db.Float, comment='Z坐标')
    install_date = db.Column(db.DateTime, comment='安装日期')
    status = db.Column(db.String(20), default='ACTIVE', comment='状态(ACTIVE/INACTIVE)')

    def __repr__(self):
        return f'<MonitoringStation {self.station_id} ({self.type})>'
