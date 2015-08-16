from flask.ext.wtf import Form
import re
from wtforms import StringField, TextAreaField, FileField, HiddenField, PasswordField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, regexp
from wtforms_components import EmailField


class PaintingCreateForm(Form):
	title = StringField('Titel', validators=[DataRequired()])
	notes = TextAreaField('Beschrijving')


class PaintingEditForm(Form):
	title = StringField('Titel', validators=[DataRequired()])
	notes = TextAreaField('Beschrijving')
	key = HiddenField('key')


class MusicForm(Form):
	title = StringField(label='Titel', validators=[DataRequired()])
	url = StringField('url')
	notes = TextAreaField('notes')

class ContactForm(Form):
	name = StringField('name', validators=[DataRequired()])
	email = EmailField('email')
	phone = IntegerField('phone')
	message = TextAreaField('message', validators=[DataRequired()])

class GigForm(Form):
	date = DateTimeField('date', validators=[DataRequired()])
	band = StringField('band', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])
	notes = TextAreaField('notes')
