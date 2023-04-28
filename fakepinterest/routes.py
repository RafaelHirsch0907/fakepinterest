# CRIAR AS ROTAS DO SITE

from flask import render_template, url_for, redirect
from fakepinterest import app, dataBase, bcrypt
from flask_login import login_required, login_user, logout_user
from fakepinterest.forms import FormLogin, FormCreateLogin
from fakepinterest.models import User, Photo

@app.route("/", methods=["GET", "POST"])
def homepage():
    formLogin = FormLogin()
    return render_template("homepage.html", form=formLogin)

@app.route("/createlogin", methods=["GET", "POST"])
def createlogin():
    formCreateLogin = FormCreateLogin()
    if formCreateLogin.validate_on_submit():
        password = bcrypt.generate_password_hash(formCreateLogin.password.data)
        user = User(username=formCreateLogin.username.data, password=password, email=formCreateLogin.email.data)

        dataBase.session.add(user)
        dataBase.session.commit()
        login_user()
        return redirect(url_for("profile", user=user.username))
    return render_template("createlogin.html", form=formCreateLogin)

@app.route("/profile/<user>")
@login_required
def profile(user):
    return render_template("profile.html", user=user)
