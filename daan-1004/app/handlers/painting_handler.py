from flask import request, make_response, render_template, redirect
from flask.ext.restful import Resource

from app.forms import PaintingCreateForm
from app.services import painting_service as service
from main import api

__author__ = 'Stretchhog'


class PaintingList(Resource):
	def get(self):
		paintings = service.get_paintings()
		return make_response(render_template("paintings/list.html", title="Schilderijen", paintings=paintings))


class PaintingDelete(Resource):
	def get(self, id):
		service.delete_painting(id)
		return redirect(api.url_for(PaintingList), 301)


class PaintingDetail(Resource):
	def get(self, id):
		painting, form = service.get_painting(id)
		return make_response(render_template('paintings/detail.html', painting=painting, form=form))

	def post(self, id):
		key = service.update_painting(id, request.get_json())
		if key is not None:
			return redirect(api.url_for(PaintingList), 301)


class PaintingCreate(Resource):
	def get(self):
		form = PaintingCreateForm()
		return make_response(render_template('paintings/create.html', form=form))

	def post(self):
		files = request.files
		key = service.create_painting(request.get_json(), files.get('image'))
		if key is not None:
			return redirect(api.url_for(PaintingList), 301)

# public
api.add_resource(PaintingList, '/main/paintings', endpoint='paintings_list')

# admin
api.add_resource(PaintingList, '/admin/paintings', endpoint='admin_paintings_list')
api.add_resource(PaintingCreate, '/admin/paintings/create', endpoint='painting_create')
api.add_resource(PaintingDetail, '/admin/paintings/<int:id>', endpoint='painting_detail')
api.add_resource(PaintingDelete, '/admin/paintings/delete/<int:id>', endpoint='painting_delete')
