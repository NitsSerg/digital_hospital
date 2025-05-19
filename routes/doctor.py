from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.doctor import Doctor
from models.appointment import Appointment  
from utils.decorators import role_required
import datetime

doctor_bp = Blueprint('doctor_bp', __name__)

@doctor_bp.route('/all')
def list_doctors():
    spec = request.args.get('specialization', '')
    query = Doctor.query
    if spec:
        query = query.filter(Doctor.specialization.ilike(f"%{spec}%"))
    doctors = query.all()
    return render_template('doctors_list.html', doctors=doctors)

@doctor_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required(['doctor'])
def edit_doctor_profile():
    doctor_profile = Doctor.query.filter_by(user_id=current_user.id).first()

    my_appointments = []
    if doctor_profile:
        my_appointments = Appointment.query.filter_by(doctor_id=doctor_profile.id).all()

    if request.method == 'POST':
        specialization = request.form.get('specialization')
        experience_years = request.form.get('experience_years')
        start_str = request.form.get('work_start')
        end_str = request.form.get('work_end')

        if not doctor_profile:
            doctor_profile = Doctor(
                user_id=current_user.id,
                specialization=specialization,
                experience_years=int(experience_years),
                work_start=datetime.datetime.strptime(start_str, "%H:%M").time(),
                work_end=datetime.datetime.strptime(end_str, "%H:%M").time()
            )
            db.session.add(doctor_profile)
        else:
            doctor_profile.specialization = specialization
            doctor_profile.experience_years = int(experience_years)
            doctor_profile.work_start = datetime.datetime.strptime(start_str, "%H:%M").time()
            doctor_profile.work_end = datetime.datetime.strptime(end_str, "%H:%M").time()

        db.session.commit()
        flash("Профіль лікаря оновлено!", "success")
        return redirect(url_for('doctor_bp.edit_doctor_profile'))

    return render_template(
        'doctor_profile.html',
        doctor=doctor_profile,
        appointments=my_appointments
    )

@doctor_bp.route('/schedule/<int:doc_id>')
def show_schedule(doc_id):
    doctor_profile = Doctor.query.get_or_404(doc_id)
    return render_template('doctor_schedule.html', doctor=doctor_profile)