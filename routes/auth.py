from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from models import db
from models.user import User

auth_bp = Blueprint('auth_bp', __name__)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'patient')

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("User with this username or email already exists.", "error")
            return redirect(url_for('auth_bp.register'))

        hashed_pwd = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_pwd, role=role)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Registration successful! You are now logged in.", "success")

        if new_user.role == 'doctor':
            return redirect(url_for('doctor_bp.edit_doctor_profile'))
        elif new_user.role == 'admin':
            return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!", "success")

            if user.role == 'doctor':
                return redirect(url_for('doctor_bp.edit_doctor_profile'))
            elif user.role == 'admin':
                return redirect('/admin/dashboard')
            else:
                return redirect(url_for('appointment_bp.list_my_appointments'))

        else:
            flash("Invalid username/email or password.", "error")
            return redirect(url_for('auth_bp.login'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth_bp.login'))
