from flask import render_template, request, redirect, url_for, flash, session
from app import db
from flask_login import login_user, logout_user, login_required
from app.models import Hospital, Doctor, Appointment
from . import bp as  hospital_bp
from .hospital_forms import LoginForm, RegistrationForm

@hospital_bp.route('/')
def index():
    #return render_template('hospital_index.html')
    pass

@hospital_bp.route('/dashboard')
def dashboard():
    hospital = Hospital.query.first()  # Get the logged-in hospital
    doctors = Doctor.query.filter_by(hospital_id=hospital.id).all()
    return render_template('hospital_dashboard.html', doctors=doctors)

@hospital_bp.route('/add_doctor', methods=['POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        hospital_id = request.form['hospital_id']
        
        doctor = Doctor(name=name, specialization=specialization, hospital_id=hospital_id)
        db.session.add(doctor)
        db.session.commit()
        
        flash("Doctor added successfully!", "success")
        return redirect(url_for('hospital.dashboard'))

@hospital_bp.route('/appointments')
def appointments():
    hospital = Hospital.query.first()  # Get the logged-in hospital
    appointments = Appointment.query.filter_by(hospital_id=hospital.id).all()
    return render_template('appointments.html', appointments=appointments)

# AUTHENTICATION ROUTES
@hospital_bp.route('/hospital/login', methods=['POST', 'GET'])
def hospital_login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hospital = Hospital.query.filter_by(email=email).first()
        if hospital and hospital.check_password(password):
            flash("Login successful!", "success")
            #session['hospital_id'] = hospital.id
            login_user(hospital)
            session['database'] = 'hospital' # This is to differentiate between hospital and patient sessions for the user_loader callback.
            return redirect(url_for('hospital.dashboard'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for('hospital.hospital_login'))
    return render_template('hospital_login.html', form=form)

@hospital_bp.route('/hospital/logout')
def hospital_logout():
    logout_user()
    session.pop('database', None)
    return redirect(url_for('hospital.hospital_login'))

@hospital_bp.route('/hospital/register', methods=['POST', 'GET'])
def hospital_register():
    form = RegistrationForm()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hospital = Hospital(name=name, email=email)
        hospital.set_password(password)
        db.session.add(hospital)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for('hospital.hospital_login'))
    return render_template('hospital_register.html', form=form)

# DOCTOR MANAGEMENT ROUTES
@hospital_bp.route('/hospital/<hospital_id:int>/doctors')
def hospital_doctors(hospital_id):
    '''add a doctor to a hospital -> [post]. View all doctors in a hospital -> [get]'''
    hospital = Hospital.query.get(hospital_id)
    doctors = Doctor.query.filter_by(hospital_id=hospital.id).all()
    #return render_template('hospital_doctors.html', doctors=doctors)
    pass

@hospital_bp.route('/hospital/<hospital_id:int>/doctor/<doctor_id:int>')
def hospital_doctor(hospital_id, doctor_id):
    '''view a single doctor in a hospital'''
    doctor = Doctor.query.get(doctor_id)
    #return render_template('hospital_doctor.html', doctor=doctor)
    pass

@hospital_bp.route('/hospital/<hospital_id:int>/doctor/<doctor_id:int>/edit', methods=['POST'])
def hospital_doctor_edit(hospital_id, doctor_id):
    '''edit a doctor in a hospital'''
    doctor = Doctor.query.get(doctor_id)
    doctor.name = request.form['name']
    doctor.specialization = request.form['specialization']
    db.session.commit()
    flash("Doctor updated successfully!", "success")
    #return redirect(url_for('hospital.hospital_doctor', hospital_id=hospital_id, doctor_id=doctor_id))
    pass

@hospital_bp.route('/hospital/<hospital_id:int>/doctor/<doctor_id:int>/delete', methods=['POST'])
def hospital_doctor_delete(hospital_id, doctor_id):
    '''delete a doctor from a hospital'''
    doctor = Doctor.query.get(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash("Doctor deleted successfully!", "success")
    #return redirect(url_for('hospital.hospital_doctors', hospital_id=hospital_id))
    pass

# APPOINTMENT MANAGEMENT ROUTES
@hospital_bp.route('/hospital/<hospital_id:int>/appointments')
def hospital_appointments(hospital_id):
    '''view all appointments in a hospital'''
    hospital = Hospital.query.get(hospital_id)
    appointments = hospital.appointments   # This is possible because of the backref in the Appointment model.
    # appointments = Appointment.query.filter_by(hospital_id=hospital.id).all()
    #return render_template('hospital_appointments.html', appointments=appointments)
    pass

@hospital_bp.route('/hospital/<hospital_id:int>/appointment/<appointment_id:int>')
def hospital_appointment(hospital_id, appointment_id):
    '''view a single appointment in a hospital'''
    appointment = Appointment.query.get(appointment_id)
    #return render_template('hospital_appointment.html', appointment=appointment)
    pass

@hospital_bp.route('/hospital/<hospital_id:int>/appointment/<appointment_id:int>/edit', methods=['POST'])
def hospital_appointment_edit(hospital_id, appointment_id):
    '''edit an appointment in a hospital'''
    appointment = Appointment.query.get(appointment_id)
    appointment.date = request.form['date']
    db.session.commit()
    flash("Appointment updated successfully!", "success")
    #return redirect(url_for('hospital.hospital_appointment', hospital_id=hospital_id, appointment_id=appointment_id))
    pass

@hospital_bp.route('/hospital/<hospital_id:int>/appointment/<appointment_id:int>/delete', methods=['POST'])
def hospital_appointment_delete(hospital_id, appointment_id):
    '''delete an appointment from a hospital'''
    appointment = Appointment.query.get(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash("Appointment deleted successfully!", "success")
    #return redirect(url_for('hospital.hospital_appointments', hospital_id=hospital_id))
    pass

@hospital_bp.route('/hospital/<hospital_id:int>/appointment/add', methods=['POST'])
def hospital_appointment_add(hospital_id):
    '''add an appointment to a hospital'''
    date = request.form['date']
    status = request.form['status']
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    appointment = Appointment(date=date, status=status, patient_id=patient_id, doctor_id=doctor_id, hospital_id=hospital_id)
    db.session.add(appointment)
    db.session.commit()
    flash("Appointment added successfully!", "success")
    #return redirect(url_for('hospital.hospital_appointments', hospital_id=hospital_id))
    pass

# ANALYTICS ROUTES
@hospital_bp.route('/hospital/<hospital_id:int>/analytics')
def hospital_analytics(hospital_id):
    '''view analytics for a hospital'''
    hospital = Hospital.query.get(hospital_id)  # what if analytics are instead taken to the dashboard?
    #return render_template('hospital_analytics.html', hospital=hospital)
    pass

# BILLING ROUTES

# VIDEO CONSULTATION ROUTES