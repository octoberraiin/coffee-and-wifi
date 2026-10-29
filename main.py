from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import URL, DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps (URL)', validators=[URL()])
    opening_time = StringField('Opening time e.g. 10AM')
    closing_time = StringField('Closing time e.g. 8PM')
    coffee_rating = SelectField('Coffee Rating', choices=[(emoji, emoji) for emoji in ['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️']])
    wifi_rating = SelectField('Wifi Rating', choices=[(emoji, emoji) for emoji in ['✘', '💪️', '💪️💪️', '💪💪💪️', '💪💪💪💪️', '💪💪💪💪💪']])
    power_socket = SelectField('Power Socket Availability', choices=[(emoji, emoji) for emoji in ['✘', '🔌️', '🔌🔌', '🔌🔌🔌️', '🔌🔌🔌🔌️', '🔌🔌🔌🔌🔌']])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', newline='', encoding='utf-8', mode='a') as csv_file:
            csv_data = csv.writer(csv_file)
            csv_data.writerow([
                '\n' + form.name.data,
                form.location.data,
                form.opening_time.data,
                form.closing_time.data,
                form.coffee_rating.data,
                form.wifi_rating.data,
                form.power_socket.data
            ])
        return redirect(url_for('cafes'))
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
