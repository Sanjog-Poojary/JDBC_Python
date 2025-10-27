from app import create_app
from models import db, Medicine, DrugManufacture, Patient, Doctor, Employee, Pharmacy, Sell, Contract, Make, SeenBy, Works, Prescribe, Transporter
from datetime import date, time

app = create_app()

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Manufacturers
        manufacturers = [
            DrugManufacture(company_id=1, name='Cipla Ltd', address='Cipla House, Peninsula Business Park, Mumbai'),
            DrugManufacture(company_id=2, name='Sun Pharma', address='Sun House, Western Express Highway, Mumbai'),
            DrugManufacture(company_id=3, name="Dr. Reddy's Labs", address='8-2-337, Road No. 3, Banjara Hills, Hyderabad'),
            DrugManufacture(company_id=4, name='Lupin Limited', address='Kalpataru Inspire, Off Western Express Highway, Mumbai'),
            DrugManufacture(company_id=5, name='Zydus Cadila', address='Sarkhej-Dholka Road, Bhat, Ahmedabad'),
        ]
        db.session.add_all(manufacturers)

        # Medicines
        medicines = ['Paracetamol','Amoxicillin','Ibuprofen','Aspirin','Atorvastatin','Metformin','Omeprazole']
        for m in medicines:
            db.session.add(Medicine(trade_name=m))

        # MAKE
        makes = [(1,'Paracetamol'),(1,'Amoxicillin'),(2,'Ibuprofen'),(3,'Aspirin'),(4,'Atorvastatin'),(5,'Metformin'),(5,'Omeprazole')]
        for c,t in makes:
            db.session.add(Make(company_id=c, trade_name=t))

        # Patients
        patients = [
            Patient(pid=201, name='Rohan Sharma', address='15 FC Road, Pune', sex='M', insurance_info='Star Health Gold', age=35),
            Patient(pid=202, name='Priya Singh', address='21 MG Road, Bangalore', sex='F', insurance_info='HDFC Ergo Optima', age=28),
            Patient(pid=203, name='Amit Patel', address='10 C.G. Road, Ahmedabad', sex='M', insurance_info='ICICI Lombard Complete', age=45),
            Patient(pid=204, name='Sneha Reddy', address='5 Jubilee Hills, Hyderabad', sex='F', insurance_info='Bajaj Allianz Silver', age=32),
            Patient(pid=205, name='Vikram Kumar', address='8 Marine Drive, Mumbai', sex='M', insurance_info='Max Bupa Health Companion', age=50),
        ]
        db.session.add_all(patients)

        # Doctors
        doctors = [
            Doctor(phys_id='DOC101', d_name='Dr. Anjali Rao', speciality='Cardiologist'),
            Doctor(phys_id='DOC102', d_name='Dr. Sameer Verma', speciality='Pediatrician'),
            Doctor(phys_id='DOC103', d_name='Dr. Neha Desai', speciality='Dermatologist'),
            Doctor(phys_id='DOC104', d_name='Dr. Rajesh Gupta', speciality='Orthopedic'),
            Doctor(phys_id='DOC105', d_name='Dr. Meera Iyer', speciality='General Physician'),
        ]
        db.session.add_all(doctors)

        # Employees
        employees = [
            Employee(employee_id='EMP201', name='Ankit Joshi'),
            Employee(employee_id='EMP202', name='Bhavna Mehta'),
            Employee(employee_id='EMP203', name='Chetan Shah'),
            Employee(employee_id='EMP204', name='Divya Nair'),
            Employee(employee_id='EMP205', name='Farhan Khan'),
        ]
        db.session.add_all(employees)

        # Pharmacies
        pharmacies = [
            Pharmacy(phar_id='PHARM01', name='Apollo Pharmacy', fax=2026543210, address='J.M. Road, Pune'),
            Pharmacy(phar_id='PHARM02', name='Wellness Forever', fax=2229876543, address='Bandra West, Mumbai'),
            Pharmacy(phar_id='PHARM03', name='MedPlus', fax=4023456789, address='Hitech City, Hyderabad'),
            Pharmacy(phar_id='PHARM04', name='Noble Medicals', fax=2025551234, address='Koregaon Park, Pune'),
            Pharmacy(phar_id='PHARM05', name='Frank Ross', fax=3322114455, address='Park Street, Kolkata'),
        ]
        db.session.add_all(pharmacies)

        # Sell
        sells = [
            Sell(price=15.50, phar_id='PHARM01', trade_name='Paracetamol'),
            Sell(price=25.00, phar_id='PHARM01', trade_name='Ibuprofen'),
            Sell(price=8.75, phar_id='PHARM02', trade_name='Aspirin'),
            Sell(price=55.20, phar_id='PHARM03', trade_name='Atorvastatin'),
            Sell(price=12.00, phar_id='PHARM05', trade_name='Omeprazole'),
        ]
        db.session.add_all(sells)

        # Contracts
        contracts = [
            Contract(start_date=date(2023,1,1), end_date=date(2025,12,31), company_id=1, phar_id='PHARM01'),
            Contract(start_date=date(2022,6,1), end_date=date(2024,5,31), company_id=2, phar_id='PHARM02'),
            Contract(start_date=date(2023,3,15), end_date=date(2025,3,14), company_id=3, phar_id='PHARM03'),
            Contract(start_date=date(2024,1,1), end_date=date(2026,12,31), company_id=5, phar_id='PHARM01'),
            Contract(start_date=date(2023,7,1), end_date=date(2025,6,30), company_id=4, phar_id='PHARM04'),
        ]
        db.session.add_all(contracts)

        # Seen_by
        sb = [
            SeenBy(pid=101, phys_id='DOC105'),
            SeenBy(pid=201, phys_id='DOC101'),
            SeenBy(pid=202, phys_id='DOC103'),
            SeenBy(pid=203, phys_id='DOC104'),
            SeenBy(pid=204, phys_id='DOC105'),
        ]
        db.session.add_all(sb)

        # Works
        work_rows = [
            Works(shift_start=time(8,0), shift_end=time(16,0), employee_id='EMP201', phar_id='PHARM01'),
            Works(shift_start=time(14,0), shift_end=time(22,0), employee_id='EMP202', phar_id='PHARM01'),
            Works(shift_start=time(9,0), shift_end=time(17,0), employee_id='EMP203', phar_id='PHARM02'),
            Works(shift_start=time(10,0), shift_end=time(18,0), employee_id='EMP204', phar_id='PHARM03'),
            Works(shift_start=time(8,30), shift_end=time(16,30), employee_id='EMP205', phar_id='PHARM04'),
        ]
        db.session.add_all(work_rows)

        # Prescriptions
        prescriptions = [
            Prescribe(date=date(2024,10,15), quantity=30, phys_id='DOC101', pid=201, trade_name='Atorvastatin'),
            Prescribe(date=date(2024,10,16), quantity=1, phys_id='DOC103', pid=202, trade_name='Omeprazole'),
            Prescribe(date=date(2024,10,17), quantity=1, phys_id='DOC105', pid=101, trade_name='Paracetamol'),
            Prescribe(date=date(2024,10,18), quantity=60, phys_id='DOC104', pid=203, trade_name='Ibuprofen'),
            Prescribe(date=date(2024,10,19), quantity=14, phys_id='DOC105', pid=204, trade_name='Amoxicillin'),
        ]
        db.session.add_all(prescriptions)

        # Transporters
        trans = [
            Transporter(trans_id=1, trans_name='Delhivery Pharma'),
            Transporter(trans_id=2, trans_name='Blue Dart Medical'),
            Transporter(trans_id=3, trans_name='QuickRun Logistics'),
            Transporter(trans_id=4, trans_name='SafeTrans Health'),
            Transporter(trans_id=5, trans_name='India Post Pharma'),
        ]
        db.session.add_all(trans)

        db.session.commit()
        print('Database seeded to drugstore.db')

if __name__ == '__main__':
    seed()
