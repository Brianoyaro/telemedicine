from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Patient, Appointment, Doctor
from . import bp as patient_bp


@patient_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']  # Ensure password is hashed

        patient = Patient(name=name, email=email, phone=phone, password=password)
        db.session.add(patient)
        db.session.commit()

        flash("Patient registered successfully!", "success")
        return redirect(url_for('patient.login'))

    return render_template('patient_register.html')

@patient_bp.route('/book_appointment', methods=['POST'])
def book_appointment():
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    appointment_date = request.form['date']
    
    appointment = Appointment(date=appointment_date, status="Pending", patient_id=patient_id, doctor_id=doctor_id)
    db.session.add(appointment)
    db.session.commit()

    flash("Appointment booked successfully!", "success")
    return redirect(url_for('patient.dashboard'))
