import datetime

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ck=CKEditor(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    all_posts=(db.session.execute(db.select(BlogPost).order_by(BlogPost.id))).scalars()
    posts = []
    for post in all_posts:
        posts.append(post)
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/show_post/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = (db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id))).scalar()
    return render_template("post.html", post=requested_post)

class Postform(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    subtitle=StringField("Subtitle",validators=[DataRequired()])
    author=StringField("Your Name",validators=[DataRequired()])
    img_url= URLField("Url for bg Image",validators=[DataRequired()])
    body=CKEditorField("body",validators=[DataRequired()])

@app.route("/add_post",methods=["POST","GET"])
def add_post():
    print(datetime.date.today())
    postform=Postform()
    if postform.validate_on_submit():
        new_post=BlogPost(title=postform.title.data,subtitle=postform.subtitle.data,date=datetime.date.today(),body=postform.body.data,author=postform.name.data,img_url=postform.url.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html",form=postform,heading="New Post")

@app.route("/edit-post/<int:post_id>",methods=["GET","POST"])
def edit_post(post_id):
    requested_post = (db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id))).scalar()
    postform = Postform(obj=requested_post)

    if postform.validate_on_submit():
        postform.populate_obj(requested_post)
        db.session.commit()
        return redirect(url_for("show_post",post_id=post_id))
    return render_template("make-post.html",form=postform,heading="Edit Post")
# TODO: edit_post() to change an existing blog post

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
