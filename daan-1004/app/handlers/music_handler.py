from flask import make_response, render_template, redirect, request
from flask.ext.restful import Resource
from app.services import music_service as service
from app.forms import MusicForm
from main import api

__author__ = 'Stretchhog'

class MusicList(Resource):
	def get(self):
		musics = service.get_all()
		return make_response(render_template("music/list.html", title="Muziek", musics=musics))


class MusicDelete(Resource):
	def get(self, id):
		service.delete_by_id(id)
		return redirect(api.url_for(MusicList), 301)


class MusicDetail(Resource):
	def get(self, id):
		painting, form = service.get_by_id(id)
		return make_response(render_template('music/detail.html', painting=painting, form=form))

	def post(self, id):
		key = service.update_by_id(id, request.get_json())
		if key is not None:
			return redirect(api.url_for(MusicList), 301)


class MusicCreate(Resource):
	def get(self):
		form = MusicForm()
		return make_response(render_template('music/create.html', form=form))

	def post(self):
		key = service.create(request.get_json())
		if key is not None:
			return redirect('/admin/music', 301)

# public
api.add_resource(MusicList, '/main/music', endpoint='music_list')

# admin
api.add_resource(MusicList, '/admin/music', endpoint='admin_music_list')
api.add_resource(MusicCreate, '/admin/music/create', endpoint='music_create')
api.add_resource(MusicDetail, '/admin/music/<int:id>', endpoint='music_detail')
api.add_resource(MusicDelete, '/admin/music/delete/<int:id>', endpoint='music_delete')
