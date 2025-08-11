import os

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

# CREATE TABLE IN DB


class User(db.Model):
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

        user=User(email=email,password=password,name=name)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("secrets",user=name))

    return render_template("register.html")


@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")

        users=(db.session.execute(db.select(User))).scalars()
        for user in users:
            if user.email == email:
                if user.password == password:
                    return redirect(url_for("secrets", user=user.name))
                else:
                    return render_template("login.html", feedback="Password Incorrect!!")
            else:
                return render_template("login.html", feedback="User doesn't exist")
        return render_template("login.html", feedback="")
    return render_template("login.html", feedback="")




@app.route('/secrets/<string:user>')
def secrets(user):
    return render_template("secrets.html",name=user)


@app.route('/logout')
def logout():
    pass


@app.route('/download/<string:name>',methods=["GET","POST"])
def download(name):
    send_from_directory(directory="files",path="Day-68/static/files/cheat_sheet.pdf")
    return render_template("secrets.html",name=name)




if __name__ == "__main__":
    app.run(debug=True)
