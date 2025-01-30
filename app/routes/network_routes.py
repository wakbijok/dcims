from flask import render_template, request, redirect, url_for, flash
from app.models import Network, Datacenter, db
from . import network

@network.route('/')
def list_networks():
    networks = Network.query.all()
    return render_template('network/list.html', networks=networks)

@network.route('/add', methods=['GET', 'POST'])
def add_network():
    datacenters = Datacenter.query.all()
    if request.method == 'POST':
        try:
            network_instance = Network(
                datacenter_id=request.form.get('datacenter_id'),
                description=request.form.get('description'),
                network_address=request.form.get('network_address'),
                gateway=request.form.get('gateway'),
                broadcast=request.form.get('broadcast'),
                vlan_id=request.form.get('vlan_id')
            )
            db.session.add(network_instance)
            db.session.commit()
            flash('Network added successfully', 'success')
            return redirect(url_for('network.list_networks'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('network/add.html', datacenters=datacenters)

@network.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_network(id):
    network_instance = Network.query.get_or_404(id)
    datacenters = Datacenter.query.all()
    
    if request.method == 'POST':
        try:
            network_instance.datacenter_id = request.form.get('datacenter_id')
            network_instance.description = request.form.get('description')
            network_instance.network_address = request.form.get('network_address')
            network_instance.gateway = request.form.get('gateway')
            network_instance.broadcast = request.form.get('broadcast')
            network_instance.vlan_id = request.form.get('vlan_id')
            
            db.session.commit()
            flash('Network updated successfully', 'success')
            return redirect(url_for('network.list_networks'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('network/edit.html', network=network_instance, datacenters=datacenters)

@network.route('/delete/<int:id>')
def delete_network(id):
    network_instance = Network.query.get_or_404(id)
    try:
        db.session.delete(network_instance)
        db.session.commit()
        flash('Network deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('network.list_networks'))