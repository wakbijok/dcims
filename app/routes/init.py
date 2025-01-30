from flask import Blueprint

auth = Blueprint('auth', __name__)
dashboard = Blueprint('dashboard', __name__)
datacenter = Blueprint('datacenter', __name__)
hardware = Blueprint('hardware', __name__)
vm = Blueprint('vm', __name__)
network = Blueprint('network', __name__)
url = Blueprint('url', __name__)
search = Blueprint('search', __name__)

from . import auth_routes, dashboard_routes, datacenter_routes, hardware_routes, vm_routes, network_routes, url_routes, search_routes