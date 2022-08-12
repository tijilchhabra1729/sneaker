from Tool import app
import os
from Tool.forms import RegistrationForm, LoginForm, SearchForm
from Tool.models import User, Design, Adjective
from flask import render_template, request, url_for, redirect, flash, abort
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import desc, asc
from werkzeug.utils import secure_filename
import stripe

public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.htm', form=form)


@app.route('/mens', methods=['GET', 'POST'])
def mens():
    return render_template('mens.htm')


if __name__ == '__main__':
    app.run(debug=True)
