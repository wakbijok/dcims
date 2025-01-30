import pandas as pd
from app import create_app, db
from app.models import Datacenter, Hardware, VirtualMachine, Network, URL

def import_excel_data(filename):
    app = create_app()
    with app.app_context():
        wb = pd.read_excel(filename, sheet_name=None)
        
        # Import Datacenters
        datacenters = {
            'DC': Datacenter(name='DC', location='Primary'),
            'DRC': Datacenter(name='DRC', location='Secondary')
        }
        for dc in datacenters.values():
            db.session.add(dc)
        db.session.commit()

        # Import Hardware
        if 'Hardware Spec' in wb:
            df = wb['Hardware Spec']
            for _, row in df.iterrows():
                hw = Hardware(
                    datacenter_id=datacenters['DC'].id if 'DC' in str(row.get('Location', '')).upper() else datacenters['DRC'].id,
                    equipment=row.get('Equipment'),
                    serial_number=row.get('Serial Number'),
                    function_desc=row.get('Function'),
                    brand_model=row.get('Brand/Model'),
                    ip_address=row.get('IP'),
                    username=row.get('Username'),
                    password=row.get('Password'),
                    ilo_login=row.get('ILO Login')
                )
                db.session.add(hw)

        # Import VMs
        vm_sheets = ['VM DC', 'VM DRC', 'VM Staging DRC']
        for sheet in vm_sheets:
            if sheet in wb:
                df = wb[sheet]
                dc_id = datacenters['DC'].id if 'DC' in sheet else datacenters['DRC'].id
                env = 'Production' if 'Staging' not in sheet else 'Staging'
                
                for _, row in df.iterrows():
                    vm = VirtualMachine(
                        datacenter_id=dc_id,
                        ip_address=row.get('IP Address'),
                        hostname=row.get('Hostname/FQDN'),
                        tech_stack=row.get('Tech Stack'),
                        description=row.get('Description'),
                        environment=env
                    )
                    db.session.add(vm)

        # Import Networks
        if 'Networks' in wb:
            df = wb['Networks']
            for _, row in df.iterrows():
                network = Network(
                    datacenter_id=datacenters['DC'].id,  # Default to DC
                    description=row.get('Description'),
                    network_address=row.get('Network'),
                    gateway=row.get('Gateway'),
                    broadcast=row.get('Broadcast'),
                    vlan_id=row.get('VLAN ID')
                )
                db.session.add(network)

        # Import URLs
        if 'URLs' in wb:
            df = wb['URL & Cred']
            for _, row in df.iterrows():
                url = URL(
                    description=row.get('Description'),
                    url=row.get('URL'),
                    is_public=True if row.get('Is Public?') == 'Yes' else False,
                    environment=row.get('Environment'),
                    ip_address=row.get('Server\'s IP address'),
                    protocol=row.get('Protocol'),
                    port=row.get('Port'),
                    remarks=row.get('Remarks')
                )
                db.session.add(url)

        db.session.commit()

if __name__ == '__main__':
    import_excel_data('NVIS Reinstatement Inventory v1.xlsx')