import os

from lib2to3.fixer_util import String

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

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
app.secret_key=os.environ.get("SECRET_KEY")


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
    form=MyForm()
    return render_template("login.html",form=form)

class MyForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField(label="Log in")

if __name__ == '__main__':
    app.run(debug=True)
