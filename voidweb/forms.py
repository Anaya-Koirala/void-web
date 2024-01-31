from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class WritingForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    subtitle = StringField("Subtitle", validators=[Length(max=100)])
    content = TextAreaField("Content", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Upload Writing")


class ShitpostingForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=100)])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Upload Shitposting")
