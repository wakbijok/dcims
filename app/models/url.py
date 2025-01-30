from app import db

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