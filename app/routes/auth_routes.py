# app/routes/auth_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "error")
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered successfully!", "success")
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials!", "error")
            return redirect(url_for('auth.login'))

        login_user(user)
        flash("Logged in successfully!", "success")
        return redirect(url_for('expenses.dashboard'))  # we'll make dashboard next

    return render_template('login.html')


@auth_bp.route('/logout', methods=['POST'])
@login_required  # Ensure that only authenticated users can access this
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')  

@auth_bp.route('/update_income', methods=['POST'])
@login_required
def update_income():
    try:
        income = float(request.form['income'])
        current_user.income = income
        db.session.commit()
        flash("Income updated successfully!", "success")
    except ValueError:
        flash("Invalid income value.", "danger")
    return redirect(url_for('expenses.dashboard'))