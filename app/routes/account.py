from flask import render_template, request, redirect, url_for, jsonify

from app import app, db, bcrypt
from app.forms.account import SignUpForm
from app.models.application.user import UserModel
from app.util.form import validate_on_submit


@app.route('/', methods=['GET', 'POST'])
def main():
    data = {"server_status": "Healthy!"}
    return jsonify(data)

@app.route('/account/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)

    if validate_on_submit(form):
        new_user = UserModel(
            username=form.username.data,
            password=bcrypt.generate_password_hash(form.password.data),
            name=form.name.data,
            nickname=form.nickname.data,
            email=form.email.data,
            company=form.company.data
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('signup_complete'))

    return render_template('signup.html', form=form)


@app.route('/account/signup/complete')
def signup_complete():
    return render_template('signup_complete.html')
