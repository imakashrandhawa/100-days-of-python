import os
from tkinter.font import names

from flask import Flask, render_template,request
import requests
import smtplib

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/form-entry",methods=['POST','GET'])
def data():
    name =request.form.get('username')
    email = request.form.get('emailaddress')
    phone = request.form.get('phonenumber')
    message = request.form['messageu']
    emailid=os.environ.get("EMAIL_USER")
    password=os.environ.get("PASSWORD_USER")
    msg=f"Information \n Name:{name} \n Email:{email}\n Phone Number={phone} \n Message:{message}"

    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(user=emailid,password=password)
        connection.sendmail(
            from_addr=emailid,
            to_addrs="randhawa.codes@gmail.com",
            msg=msg
        )

    return "Successfully sent"


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
