from flask import Blueprint, render_template
from app.models import VirtualMachine, Hardware, Network, URL

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    stats = {
        'vm_count': VirtualMachine.query.count(),
        'hardware_count': Hardware.query.count(),
        'network_count': Network.query.count(),
        'url_count': URL.query.count(),
        'recent_vms': VirtualMachine.query.order_by(VirtualMachine.id.desc()).limit(5).all(),
        'recent_hardware': Hardware.query.order_by(Hardware.id.desc()).limit(5).all()
    }
    return render_template('dashboard.html', **stats)