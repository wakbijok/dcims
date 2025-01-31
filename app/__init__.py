from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from app.utils.logger import setup_logger
from app.errors import register_error_handlers

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    setup_logger(app)
    register_error_handlers(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    
    with app.app_context():
        from .models import User, Datacenter, Hardware, VirtualMachine, Network, URL
        from .routes import auth, datacenter, hardware, vm, network, url, dashboard, search
        
        db.create_all()  # Create database tables
        
        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(dashboard, url_prefix='/')
        app.register_blueprint(datacenter, url_prefix='/datacenter')
        app.register_blueprint(hardware, url_prefix='/hardware')
        app.register_blueprint(vm, url_prefix='/vm')
        app.register_blueprint(network, url_prefix='/network')
        app.register_blueprint(url, url_prefix='/url')
        app.register_blueprint(search, url_prefix='/')
        
        from .commands import create_user
        app.cli.add_command(create_user)
        
        return app