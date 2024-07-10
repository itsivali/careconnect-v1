#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
from datetime import datetime, timedelta

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Patient, Doctor, Appointment, Bill, Service, BillService, Admin

def create_fake_patients(num_patients):
    patients = []
    for _ in range(num_patients):
        patient = Patient(
            usernaname=fake.user_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
            contact_number=f"+254{fake.msisdn()[4:]}",  # Kenyan format
            email=fake.email()
        )
        patient.password_hash = 'password123'  # Set a default password
        patients.append(patient)
    return patients

def create_fake_doctors(num_doctors):
    specializations = ['Cardiology', 'Neurology', 'Pediatrics', 'Oncology', 'Dermatology']
    doctors = []
    for _ in range(num_doctors):
        doctor = Doctor(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            specialization=rc(specializations)
        )
        doctors.append(doctor)
    return doctors

def create_fake_services(num_services):
    medical_services = [
        'General Checkup', 'Blood Test', 'X-Ray', 'MRI Scan', 'CT Scan',
        'Ultrasound', 'Vaccination', 'Physical Therapy', 'Dental Cleaning',
        'Eye Examination', 'ECG', 'Allergy Test', 'Colonoscopy', 'Mammogram',
        'Dermatology Consultation', 'Nutritional Counseling', 'Psychotherapy Session',
        'Chiropractic Adjustment', 'Acupuncture', 'Physiotherapy'
    ]
    services = []
    for _ in range(num_services):
        service = Service(
            name=fake.random_element(elements=medical_services),
            description=fake.sentence(),
            price=round(fake.pyfloat(min_value=50, max_value=1000), 2)
        )
        services.append(service)
    return services

def create_fake_appointments(patients, doctors):
    appointments = []
    for patient in patients:
        num_appointments = randint(1, 3)
        for _ in range(num_appointments):
            appointment = Appointment(
                patient=patient,
                doctor=rc(doctors),
                appointment_date=fake.future_datetime(end_date='+30d'),
                reason=fake.sentence(),
                status=rc(['Scheduled', 'Completed', 'Cancelled'])
            )
            appointments.append(appointment)
    return appointments

def create_fake_bills(patients, services):
    bills = []
    for patient in patients:
        num_bills = randint(1, 3)
        for _ in range(num_bills):
            bill = Bill(
                patient=patient,
                bill_date=fake.date_time_between(start_date='-30d', end_date='now'),
                amount=0,  # Will be calculated based on services
                status=rc(['Unpaid', 'Paid', 'Partially Paid'])
            )
            db.session.add(bill)
            db.session.commit()  # Commit the bill to get an ID

            used_services = set()
            num_services = randint(1, 5)
            for _ in range(num_services):
                service = rc(services)
                if service.id not in used_services:
                    used_services.add(service.id)
                    bill_service = BillService(
                        bill=bill,
                        service=service,
                        quantity=randint(1, 3)
                    )
                    db.session.add(bill_service)
                    bill.amount += bill_service.service.price * bill_service.quantity

            db.session.commit()
            bills.append(bill)
    return bills

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create admin with default values
        admin = Admin(username='admincareconnect')
        admin.password_hash = 'admincareconnect'
        db.session.add(admin)

        # Create fake data
        patients = create_fake_patients(50)
        doctors = create_fake_doctors(10)
        services = create_fake_services(20)
        
        db.session.add_all(patients + doctors + services)
        db.session.commit()

        appointments = create_fake_appointments(patients, doctors)
        bills = create_fake_bills(patients, services)

        db.session.add_all(appointments + bills)
        db.session.commit()

        print("Seed completed successfully!")