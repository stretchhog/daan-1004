from flask.ext.restful import abort
from app.forms import MusicForm
from app.models import Music


def get_music(id):
	music = Music.get_by_id(id)
	form = MusicForm()
	form.title.data = music.title
	form.youtube.data = music.youtube
	form.notes.data = music.notes
	return music, form

def update_music(id, data):
	form = MusicForm(data=data)
	music = Music.get_by_id(id)
	music.title = form.title.data
	music.notes = form.notes.data
	music.youtube = form.youtube.data
	return music.put()

def create_music(data):
	form = MusicForm(data=data)
	if form.validate():
		pass
	else:
		abort(400)
	music = Music()
	music.title = form.title.data
	music.youtube = form.youtube.data
	music.notes = form.notes.data
	return music.put()

def delete_music(id):
	return Music.get_by_id(id).key.delete()


def get_musics():
	return Music.query().order(-Music.date_added).fetch()
