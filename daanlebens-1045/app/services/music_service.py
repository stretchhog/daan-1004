import re
from flask.ext.restful import abort
from app.forms import MusicForm
from app.models import Music


def get_by_id(id):
	music = Music.get_by_id(id)
	form = MusicForm()
	form.title.data = music.title
	form.url.data = music.url
	form.notes.data = music.notes
	return music, form


def update_by_id(id, data):
	form = MusicForm(data=data)
	music = Music.get_by_id(id)
	music.title = form.title.data
	music.notes = form.notes.data
	music.youtube = form.url.data
	return music.put()


def create(data):
	form = MusicForm(data=data)
	if form.validate():
		pass
	else:
		abort(400)
	music = Music()
	music.title = form.title.data
	music.url = extract_video_id(form.url.data)
	music.notes = form.notes.data
	return music.put()


def delete_by_id(id):
	return Music.get_by_id(id).key.delete()


def get_all():
	return Music.query().order(-Music.date_added).fetch()


def extract_video_id(url):
	regex = (
		r'(https?://)?(www\.)?'
		'(youtube|youtu|youtube-nocookie)\.(com|be)/'
		'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

	youtube_regex_match = re.match(regex, url)
	if youtube_regex_match:
		return youtube_regex_match.group(6)
