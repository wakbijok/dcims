from flask import Blueprint

auth = Blueprint('auth', __name__)
datacenter = Blueprint('datacenter', __name__)
hardware = Blueprint('hardware', __name__)
vm = Blueprint('vm', __name__)
network = Blueprint('network', __name__)
url = Blueprint('url', __name__)
search = Blueprint('search', __name__)
dashboard = Blueprint('dashboard', __name__)

from .datacenter_routes import *
from .hardware_routes import *
from .vm_routes import *
from .network_routes import *
from .url_routes import *
from .search_routes import *
from .dashboard_routes import *
from .auth_routes import *
