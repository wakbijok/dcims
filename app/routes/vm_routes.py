from flask import render_template, request, redirect, url_for, flash, jsonify
from app.models import VirtualMachine, Datacenter, db
from . import vm

@vm.route('/')
def list_vms():
    vms = VirtualMachine.query.all()
    return render_template('vm/list.html', vms=vms)

@vm.route('/add', methods=['GET', 'POST'])
def add_vm():
    datacenters = Datacenter.query.all()
    if request.method == 'POST':
        try:
            vm_instance = VirtualMachine(
                datacenter_id=request.form.get('datacenter_id'),
                ip_address=request.form.get('ip_address') or None,
                hostname=request.form.get('hostname'),
                tech_stack=request.form.get('tech_stack'),
                description=request.form.get('description'),
                environment=request.form.get('environment')
            )
            db.session.add(vm_instance)
            db.session.commit()
            flash('Virtual Machine added successfully', 'success')
            return redirect(url_for('vm.list_vms'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('vm/add.html', datacenters=datacenters)

@vm.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_vm(id):
    vm_instance = VirtualMachine.query.get_or_404(id)
    datacenters = Datacenter.query.all()
    
    if request.method == 'POST':
        try:
            vm_instance.datacenter_id = request.form.get('datacenter_id')
            vm_instance.ip_address = request.form.get('ip_address') or None
            vm_instance.hostname = request.form.get('hostname')
            vm_instance.tech_stack = request.form.get('tech_stack')
            vm_instance.description = request.form.get('description')
            vm_instance.environment = request.form.get('environment')
            
            db.session.commit()
            flash('Virtual Machine updated successfully', 'success')
            return redirect(url_for('vm.list_vms'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('vm/edit.html', vm=vm_instance, datacenters=datacenters)

@vm.route('/delete/<int:id>')
def delete_vm(id):
    vm_instance = VirtualMachine.query.get_or_404(id)
    try:
        db.session.delete(vm_instance)
        db.session.commit()
        flash('Virtual Machine deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('vm.list_vms'))

@vm.route('/check-ip', methods=['POST'])
def check_ip():
    ip_address = request.form.get('ip_address')
    vm_id = request.form.get('id')
    
    query = VirtualMachine.query.filter_by(ip_address=ip_address)
    if vm_id:
        query = query.filter(VirtualMachine.id != vm_id)
    
    exists = query.first() is not None
    return jsonify({'exists': exists})