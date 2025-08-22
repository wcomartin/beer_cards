from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from models import User # Assuming models are accessible via 'models' package
from database import db # Need db for User operations
from datetime import datetime # For last_login

auth_bp = Blueprint('auth_bp', __name__)

# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('beer_bp.index'))
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email address already exists', 'error')
#             return redirect(url_for('auth_bp.register'))
        
#         new_user = User(email=email, first_name=first_name, last_name=last_name)
#         new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Account created successfully! Please log in.', 'success')
#         return redirect(url_for('auth_bp.login'))
#     return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('beer_bp.index')) # Redirect to beer blueprint's index
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('auth_bp.login')) # Redirect to blueprint's login

        login_user(user, remember=remember)
        user.last_login = datetime.utcnow() # Update last login time
        db.session.commit()
        return redirect(url_for('beer_bp.index')) # Redirect to beer blueprint's index
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required # Protect logout route
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_bp.login')) # Redirect to blueprint's login

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if not current_user.check_password(current_password):
            flash('Incorrect current password.', 'error')
            return redirect(url_for('auth_bp.change_password'))

        if new_password != confirm_new_password:
            flash('New password and confirmation do not match.', 'error')
            return redirect(url_for('auth_bp.change_password'))

        # Add any password complexity requirements here (e.g., min length)
        if len(new_password) < 6: # Example: minimum 6 characters
            flash('New password must be at least 6 characters long.', 'error')
            return redirect(url_for('auth_bp.change_password'))

        current_user.set_password(new_password)
        db.session.commit()
        flash('Your password has been updated successfully!', 'success')
        return redirect(url_for('beer_bp.index')) # Redirect to a main page after success
    return render_template('change_password.html')