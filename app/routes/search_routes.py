from flask import Blueprint, request, render_template
from sqlalchemy import or_
from app.models import VirtualMachine
from app.models import Hardware
from app.models import Network
from app.models import URL

search = Blueprint('search', __name__)

@search.route('/search')
def search_inventory():
    query = request.args.get('q', '')
    if not query:
        return render_template('search/results.html', results={})

    results = {
        'vms': VirtualMachine.query.filter(or_(
            VirtualMachine.hostname.ilike(f'%{query}%'),
            VirtualMachine.ip_address.ilike(f'%{query}%'),
            VirtualMachine.tech_stack.ilike(f'%{query}%')
        )).all(),
        
        'hardware': Hardware.query.filter(or_(
            Hardware.equipment.ilike(f'%{query}%'),
            Hardware.ip_address.ilike(f'%{query}%'),
            Hardware.serial_number.ilike(f'%{query}%')
        )).all(),
        
        'networks': Network.query.filter(or_(
            Network.description.ilike(f'%{query}%'),
            Network.network_address.ilike(f'%{query}%'),
            Network.gateway.ilike(f'%{query}%')
        )).all(),
        
        'urls': URL.query.filter(or_(
            URL.url.ilike(f'%{query}%'),
            URL.description.ilike(f'%{query}%'),
            URL.ip_address.ilike(f'%{query}%')
        )).all()
    }
    
    return render_template('search/results.html', results=results, query=query)
