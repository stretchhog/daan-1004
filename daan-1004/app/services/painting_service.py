from base64 import b64encode
from werkzeug.exceptions import abort
from app.forms import PaintingEditForm, PaintingCreateForm
from app.models import Painting

__author__ = 'Stretchhog'

def get_painting(key):
	qry = Painting.query(Painting.key == key)
	painting = qry.fetch(1)[0]
	form = PaintingEditForm()
	form.title.data = painting.title
	form.notes.data = painting.notes
	form.key.data = painting.key
	return painting, form

def update_painting(data):
	form = PaintingEditForm(data=data)
	qry = Painting.query(Painting.key == form.key.data)
	painting = qry.fetch(1)[0]
	painting.title = form.title.data
	painting.notes = form.notes.data
	return painting.put()

def create_painting(data):
	form = PaintingCreateForm(data=data)
	if form.validate():
		pass
	else:
		abort(400)
	painting = Painting()
	painting.title = form.title.data
	painting.notes = form.notes.data
	image = form.image.data
	painting.image = b64encode(image)
	return painting.put()

def delete_painting(key):
	qry = Painting.query(Painting.key == key)
	return qry.fetch(1)[0].delete()


def get_paintings():
	return Painting.query().order(-Painting.date_added).fetch()
