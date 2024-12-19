#!/usr/bin/python3
"""
AUTH module
"""

from flask import Blueprint, render_template, session
from flask import redirect, url_for, flash, request, jsonify
from models import storage
from models.models import User
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from .forms import SignInForm, SignUpForm, ForgotPasswordForm
from auth import app_views_auth


import datetime
import os
from operator import attrgetter


auth = Blueprint('auth', __name__)


@app_views_auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """Sing up function"""
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        name = sign_up_form.name.data
        address = sign_up_form.address.data
        email = sign_up_form.email.data
        phone_number = sign_up_form.phone_number.data
        password = sign_up_form.password.data
        my_dict = {"name": name,
                   "email": email,
                   "phone_number": phone_number,
                   "role": "Student",
                   "password": password,
                   "address": address,
                   "profile_image": "user.avif"}
    
        new_instance = User()
        for key, value in my_dict.items():
            setattr(new_instance, key, value)
        try:
            new_instance.save()
            message = """Account successfully created"""
            flash(message, 'success')
            return redirect(url_for('app_views_home.home'))

        except IntegrityError as e:
            print(e)
            storage.close()
            message = """Account not created, Email already exist"""
            flash(message, 'error')
            return redirect(url_for('app_views_home.home'))
    else:
        message = """An error occur while creating your accound!"""
        flash(message, 'error')
        return redirect(url_for('app_views_home.home'))
    

@app_views_auth.route("/")
def home():
    """SignIn"""
    return "This is auth blueprint"
