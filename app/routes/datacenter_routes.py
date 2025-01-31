from flask import render_template, request, redirect, url_for, flash
from app.models import Datacenter
from app import db
from . import datacenter

@datacenter.route('/')
def list_datacenters():
    datacenters = Datacenter.query.all()
    return render_template('datacenter/list.html', datacenters=datacenters)

@datacenter.route('/add', methods=['GET', 'POST'])
def add_datacenter():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        
        if name:
            dc = Datacenter(name=name, location=location)
            db.session.add(dc)
            db.session.commit()
            flash('Datacenter added successfully', 'success')
            return redirect(url_for('datacenter.list_datacenters'))
        
    return render_template('datacenter/add.html')

@datacenter.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_datacenter(id):
    dc = Datacenter.query.get_or_404(id)
    
    if request.method == 'POST':
        dc.name = request.form.get('name')
        dc.location = request.form.get('location')
        db.session.commit()
        flash('Datacenter updated successfully', 'success')
        return redirect(url_for('datacenter.list_datacenters'))
        
    return render_template('datacenter/edit.html', datacenter=dc)

@datacenter.route('/delete/<int:id>')
def delete_datacenter(id):
    dc = Datacenter.query.get_or_404(id)
    db.session.delete(dc)
    db.session.commit()
    flash('Datacenter deleted successfully', 'success')
    return redirect(url_for('datacenter.list_datacenters'))
