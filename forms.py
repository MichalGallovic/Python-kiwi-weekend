from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    source = StringField("Source", validators=[DataRequired()])
    destination = StringField("Destination", validators=[DataRequired()])
    departure_date = DateTimeField(
        label="Departure", format="%Y-%m-%d", validators=[DataRequired()]
    )
    arrival_date = DateTimeField(
        label="Arrival", format="%Y-%m-%d"
    )
