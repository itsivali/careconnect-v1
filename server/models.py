from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
import re

from config import db, bcrypt

class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'

    serialize_rules = ('-appointments.patient', '-bills.patient')

    id = db.Column(db.Integer, primary_key=True)
    usernaname = db.Column(db.String(50), nullable=False)
    _password_hash = db.Column(db.String)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(120))
    
    appointments = db.relationship('Appointment', back_populates='patient')
    bills = db.relationship('Bill', back_populates='patient')

    doctors = association_proxy('appointments', 'doctor')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty")
        return value.strip()

    @validates('email')
    def validate_email(self, key, value):
        if value:
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, value):
                raise ValueError("Invalid email format")
        return value

    @validates('contact_number')
    def validate_contact_number(self, key, value):
        if value:
            pattern = r'^(?:0|\+254|254)([0-9]{9})$'
            if not re.match(pattern, value):
                raise ValueError("Invalid contact number format")
        return value

    def __repr__(self):
        return f"<Patient {self.id}: {self.first_name} {self.last_name}>"

class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'

    serialize_rules = ('-patients',)

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(100))
    
    appointments = db.relationship('Appointment', back_populates='doctor')

    patients = association_proxy('appointments', 'patient')

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty")
        return value.strip()

    def __repr__(self):
        return f"<Doctor {self.id}: Dr. {self.last_name}, {self.specialization}>"

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    serialize_rules = ('-patient', '-doctor')
    serialize_only = ('id', 'patient_id', 'doctor_id', 'appointment_date', 'reason', 'status')

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Scheduled')
    
    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')

    @validates('appointment_date')
    def validate_appointment_date(self, key, value):
        if value <= datetime.now():
            raise ValueError("Appointment date must be in the future")
        return value

    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['Scheduled', 'Completed', 'Cancelled']
        if value not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return value

    def __repr__(self):
        return f"<Appointment {self.id}: Patient {self.patient_id} with Doctor {self.doctor_id} on {self.appointment_date}>"

class Bill(db.Model, SerializerMixin):
    __tablename__ = 'bills'

    serialize_rules = ('-patient.bills', '-bill_services', '-patient.appointments')

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    bill_date = db.Column(db.DateTime )
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Unpaid')
    
    patient = db.relationship('Patient', back_populates='bills')
    bill_services = db.relationship('BillService', back_populates='bill', cascade='all, delete-orphan')
    
    services = association_proxy('bill_services', 'service')

    

    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['Unpaid', 'Paid', 'Partially Paid']
        if value not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return value

    def __repr__(self):
        return f"<Bill {self.id}: Patient {self.patient_id}, Amount ${self.amount}, Status: {self.status}>"

class Service(db.Model, SerializerMixin):
    __tablename__ = 'services'

    serialize_rules = ('-bill_services.service',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    
    bill_services = db.relationship('BillService', back_populates='service')
    
    bills = association_proxy('bill_services', 'bill')

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Service name cannot be empty")
        return value.strip()

    @validates('price')
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

    def __repr__(self):
        return f"<Service {self.id}: {self.name}, Price: ${self.price}>"

class BillService(db.Model, SerializerMixin):
    __tablename__ = 'bill_services'

    serialize_rules = ('-bill.bill_services', '-service.bill_services', '-bill.patient.appointments')

    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    notes = db.Column(db.String(200))  
    
    bill = db.relationship('Bill', back_populates='bill_services')
    service = db.relationship('Service', back_populates='bill_services')

    @validates('quantity')
    def validate_quantity(self, key, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than 0")
        return value

    def __repr__(self):
        return f"<BillService: Bill {self.bill_id}, Service {self.service_id}, Quantity: {self.quantity}>"
    

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, default='admincareconnect')
    _password_hash = db.Column(db.String, default='admincareconnect')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f"<Admin {self.id}: {self.username}>"
