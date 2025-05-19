from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.appointment import Appointment
from models.doctor import Doctor
from datetime import datetime

appointment_bp = Blueprint('appointment_bp', __name__)

@appointment_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_appointment():
    if current_user.role != 'patient':
        flash("Only patients can create appointments.", "error")
        return redirect(url_for('home'))

    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        appt_time_str = request.form.get('appointment_time')
        try:
            appt_time = datetime.strptime(appt_time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            flash("Incorrect date/time format.", "error")
            return redirect(url_for('appointment_bp.create_appointment'))

        new_appt = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor_id,
            appointment_time=appt_time,
            status='scheduled'
        )
        db.session.add(new_appt)
        db.session.commit()
        flash("Appointment created!", "success")
        return redirect(url_for('appointment_bp.list_my_appointments'))

    doctors = Doctor.query.all()
    return render_template('appointment_create.html', doctors=doctors)

@appointment_bp.route('/my')
@login_required
def list_my_appointments():
    if current_user.role == 'patient':
        appts = Appointment.query.filter_by(patient_id=current_user.id).all()
        return render_template('appointment_list.html', appointments=appts, role='patient')
    elif current_user.role == 'doctor':
        doc_profile = Doctor.query.filter_by(user_id=current_user.id).first()
        if doc_profile:
            appts = Appointment.query.filter_by(doctor_id=doc_profile.id).all()
            return render_template('appointment_list.html', appointments=appts, role='doctor')
        return render_template('appointment_list.html', appointments=[], role='doctor')
    else:
        appts = Appointment.query.all()
        return render_template('appointment_list.html', appointments=appts, role='admin')

@appointment_bp.route('/cancel/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if current_user.role == 'patient' and appt.patient_id != current_user.id:
        flash("You can only cancel your own appointments.", "error")
        return redirect(url_for('appointment_bp.list_my_appointments'))
    elif current_user.role == 'doctor':
        doc_profile = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doc_profile or appt.doctor_id != doc_profile.id:
            flash("You can only cancel your own appointments (doctor).", "error")
            return redirect(url_for('appointment_bp.list_my_appointments'))
    appt.status = 'cancelled'
    db.session.commit()
    flash("Appointment cancelled.", "info")
    return redirect(url_for('appointment_bp.list_my_appointments'))

@appointment_bp.route('/change/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def change_appointment(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if current_user.role == 'patient' and appt.patient_id != current_user.id:
        flash("You can only change your own appointments.", "error")
        return redirect(url_for('appointment_bp.list_my_appointments'))
    elif current_user.role == 'doctor':
        doc_profile = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doc_profile or appt.doctor_id != doc_profile.id:
            flash("You can only change your own appointments (doctor).", "error")
            return redirect(url_for('appointment_bp.list_my_appointments'))

    if request.method == 'POST':
        new_time_str = request.form.get('new_time')
        try:
            new_time = datetime.strptime(new_time_str, "%Y-%m-%d %H:%M")
            appt.appointment_time = new_time
            db.session.commit()
            flash("Appointment changed.", "success")
        except ValueError:
            flash("Incorrect date/time format.", "error")
        return redirect(url_for('appointment_bp.list_my_appointments'))

    return render_template('appointment_change.html', appt=appt)

