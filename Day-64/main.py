import os

from flask import Flask, render_template, redirect, url_for, request
from flask.cli import load_dotenv
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, nullslast
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

load_dotenv()
# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer,nullable=False)
    description: Mapped[str] = mapped_column(String(250),nullable=False)
    rating: Mapped[float] = mapped_column(Float)
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String(250))
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-collection.db"
db.init_app(app)


@app.route("/")
def home():
    movies = db.session.execute(
        db.select(Movie).order_by(nullslast(Movie.rating.desc()))
    ).scalars().all()
    i=1
    for movie in movies:
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.title == movie.title)).scalar()
        movie_to_update.ranking = i
        db.session.commit()
        i+=1

    new_movies = db.session.execute(
        db.select(Movie).order_by(nullslast(Movie.rating.desc()))
    ).scalars().all()

    return render_template("index.html",movies=new_movies)

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

    if form.validate_on_submit():
        url = "https://api.themoviedb.org/3/search/movie"

        params={
            "query": form.title.data
        }

        headers = {
            "accept": "application/json",
            "Authorization": os.getenv("key")
        }


        response = (requests.get(url, headers=headers,params=params)).json()
        results=response['results']

        return render_template("select.html", movies=results)




    return render_template("add.html",form=form)

@app.route("/select/<int:id>")
def select(id):
    url_new = f"https://api.themoviedb.org/3/movie/{id}"



    headers = {
        "accept": "application/json",
        "Authorization": os.getenv("key")
    }

    response_new = (requests.get(url_new, headers=headers)).json()
    poster_path = response_new.get("poster_path")
    img_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
    new_movie = Movie(title=response_new['original_title'],
                      year=response_new['release_date'],
                      description=response_new['overview'],
                      rating=0,
                      ranking=0,
                      review="",
                      img_url=img_url)
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('edit',title=response_new['original_title']))

if __name__ == '__main__':
    app.run(debug=True)
