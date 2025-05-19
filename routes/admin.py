from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from utils.decorators import role_required
from models import db
from models.user import User
from models.doctor import Doctor
from models.appointment import Appointment

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard')
@login_required
@role_required(['admin'])
def dashboard():
    users = User.query.all()
    doctors = Doctor.query.all()
    appointments = Appointment.query.all()
    return render_template('admin_dashboard.html', users=users, doctors=doctors, appointments=appointments)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # Видаляємо лікаря, якщо він є для цього користувача
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if doctor:
        db.session.delete(doctor)
    db.session.delete(user)
    db.session.commit()
    flash('Користувача та пов’язаного лікаря видалено', 'success')
    return redirect(url_for('admin_bp.dashboard'))

@admin_bp.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Лікаря видалено', 'success')
    return redirect(url_for('admin_bp.dashboard'))

@admin_bp.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Запис видалено', 'success')
    return redirect(url_for('admin_bp.dashboard'))



