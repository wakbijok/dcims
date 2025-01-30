from app.main import db
from flask_login import UserMixin
from datetime import datetime

class Datacenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hardware = db.relationship('Hardware', backref='datacenter', lazy=True)
    virtual_machines = db.relationship('VirtualMachine', backref='datacenter', lazy=True)
    networks = db.relationship('Network', backref='datacenter', lazy=True)

class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datacenter_id = db.Column(db.Integer, db.ForeignKey('datacenter.id'), nullable=False)
    equipment = db.Column(db.String(100))
    serial_number = db.Column(db.String(100), unique=True)
    function_desc = db.Column(db.Text)
    brand_model = db.Column(db.String(100))
    ip_address = db.Column(db.String(45), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(255))
    ilo_login = db.Column(db.String(100))

class VirtualMachine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datacenter_id = db.Column(db.Integer, db.ForeignKey('datacenter.id'), nullable=False)
    ip_address = db.Column(db.String(45), unique=True)
    hostname = db.Column(db.String(255))
    tech_stack = db.Column(db.String(100))
    description = db.Column(db.Text)
    environment = db.Column(db.Enum('Production', 'Staging', 'Development'))
    urls = db.relationship('URL', backref='virtual_machine', lazy=True)

class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datacenter_id = db.Column(db.Integer, db.ForeignKey('datacenter.id'), nullable=False)
    description = db.Column(db.String(255))
    network_address = db.Column(db.String(45))
    gateway = db.Column(db.String(45))
    broadcast = db.Column(db.String(45))
    vlan_id = db.Column(db.Integer)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    is_public = db.Column(db.Boolean)
    environment = db.Column(db.String(50))
    ip_address = db.Column(db.String(45), db.ForeignKey('virtual_machine.ip_address'))
    protocol = db.Column(db.String(10))
    port = db.Column(db.Integer)
    remarks = db.Column(db.Text)