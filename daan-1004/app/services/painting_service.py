from base64 import b64encode
from werkzeug.exceptions import abort
from app.forms import PaintingEditForm, PaintingCreateForm
from app.models import Painting

__author__ = 'Stretchhog'

def get_painting(id):
	painting = Painting.get_by_id(id)
	form = PaintingEditForm()
	form.title.data = painting.title
	form.notes.data = painting.notes
	form.key.data = painting.key
	return painting, form

def update_painting(id, data):
	form = PaintingEditForm(data=data)
	painting = Painting.get_by_id(id)
	painting.title = form.title.data
	painting.notes = form.notes.data
	return painting.put()

def create_painting(data, image):
	form = PaintingCreateForm(data=data)
	# if form.validate():
	# 	pass
	# else:
	# 	abort(400)
	painting = Painting()
	painting.title = form.title.data
	painting.notes = form.notes.data
	painting.image = b64encode(image)
	return painting.put()

def delete_painting(id):
	return Painting.get_by_id(id).key.delete()


def get_paintings():
	return Painting.query().order(-Painting.date_added).fetch()
