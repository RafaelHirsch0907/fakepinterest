# CRIAR AS ROTAS DO SITE

from flask import render_template, url_for, redirect
from fakepinterest import app, dataBase, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCreateLogin, FormPhoto
from fakepinterest.models import User, Photo
from werkzeug.utils import secure_filename
import os

@app.route("/", methods=["GET", "POST"])
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        user = User.query.filter_by(email=formLogin.email.data).first()
        if user and bcrypt.check_password_hash(user.password, formLogin.password.data):
            login_user(user)
            return redirect(url_for("profile", user_id=user.id))
    return render_template("homepage.html", form=formLogin)

@app.route("/createlogin", methods=["GET", "POST"])
def createlogin():
    formCreateLogin = FormCreateLogin()
    if formCreateLogin.validate_on_submit():
        password = bcrypt.generate_password_hash(formCreateLogin.password.data)
        user = User(username=formCreateLogin.username.data, password=password, email=formCreateLogin.email.data)

        dataBase.session.add(user)
        dataBase.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("profile", user_id=user.id))
    return render_template("createlogin.html", form=formCreateLogin)

@app.route("/profile/<user_id>", methods=["GET", "POST"])
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        formPhoto = FormPhoto()
        if formPhoto.validate_on_submit():
            archive = formPhoto.photo.data
            securityName = secure_filename(archive.filename)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], securityName)
            archive.save(path)
            photo = Photo(image=securityName, userId=current_user.id)
            dataBase.session.add(photo)
            dataBase.session.commit()
        return render_template("profile.html", user=current_user, form=formPhoto)
    else:
        user = User.query.get(int(user_id))
        return render_template("profile.html", user=user, form=None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
def feed():
    photos = Photo.query.order_by(Photo.createDate.desc()).all()
    return render_template("feed.html", photos=photos)
