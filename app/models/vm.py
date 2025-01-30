from app import db

class VirtualMachine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datacenter_id = db.Column(db.Integer, db.ForeignKey('datacenter.id'), nullable=False)
    ip_address = db.Column(db.String(45), unique=True)
    hostname = db.Column(db.String(255))
    tech_stack = db.Column(db.String(100))
    description = db.Column(db.Text)
    environment = db.Column(db.Enum('Production', 'Staging', 'Development'))
    
    urls = db.relationship('URL', backref='virtual_machine', lazy=True)