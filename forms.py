from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional

class addPetForm(FlaskForm):
    "Form for adding a pet"
    name = StringField("Name", validators=[InputRequired()])
    species = StringField("Species")
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[NumberRange(min=0, max=30)])
    notes = StringField("Notes", validators=[Optional()])
    available = BooleanField("Is this pet available?", default=False)

class editPetForm(FlaskForm):
    """Form for editing an existing pet."""
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = StringField("Notes", validators=[Optional()])
    available = BooleanField("Is this pet available?", default=False)
