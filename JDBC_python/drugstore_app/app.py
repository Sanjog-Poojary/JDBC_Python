from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Medicine, DrugManufacture, Patient, Doctor, Prescribe, Sell, Make, SeenBy
from sqlalchemy import text
import csv
import io
from flask import Response
from datetime import date
import os

def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    # Use an absolute path for the SQLite DB so the app and seed script always reference the same file
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # prefer the instance/ DB (seed script created instance/drugstore.db); fallback to drugstore.db
    instance_db = os.path.join(base_dir, 'instance', 'drugstore.db')
    db_path = instance_db if os.path.exists(instance_db) else os.path.join(base_dir, 'drugstore.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/')
    def index():
        medicines = Medicine.query.limit(10).all()
        counts = {
            'medicines': Medicine.query.count(),
            'manufacturers': DrugManufacture.query.count(),
            'patients': Patient.query.count()
        }
        return render_template('index.html', medicines=medicines, counts=counts)

    @app.route('/medicines')
    def medicines():
        q = request.args.get('q')
        if q:
            items = Medicine.query.filter(Medicine.trade_name.ilike(f"%{q}%")).all()
        else:
            items = Medicine.query.order_by(Medicine.trade_name).all()
        return render_template('medicines.html', medicines=items, q=q)

    @app.route('/medicines/edit/<trade_name>', methods=['GET','POST'])
    def edit_medicine(trade_name):
        med = Medicine.query.get_or_404(trade_name)
        if request.method == 'POST':
            new_name = request.form.get('trade_name')
            if not new_name:
                flash('Name required', 'danger')
                return redirect(url_for('edit_medicine', trade_name=trade_name))

            # check for dependent references
            deps = Sell.query.filter_by(trade_name=trade_name).count() + Make.query.filter_by(trade_name=trade_name).count() + Prescribe.query.filter_by(trade_name=trade_name).count()
            if deps > 0 and new_name != trade_name:
                flash('Cannot rename medicine with existing references (sell/make/prescribe). Delete references first.', 'warning')
                return redirect(url_for('medicines'))

            if new_name != trade_name:
                # simple rename when safe
                med.trade_name = new_name
                db.session.commit()
                flash('Medicine renamed', 'success')
            else:
                flash('No changes made', 'info')
            return redirect(url_for('medicines'))
        return render_template('edit_medicine.html', med=med)

    @app.route('/medicines/delete/<trade_name>', methods=['POST'])
    def delete_medicine(trade_name):
        med = Medicine.query.get_or_404(trade_name)
        deps = Sell.query.filter_by(trade_name=trade_name).count() + Make.query.filter_by(trade_name=trade_name).count() + Prescribe.query.filter_by(trade_name=trade_name).count()
        if deps > 0:
            flash('Cannot delete medicine with existing references (sell/make/prescribe). Remove references first.', 'warning')
            return redirect(url_for('medicines'))
        db.session.delete(med)
        db.session.commit()
        flash('Medicine deleted', 'success')
        return redirect(url_for('medicines'))

    @app.route('/manufacturers')
    def manufacturers():
        items = DrugManufacture.query.order_by(DrugManufacture.name).all()
        return render_template('manufacturers.html', manufacturers=items)

    @app.route('/patients')
    def patients():
        items = Patient.query.order_by(Patient.name).all()
        return render_template('patients.html', patients=items)

    @app.route('/patients/add', methods=['GET','POST'])
    def add_patient():
        if request.method == 'POST':
            pid = request.form.get('pid')
            name = request.form.get('name')
            address = request.form.get('address')
            sex = request.form.get('sex')
            insurance = request.form.get('insurance')
            age = request.form.get('age')
            p = Patient(pid=int(pid), name=name, address=address, sex=sex, insurance_info=insurance, age=int(age) if age else None)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('patients'))
        return render_template('add_patient.html')

    @app.route('/patients/edit/<int:pid>', methods=['GET','POST'])
    def edit_patient(pid):
        p = Patient.query.get_or_404(pid)
        if request.method == 'POST':
            p.name = request.form.get('name')
            p.address = request.form.get('address')
            p.sex = request.form.get('sex')
            p.insurance_info = request.form.get('insurance')
            age = request.form.get('age')
            p.age = int(age) if age else None
            db.session.commit()
            flash('Patient updated', 'success')
            return redirect(url_for('patients'))
        return render_template('edit_patient.html', p=p)

    @app.route('/patients/delete/<int:pid>', methods=['POST'])
    def delete_patient(pid):
        p = Patient.query.get_or_404(pid)
        # delete dependent records first
        Prescribe.query.filter_by(pid=pid).delete()
        SeenBy.query.filter_by(pid=pid).delete()
        db.session.delete(p)
        db.session.commit()
        flash('Patient and related records deleted', 'success')
        return redirect(url_for('patients'))

    @app.route('/prescriptions')
    def prescriptions():
        items = Prescribe.query.order_by(Prescribe.date.desc()).all()
        return render_template('prescriptions.html', prescriptions=items)

    @app.route('/query', methods=['GET','POST'])
    def query():
        results = None
        columns = []
        error = None
        q = ''
        if request.method == 'POST':
            q = request.form.get('sql') or ''
            q_stripped = q.strip()
            # Basic safety: allow only single SELECT statements
            if not q_stripped.lower().startswith('select'):
                error = 'Only SELECT queries are allowed.'
            elif ';' in q_stripped and q_stripped.count(';') > 1:
                error = 'Only a single SELECT statement is allowed.'
            else:
                try:
                    # limit rows to 200
                    stmt = text(q_stripped + ' LIMIT 200') if 'limit' not in q_stripped.lower() else text(q_stripped)
                    # Use session.execute which works with SQLAlchemy 2.x (avoids Engine.execute)
                    res = db.session.execute(stmt)
                    rows = res.fetchall()
                    columns = res.keys()
                    results = rows
                except Exception as e:
                    error = str(e)
        return render_template('query.html', results=results, columns=columns, error=error, q=q)

    @app.route('/query/download', methods=['POST'])
    def query_download():
        # Accept SQL from the form, validate same as query route, execute and stream CSV
        q = request.form.get('sql') or ''
        q_stripped = q.strip()
        if not q_stripped.lower().startswith('select'):
            return 'Only SELECT queries are allowed', 400
        try:
            stmt = text(q_stripped) if 'limit' in q_stripped.lower() else text(q_stripped + ' LIMIT 10000')
            res = db.session.execute(stmt)
            rows = res.fetchall()
            columns = res.keys()

            si = io.StringIO()
            writer = csv.writer(si)
            writer.writerow(columns)
            for r in rows:
                writer.writerow([str(x) if x is not None else '' for x in r])
            output = si.getvalue()
            return Response(output, mimetype='text/csv', headers={
                'Content-Disposition': 'attachment; filename="query_results.csv"'
            })
        except Exception as e:
            return str(e), 500

    @app.route('/prescriptions/add', methods=['GET','POST'])
    def add_prescription():
        if request.method == 'POST':
            date_s = request.form.get('date')
            quantity = int(request.form.get('quantity'))
            phys_id = request.form.get('phys_id')
            pid = int(request.form.get('pid'))
            trade_name = request.form.get('trade_name')
            pr = Prescribe(date=date.fromisoformat(date_s), quantity=quantity, phys_id=phys_id, pid=pid, trade_name=trade_name)
            db.session.add(pr)
            db.session.commit()
            return redirect(url_for('prescriptions'))
        meds = Medicine.query.order_by(Medicine.trade_name).all()
        docs = Doctor.query.order_by(Doctor.d_name).all()
        pats = Patient.query.order_by(Patient.name).all()
        return render_template('add_prescription.html', meds=meds, docs=docs, pats=pats)

    return app

if __name__ == '__main__':
    app = create_app()
    # Run without the debug reloader so the process stays in a single foreground process
    app.run(host='127.0.0.1', port=5000, debug=False)
