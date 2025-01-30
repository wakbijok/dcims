from flask import render_template, request, redirect, url_for, flash, jsonify
from app.models import Hardware, Datacenter, db
from . import hardware

@hardware.route('/')
def list_hardware():
    hardware_items = Hardware.query.all()
    return render_template('hardware/list.html', hardware_items=hardware_items)

@hardware.route('/add', methods=['GET', 'POST'])
def add_hardware():
    datacenters = Datacenter.query.all()
    if request.method == 'POST':
        try:
            hw = Hardware(
                datacenter_id=request.form.get('datacenter_id'),
                equipment=request.form.get('equipment'),
                serial_number=request.form.get('serial_number') or None,
                function_desc=request.form.get('function_desc'),
                brand_model=request.form.get('brand_model'),
                ip_address=request.form.get('ip_address') or None,
                username=request.form.get('username'),
                password=request.form.get('password'),
                ilo_login=request.form.get('ilo_login')
            )
            db.session.add(hw)
            db.session.commit()
            flash('Hardware added successfully', 'success')
            return redirect(url_for('hardware.list_hardware'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('hardware/add.html', datacenters=datacenters)

@hardware.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_hardware(id):
    hw = Hardware.query.get_or_404(id)
    datacenters = Datacenter.query.all()
    
    if request.method == 'POST':
        try:
            hw.datacenter_id = request.form.get('datacenter_id')
            hw.equipment = request.form.get('equipment')
            hw.serial_number = request.form.get('serial_number') or None
            hw.function_desc = request.form.get('function_desc')
            hw.brand_model = request.form.get('brand_model')
            hw.ip_address = request.form.get('ip_address') or None
            hw.username = request.form.get('username')
            hw.password = request.form.get('password')
            hw.ilo_login = request.form.get('ilo_login')
            
            db.session.commit()
            flash('Hardware updated successfully', 'success')
            return redirect(url_for('hardware.list_hardware'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('hardware/edit.html', hardware=hw, datacenters=datacenters)

@hardware.route('/delete/<int:id>')
def delete_hardware(id):
    hw = Hardware.query.get_or_404(id)
    try:
        db.session.delete(hw)
        db.session.commit()
        flash('Hardware deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('hardware.list_hardware'))

@hardware.route('/check-unique', methods=['POST'])
def check_unique():
    field = request.form.get('field')
    value = request.form.get('value')
    id = request.form.get('id')
    
    query = Hardware.query.filter(getattr(Hardware, field) == value)
    if id:
        query = query.filter(Hardware.id != id)
    
    exists = query.first() is not None
    return jsonify({'exists': exists})