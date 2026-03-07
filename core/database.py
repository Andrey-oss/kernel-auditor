# pylint: disable=line-too-long
'''Database manager'''

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TuningProfile(db.Model):
    '''ENTITY 1: Tuning Profile'''

    __tablename__ = 'tuning_profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)           # "Gaming", "Server", "Power saving"
    description = db.Column(db.Text)                           # Profile description
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)           # Currently active profile

    # Relationships with settings
    sysctl_settings = db.relationship('SysctlSetting', backref='profile', lazy=True, cascade='all, delete-orphan')
    cpu_settings = db.relationship('CpuSetting', backref='profile', lazy=True, cascade='all, delete-orphan')
    scheduler_settings = db.relationship('SchedulerSetting', backref='profile', lazy=True, cascade='all, delete-orphan')
    network_settings = db.relationship('NetworkSetting', backref='profile', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active,
            'settings_count': len(self.sysctl_settings) + len(self.cpu_settings) + 
                             len(self.scheduler_settings) + len(self.network_settings)
        }

class SysctlSetting(db.Model):
    '''ENTITY 2: Sysctl Settings'''

    __tablename__ = 'sysctl_settings'

    id = db.Column(db.Integer, primary_key=True)
    parameter = db.Column(db.String(200), nullable=False)      # vm.swappiness
    value = db.Column(db.String(500), nullable=False)          # 10
    description = db.Column(db.String(500))                    # "How aggressively to use swap"
    profile_id = db.Column(db.Integer, db.ForeignKey('tuning_profiles.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'parameter': self.parameter,
            'value': self.value,
            'description': self.description
        }

class CpuSetting(db.Model):
    '''ENTITY 3: CPU Settings'''

    __tablename__ = 'cpu_settings'

    id = db.Column(db.Integer, primary_key=True)
    cpu_core = db.Column(db.String(10), default='all')         # 'all' or 'cpu0', 'cpu1'
    parameter = db.Column(db.String(50), nullable=False)       # scaling_governor, min_freq
    value = db.Column(db.String(100), nullable=False)          # performance, 1400000
    profile_id = db.Column(db.Integer, db.ForeignKey('tuning_profiles.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'cpu_core': self.cpu_core,
            'parameter': self.parameter,
            'value': self.value
        }

class SchedulerSetting(db.Model):
    '''ENTITY 4: I/O Scheduler Settings'''

    __tablename__ = 'scheduler_settings'

    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(50), nullable=False) # sda, nvme0n1
    parameter = db.Column(db.String(50), nullable=False) # scheduler, nr_requests
    value = db.Column(db.String(100), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('tuning_profiles.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'device': self.device,
            'parameter': self.parameter,
            'value': self.value
        }

class NetworkSetting(db.Model):
    '''ENTITY 5: Network Settings'''

    __tablename__ = 'network_settings'

    id = db.Column(db.Integer, primary_key=True)
    parameter = db.Column(db.String(200), nullable=False)      # tcp_congestion_control, rmem_max
    value = db.Column(db.String(500), nullable=False)
    interface = db.Column(db.String(50), default='all')        # all, eth0, wlan0
    description = db.Column(db.String(500))
    profile_id = db.Column(db.Integer, db.ForeignKey('tuning_profiles.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'parameter': self.parameter,
            'value': self.value,
            'interface': self.interface,
            'description': self.description
        }

class AuditLog(db.Model):
    '''ENTITY 6: Audit History'''

    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True) # Index for faster sorting
    action = db.Column(db.String(50)) # apply_profile, change_sysctl, etc.
    category = db.Column(db.String(30), nullable=False) # profile, sysctl, cpu, network, scheduler
    parameter = db.Column(db.String(200))
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    status = db.Column(db.String(20)) # success, error
    profile_id = db.Column(db.Integer, db.ForeignKey('tuning_profiles.id'), nullable=True)

    # Relationship for profile name
    profile = db.relationship('TuningProfile', foreign_keys=[profile_id])

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'action': self.action,
            'category': self.category,
            'parameter': self.parameter,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'status': self.status,
            'profile_name': self.profile.name if self.profile else None
        }

    __table_args__ = (
        db.CheckConstraint(
            category.in_(['profile', 'sysctl', 'cpu', 'network', 'scheduler']),
            name='valid_categories'
        ),
    )
