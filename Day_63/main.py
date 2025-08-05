from symtable import Class

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField

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
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap=Bootstrap5(app)

all_books = []

class Form(FlaskForm):
    name=StringField("Book name: ")
    author=StringField("Author: ")
    rating=StringField("Rating: ")



@app.route('/')
def home():
    return render_template("index.html", all_books=all_books)


@app.route("/add",methods=['POST','GET'])
def add():
    form=Form()
    if form.validate_on_submit():
        all_books.append([
            {
                "title":form.name.data,
                "author":form.author.data,
                "rating":form.rating.data,
            }
        ])
    print(all_books)
    return render_template("add.html",form=form)


if __name__ == "__main__":
    app.run(debug=True)

