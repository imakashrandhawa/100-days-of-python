from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired
from wtforms.validators import URL
import csv

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


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location= URLField('Cafe Location on Google maps(URL)', validators=[DataRequired(),URL()])
    open_time= StringField('Opening Time', validators=[DataRequired()])
    close_time= StringField('Closing Time', validators=[DataRequired()])
    coffee_rating=SelectField("Coffee Rating", choices=[('☕','☕'),('☕☕','☕☕'),('☕☕☕','☕☕☕'),('☕☕☕☕','☕☕☕☕')],validators=[DataRequired()])
    wifi_rating=SelectField("Wifi Strength Rating", choices=[('🛜','🛜'),('🛜🛜','🛜🛜'),('🛜🛜🛜','🛜🛜🛜'),('🛜🛜🛜🛜','🛜🛜🛜🛜')],validators=[DataRequired()])
    power_availability=SelectField("Power Socket Availability", choices=[('🔌','🔌'),('🔌🔌','🔌🔌'),('🔌🔌🔌','🔌🔌🔌'),('🔌🔌🔌🔌','🔌🔌🔌🔌')],validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST','GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv','a+', newline='', encoding='utf-8') as csv_file:
            csv_file.writelines(f"\n{form.cafe.data},{form.location.data},{form.open_time.data},{form.close_time.data},{form.coffee_rating.data},{form.wifi_rating.data},{form.power_availability.data}")

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()


    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)



if __name__ == '__main__':
    app.run(debug=True)
