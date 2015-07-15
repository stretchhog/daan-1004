from flask.ext.wtf import Form
import re
from wtforms import StringField, TextAreaField, FileField, HiddenField, PasswordField
from wtforms.validators import DataRequired, regexp


class PaintingCreateForm(Form):
	title = StringField('Titel', validators=[DataRequired()])
	notes = TextAreaField('Beschrijving')


class PaintingEditForm(Form):
	title = StringField('Titel', validators=[DataRequired()])
	notes = TextAreaField('Beschrijving')
	key = HiddenField('key')


class MusicForm(Form):
	title = StringField('title', validators=[DataRequired()])
	youtube = StringField('youtube')
	notes = TextAreaField('notes')
