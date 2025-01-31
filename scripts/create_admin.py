#!/usr/bin/env python3
import sys
sys.path.append('/opt/dcims')

from app import create_app, db
from app.models.user import User

def create_admin():
    app = create_app()
    with app.app_context():
        user = User(username='admin')
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
        print("Admin user created successfully")

if __name__ == '__main__':
    create_admin()