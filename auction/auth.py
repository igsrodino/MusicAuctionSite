from flask import (Blueprint, flash, render_template, request, url_for, redirect) 
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db
from .models import User


#create a blueprint
bp = Blueprint('auth', __name__)

# Register function
@bp.route("/register", methods=["GET", "POST"])
def register():
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():

        # Grab all of the data from the form
        username = registerForm.username.data
        email = registerForm.email_id.data
        phone = registerForm.phone.data
        mail_address = registerForm.address.data
        pwd = registerForm.password.data

        # Check if there is a user with that username already
        # Note: Returns either the user object or NULL
        u = User.query.filter_by(name = username).first()
        if u:
            flash("This username is already taken!", "info")
            return redirect(url_for("auth.login"))
        
        # If the username is unique, create the user
        # Hash the password
        pwd_hash = generate_password_hash(pwd)
        new_user = User(name=username, email_address=email, phone_number = phone, mail_address = mail_address, password_hash = pwd_hash)
        
        db.session.add(new_user)
        db.session.commit()
        flash("Account successfully registered! Please log in.", "info")
        return redirect(url_for("auth.login"))
    
    else:
        return render_template("user.html", form = registerForm, heading = "Register Account")

# Login function
@bp.route('/login', methods=['GET', 'POST'])
def login():
    print('In Login View function')
    loginForm = LoginForm()
    error=None

    # Check if there is a user with that username already, and check if user input matches user in db
    if (loginForm.validate_on_submit()):
        user_name = loginForm.user_name.data
        password = loginForm.password.data
        u1 = User.query.filter_by(name=user_name).first()
   
        # Display error message if user inputs wrong username or password
        if u1 is None or not check_password_hash(u1.password_hash, password):
            error='Incorrect username or password!'

        # Login user if credentials are correct
        if error is None:
            login_user(u1)
            
            nextp = request.args.get('next') 

            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=loginForm, heading='Login')

# Logout function
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    # Display logged out message if succesful
    flash("Successfully logged out!", "info")
    return redirect(url_for("auth.login"))
