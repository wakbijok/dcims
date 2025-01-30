from app import db

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