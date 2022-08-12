from Tool import app, db
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('index')
            return redirect(next)
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'
    return render_template('login.htm', form=form, error=error)


@app.route('/mens', methods=['GET', 'POST'])
def mens():
    return render_template('mens.htm')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    name = []
    design = []
    for i in current_user.design_names.split(','):
        name.append(i)
    for i in current_user.designs:
        design.append(i)
    ranges = range(len(design))
    return render_template('account.htm', name=name, design=design, ranges=ranges)


@app.route('/designfind/<adjectives>/<name_>', methods=['GET', 'POST'])
@login_required
def find(adjectives, name_):
    form = SearchForm()
    if form.validate_on_submit():
        adjectives_ = form.adjectives.data
        return redirect(url_for('find', adjectives=adjectives_, name_=form.name.data))
    da_list = []
    if adjectives != 'None':
        for i in adjectives.split(','):
            adjective = Adjective.query.filter_by(name=i.lower()).first()
            if adjective:
                for j in adjective.designs:
                    if j not in current_user.designs:
                        da_list.append(j)
    else:
        pass
    nums = range(len(da_list))
    print(da_list)
    return render_template('find.htm', da_list=da_list, form=form, adjectives=adjectives, name_=name_, nums=nums, rame=name_)


@app.route('/add/<design_id>/<adjectives_>/<where>/<name_>', methods=['GET', 'POST'])
@login_required
def add(design_id, adjectives_, where, name_):
    design = Design.query.filter_by(id=int(design_id)).first()
    current_user.designs.append(design)
    if current_user.design_names == '':
        current_user.design_names += name_
    else:
        current_user.design_names += ','+name_
    db.session.commit()
    if where == 'find':
        return redirect(url_for(where, adjectives=adjectives_, name_=name_))
    else:
        return redirect(url_for(where))


@app.route('/remove/<design_id>/<adjectives_>/<where>/<name_>', methods=['GET', 'POST'])
@login_required
def remove(design_id, adjectives_, where, name_):
    design = Design.query.filter_by(id=int(design_id)).first()
    current_user.designs.remove(design)
    db.session.commit()
    dn = current_user.design_names.split(',')
    dn.remove(name_)
    current_user.design_names = ''.join(dn)
    db.session.commit()
    if where == 'find':
        return redirect(url_for(where, adjectives=adjectives_))
    else:
        return redirect(url_for(where))


######## payments #########

@app.route('/payment')
def payment():
    return render_template('account.htm', public_key=public_key)


@app.route('/thankyou')
def thankyou():
    return render_template("thank_you.htm")


@app.route('/payment/hqhfoufhofhqoufhqoufh', methods=['POST'])
def payment_form():

    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        amount=499,
        customer=customer.id,
        currency='usd',
        description='Premium'
    )

    return redirect(url_for('thankyou'))


if __name__ == '__main__':
    app.run(debug=True)
