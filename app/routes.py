from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Case, Watcher, Sighting

main = Blueprint('main', __name__)

@main.route('/')
def index():
    cases = Case.query.filter_by(status='active').order_by(Case.created_at.desc()).all()
    return render_template('index.html', cases=cases)

@main.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        case = Case(
            category=request.form.get('category'),
            name=request.form.get('name'),
            age=request.form.get('age'),
            last_location=request.form.get('last_location'),
            clothing=request.form.get('clothing'),
            medical=request.form.get('medical'),
            police_case=request.form.get('police_case'),
            vehicle=request.form.get('vehicle'),
            reporter_name=request.form.get('reporter_name'),
            reporter_phone=request.form.get('reporter_phone'),
            status='pending'
        )
        db.session.add(case)
        db.session.commit()
        flash('Report submitted. Our team will verify and activate the alert shortly.')
        return redirect(url_for('main.index'))
    return render_template('report.html')

@main.route('/watch', methods=['GET', 'POST'])
def watch():
    if request.method == 'POST':
        watcher = Watcher(
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            role=request.form.get('role'),
            area=request.form.get('area')
        )
        db.session.add(watcher)
        db.session.commit()
        flash('Welcome to the Ubuntu Watcher network!')
        return redirect(url_for('main.index'))
    return render_template('watch.html')

@main.route('/admin')
def admin():
    pending = Case.query.filter_by(status='pending').all()
    active = Case.query.filter_by(status='active').all()
    resolved = Case.query.filter(Case.status.in_(['found','deceased','investigation'])).all()
    watchers = Watcher.query.order_by(Watcher.registered_at.desc()).all()
    return render_template('admin.html', pending=pending, active=active, resolved=resolved, watchers=watchers)

@main.route('/admin/activate/<int:case_id>')
def activate(case_id):
    case = Case.query.get_or_404(case_id)
    case.status = 'active'
    db.session.commit()
    flash(f'Alert activated for {case.name}.')
    return redirect(url_for('main.admin'))

@main.route('/admin/resolve/<int:case_id>/<resolution>')
def resolve(case_id, resolution):
    case = Case.query.get_or_404(case_id)
    case.status = resolution
    db.session.commit()
    flash(f'Case for {case.name} marked as {resolution}.')
    return redirect(url_for('main.admin'))