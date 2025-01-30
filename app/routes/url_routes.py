from flask import render_template, request, redirect, url_for, flash
from app.models import URL, VirtualMachine, db
from . import url

@url.route('/')
def list_urls():
    urls = URL.query.all()
    return render_template('url/list.html', urls=urls)

@url.route('/add', methods=['GET', 'POST'])
def add_url():
    vms = VirtualMachine.query.all()
    if request.method == 'POST':
        try:
            url_instance = URL(
                description=request.form.get('description'),
                url=request.form.get('url'),
                is_public=bool(request.form.get('is_public')),
                environment=request.form.get('environment'),
                ip_address=request.form.get('ip_address'),
                protocol=request.form.get('protocol'),
                port=request.form.get('port'),
                remarks=request.form.get('remarks')
            )
            db.session.add(url_instance)
            db.session.commit()
            flash('URL added successfully', 'success')
            return redirect(url_for('url.list_urls'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('url/add.html', vms=vms)

@url.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_url(id):
    url_instance = URL.query.get_or_404(id)
    vms = VirtualMachine.query.all()
    
    if request.method == 'POST':
        try:
            url_instance.description = request.form.get('description')
            url_instance.url = request.form.get('url')
            url_instance.is_public = bool(request.form.get('is_public'))
            url_instance.environment = request.form.get('environment')
            url_instance.ip_address = request.form.get('ip_address')
            url_instance.protocol = request.form.get('protocol')
            url_instance.port = request.form.get('port')
            url_instance.remarks = request.form.get('remarks')
            
            db.session.commit()
            flash('URL updated successfully', 'success')
            return redirect(url_for('url.list_urls'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('url/edit.html', url=url_instance, vms=vms)

@url.route('/delete/<int:id>')
def delete_url(id):
    url_instance = URL.query.get_or_404(id)
    try:
        db.session.delete(url_instance)
        db.session.commit()
        flash('URL deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('url.list_urls'))