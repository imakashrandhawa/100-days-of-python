from symtable import Class

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Nullable


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

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


class Form(FlaskForm):
    name=StringField("Book name: ")
    author=StringField("Author: ")
    rating=StringField("Rating: ")



@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    print(all_books)
    return render_template("index.html", all_books=all_books)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250))
    rating: Mapped[float] = mapped_column(Float)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
db.init_app(app)


@app.route("/add",methods=['POST','GET'])
def add():
    form=Form()
    if form.validate_on_submit():
        new_book = Book(
            title=form.name.data,
            author=form.author.data,
            rating=float(form.rating.data)  # Cast to float for model
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html",form=form)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

