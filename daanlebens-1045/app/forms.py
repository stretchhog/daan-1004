from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, HiddenField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email
from wtforms_components import EmailField


class PaintingCreateForm(Form):
	title = StringField('Titel', validators=[DataRequired()])
	notes = TextAreaField('Beschrijving')


class MusicForm(Form):
	title = StringField(label='Titel', validators=[DataRequired()])
	url = StringField('url')
	notes = TextAreaField('notes')


class ContactForm(Form):
	name = StringField('name', validators=[DataRequired(message="Naam is verplicht.")])
	email = EmailField('email', validators=[DataRequired(message="Email adres is verplicht"),
	                                        Email(message="Email adres formaat klopt niet.")])
	phone = StringField('phone')
	message = TextAreaField('message', validators=[DataRequired(message="Een bericht is verplicht.")])


class GigForm(Form):
	date = DateTimeField('date', validators=[DataRequired()])
	band = StringField('band', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])
	notes = TextAreaField('notes')
