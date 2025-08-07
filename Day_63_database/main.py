from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False)
    title: Mapped[str] = mapped_column(String(250),unique=True,nullable=False,)
    author: Mapped[str]=mapped_column(String(250))
    rating: Mapped[float]=mapped_column(Float)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

books=User(id=2,title="Potter",author="HArry",rating=9)


with app.app_context():
    db.session.add(books)
    db.session.commit()


