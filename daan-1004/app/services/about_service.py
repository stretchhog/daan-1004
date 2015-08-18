import datetime
from app.forms import GigForm
from app.models import Gig

__author__ = 'tvancann'


def create(data):
	form = GigForm(data=data)
	if form.validate():
		pass
	else:
		return form.errors
	gig = Gig()
	gig.band = form.band.data
	gig.date = form.date.data
	gig.location = form.location.data
	gig.notes = form.notes.data
	return gig.put()


def get_all():
	now = datetime.datetime.now()
	return Gig.query(Gig.date >= now).order(Gig.date).fetch()


def delete_by_id(id):
	return Gig.get_by_id(id).key.delete()


def get_by_id(id):
	gig = Gig.get_by_id(id)
	form = GigForm()
	form.band.data = gig.band
	form.date.data = gig.date
	form.location.data = gig.location
	form.notes.data = gig.notes
	return gig, form


def update_by_id(id, data):
	form = GigForm(data=data)
	gig = Gig.get_by_id(id)
	gig.band = form.band.data
	gig.date = form.date.data
	gig.location = form.location.data
	gig.notes = form.notes.data
	return gig.put()
