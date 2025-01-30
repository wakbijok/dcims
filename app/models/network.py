from app import db

class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datacenter_id = db.Column(db.Integer, db.ForeignKey('datacenter.id'), nullable=False)
    description = db.Column(db.String(255))
    network_address = db.Column(db.String(45))
    gateway = db.Column(db.String(45))
    broadcast = db.Column(db.String(45))
    vlan_id = db.Column(db.Integer)