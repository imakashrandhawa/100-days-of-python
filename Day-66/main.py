import json

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(to_dict(random_cafe))

@app.route("/all")
def all_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    new_cafes=[]
    for cafe in all_cafes:
        new_cafe=to_dict(cafe)
        new_cafes.append(new_cafe)
    return jsonify(new_cafes)

@app.route("/add",methods=["POST"])
def add():
    name=request.form['name']
    location=request.form['map_url']
    print(name,location)
    response={
       "response":{
           "success":"Successfully added the cafe"
       }
    }
    return response

@app.route("/update/<int:id>",methods=["GET","POST","PATCH"])
def update(id):
    try:
        cafe = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
        cafe.coffee_price=request.args.get("new_price")
        db.session.commit()
        return {
            "success":"Successfully updated the price."
        }
    except:
        return {
            "Not found": "ID doesn't exist"
        }

@app.route("/closed/<int:id>",methods=["DELETE"])
def closed(id):
    if request.args.get("api-key") == "TopScretAPIKey":
        try:
            cafe = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
            db.session.delete(cafe)
            db.session.commit()
            return{
                "Success":"Cafe has been removed from the list"
            }
        except:
            return {
                "Failed":"Cafe does not exist"
            }
    else:
        return {
            "Not Allowed":"Make sure you have correct API key"
        }





# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
