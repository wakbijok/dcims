from app import db
from datetime import datetime

class Datacenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    hardware = db.relationship('Hardware', backref='datacenter', lazy=True)
    virtual_machines = db.relationship('VirtualMachine', backref='datacenter', lazy=True)
    networks = db.relationship('Network', backref='datacenter', lazy=True)