from flask_sqlalchemy import SQLAlchemy
from datetime import time, date

db = SQLAlchemy()

class Medicine(db.Model):
    __tablename__ = 'medicine'
    trade_name = db.Column(db.String(50), primary_key=True)

class DrugManufacture(db.Model):
    __tablename__ = 'drug_manufacture'
    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

class Patient(db.Model):
    __tablename__ = 'patient'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    sex = db.Column(db.String(1))
    insurance_info = db.Column(db.String(200))
    age = db.Column(db.Integer)

class Doctor(db.Model):
    __tablename__ = 'doctor'
    phys_id = db.Column(db.String(20), primary_key=True)
    d_name = db.Column(db.String(100), nullable=False)
    speciality = db.Column(db.String(100))

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.String(25), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Pharmacy(db.Model):
    __tablename__ = 'pharmacy'
    phar_id = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(100))
    fax = db.Column(db.BigInteger)
    address = db.Column(db.String(200))

class Sell(db.Model):
    __tablename__ = 'sell'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float)
    phar_id = db.Column(db.String(30), db.ForeignKey('pharmacy.phar_id'))
    trade_name = db.Column(db.String(50), db.ForeignKey('medicine.trade_name'))

class Contract(db.Model):
    __tablename__ = 'contract'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    company_id = db.Column(db.Integer, db.ForeignKey('drug_manufacture.company_id'))
    phar_id = db.Column(db.String(30), db.ForeignKey('pharmacy.phar_id'))

class Make(db.Model):
    __tablename__ = 'make'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('drug_manufacture.company_id'))
    trade_name = db.Column(db.String(50), db.ForeignKey('medicine.trade_name'))

class SeenBy(db.Model):
    __tablename__ = 'seen_by'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, db.ForeignKey('patient.pid'))
    phys_id = db.Column(db.String(20), db.ForeignKey('doctor.phys_id'))

class Works(db.Model):
    __tablename__ = 'works'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shift_start = db.Column(db.Time)
    shift_end = db.Column(db.Time)
    employee_id = db.Column(db.String(25), db.ForeignKey('employee.employee_id'))
    phar_id = db.Column(db.String(30), db.ForeignKey('pharmacy.phar_id'))

class Prescribe(db.Model):
    __tablename__ = 'prescribe'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
    phys_id = db.Column(db.String(20), db.ForeignKey('doctor.phys_id'))
    pid = db.Column(db.Integer, db.ForeignKey('patient.pid'))
    trade_name = db.Column(db.String(50), db.ForeignKey('medicine.trade_name'))

class Transporter(db.Model):
    __tablename__ = 'transporter'
    trans_id = db.Column(db.Integer, primary_key=True)
    trans_name = db.Column(db.String(200))
