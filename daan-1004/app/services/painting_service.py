from base64 import b64encode
from google.appengine.api.images import get_serving_url
from google.appengine.ext import blobstore
import re
from google.appengine.ext.blobstore import BlobInfo
from app.forms import PaintingCreateForm, PaintingCreateForm
from app.models import Painting

__author__ = 'Stretchhog'

def get_painting(id):
	painting = Painting.get_by_id(id)
	form = PaintingCreateForm()
	form.title.data = painting.title
	form.notes.data = painting.notes
	return painting, form

def update_painting(id, data):
	form = PaintingCreateForm(data=data)
	painting = Painting.get_by_id(id)
	painting.title = form.title.data
	painting.notes = form.notes.data
	return painting.put()

def create_painting(data, blob_key):
	form = PaintingCreateForm(data=data)
	painting = Painting(title=form.title.data, blob_key=blob_key, notes=form.notes.data)
	return painting.put()

def delete_painting(id):
	painting = Painting.get_by_id(id)
	BlobInfo.get(painting.blob_key).delete()
	return painting.key.delete()


def get_paintings():
	paintings = Painting.query().order(-Painting.date_added).fetch()
	images = [get_serving_url(painting.blob_key) for painting in paintings]
	return paintings, images

