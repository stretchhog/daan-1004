from app.forms import PaintingEditForm
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
