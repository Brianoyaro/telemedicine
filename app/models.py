from app import db, login
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Hospital(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # You should hash this before storing.
    #location = db.Column(db.String(200), nullable=False)
    #plan_type = db.Column(db.String(20), default="free")  # 'free' or 'premium' Take this to billing class to abstract billing logic.
    doctors = db.relationship('Doctor', backref='hospital', lazy=True)
    appointments = db.relationship('Appointment', backref='hospital', lazy=True)

    def __repr__(self):
        """officialrepresentation of a user object"""
        return "<Name: {}>, <Email: {}>, <Location: {}>".format(self.name, self.email, self.location)

    def set_password(self, password):
        """sets a users password as a hashed attribute"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """validates a user's password incase they want to login"""
        return check_password_hash(self.password_hash, password)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    availability = db.Column(db.String(500), nullable=True)  # Store availability as a string for simplicity.

class Patient(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # phone = db.Column(db.String(15), nullable=False) What if we request the phone number when booking an appointment?
    password = db.Column(db.String(100), nullable=False)  # You should hash this before storing.
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def __repr__(self):
        """officialrepresentation of a PAtient object"""
        return "<Name: {}>, <Email:{}>, <Contact:{}>".format(self.name, self.email, self.phone)

    def set_password(self, password):
        """sets a users password as a hashed attribute"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """validates a user's password incase they want to login"""
        return check_password_hash(self.password_hash, password)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # e.g., 'Pending', 'Completed'
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

@login.user_loader
def load_user(id):
    '''dynamically load the user based on the database in use because they will have different ield in the database'''
    database = session.get('database')
    if database == 'hospital':
        return Hospital.query.get(int(id))
    return Patient.query.get(int(id))