import os

import flask
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from wtforms.fields.simple import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
login_manager=LoginManager()
login_manager.init_app(app)

# CREATE TABLE IN DB


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))



with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register',methods=["POST","GET"])
def register():
    if request.method == "POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        hash_pass=generate_password_hash(password,method="pbkdf2:sha256",salt_length=8)
        user=User(email=email,password=hash_pass,name=name)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("secrets",user=name))

    return render_template("register.html")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))


@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        passwor = request.form.get("password")
        user=(db.session.execute(db.select(User).where(User.email == email))).scalar()
        if not user or not check_password_hash(user.password,passwor):
            return render_template("login.html", feedback="User or Password Incorrect!!")
        login_user(user)
        return redirect(url_for("secrets",user=user.name))
    return render_template("login.html")


# @app.route('/login',methods=["POST","GET"])
# def login():
#     if request.method == "POST":
#         email=request.form.get("email")
#         password=request.form.get("password")
#         hash_pass=generate_password_hash(password,method="pbkdf2:sha256",salt_length=8)
#
#
#         users=(db.session.execute(db.select(User))).scalars()
#         for user in users:
#             if user.email == email:
#                 if user.password == hash_pass:
#                     return redirect(url_for("secrets", user=user.name))
#                 else:
#                     return render_template("login.html", feedback="Password Incorrect!!")
#             else:
#                 return render_template("login.html", feedback="User doesn't exist")
#         return render_template("login.html", feedback="")
#     return render_template("login.html", feedback="")




@app.route('/secrets/<string:user>')
@login_required
def secrets(user):
    return render_template("secrets.html",name=user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/download',methods=["GET","POST"])
@login_required
def download():
    location=os.path.join(app.root_path,"static","files")
    file=send_from_directory(location,path="cheat_sheet.pdf")
    return file




if __name__ == "__main__":
    app.run(debug=True)
