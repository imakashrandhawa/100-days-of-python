import os
from ensurepip import bootstrap

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


app = Flask(__name__)
bootstrap=Bootstrap5(app)
app.secret_key=os.environ.get("SECRET_KEY")


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=['POST','GET'])
def login():
    form=MyForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        if email=="admin@email.com" and password=="12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")

    return render_template("login.html",form=form)

class MyForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email(message="Enter valid email")])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    submit=SubmitField(label="Log in")

if __name__ == '__main__':
    app.run(debug=True)
