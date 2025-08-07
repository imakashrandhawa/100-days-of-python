from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

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
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer,nullable=False)
    description: Mapped[str] = mapped_column(String(250),nullable=False)
    rating: Mapped[float] = mapped_column(Float,nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-collection.db"
db.init_app(app)


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.id))
    all_movies = result.scalars().all()
    return render_template("index.html",movies=all_movies)

with app.app_context():
    db.session.commit()

class Edit(FlaskForm):
    rating = StringField("Your Rating Out of 10")
    review = StringField("Your Review")
    submit = SubmitField('Done')

@app.route("/edit/<string:title>",methods=["POST","GET"])
def edit(title):
    form=Edit()
    movie = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
    if form.validate_on_submit():
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
        movie_to_update.rating=form.rating.data
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html",form=form,movies=movie)

@app.route("/delete/<string:title>",methods=["POST","GET"])
def delete(title):
    book_to_delete = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

class Add(FlaskForm):
    title = StringField("Movie Title")
    add = SubmitField('Add Movie')


@app.route("/add",methods=["POST","GET"])
def add():
    form=Add()
    list=[]
    if form.validate_on_submit():
        url = "https://api.themoviedb.org/3/search/movie"

        params={
            "query": form.title.data
        }

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OTNhODNiNjgxNjFkZDc1MzIzYWVhMGEwYWZlYmYwOCIsIm5iZiI6MTc1NDU4MTUzNS42NzI5OTk5LCJzdWIiOiI2ODk0Y2ExZmNiZDk1Mjc4YTkyOGE1MTQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.HAKaGFLMVmbjoJOIlpv6YPDixo4yrjR5aIPMrma29_0"
        }

        response = (requests.get(url, headers=headers,params=params)).json()
        results=response['results']
        for result in results:
            list.append(f"{result['title']} {result['release_date']}")
        print(list)
        return render_template("select.html", movies=list)


    return render_template("add.html",form=form)



if __name__ == '__main__':
    app.run(debug=True)
