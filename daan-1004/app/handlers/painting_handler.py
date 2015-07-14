from flask import request, make_response, render_template
from flask.ext.login import login_required
from flask.ext.restful import Resource
from werkzeug.utils import redirect

from app.forms import PaintingCreateForm
from app.services import painting_service as service
from main import api

__author__ = 'Stretchhog'


class PaintingList(Resource):
	def get(self):
		paintings = service.get_paintings()
		return make_response(
			render_template("paintings/list.html", title="Schilderijen", paintings=paintings))


class PaintingDelete(Resource):
	@login_required
	def get(self, key):
		service.delete_painting(key)
		return redirect(api.url_for(PaintingList), 301)


class PaintingDetail(Resource):
	@login_required
	def get(self, key):
		painting, form = service.get_painting(key)
		return make_response(render_template('paintings/detail.html', painting=painting, form=form))

	@login_required
	def post(self):
		key = service.update_painting(request.get_json())
		if key is not None:
			return redirect(api.url_for(PaintingList), 301)


class PaintingCreate(Resource):
	@login_required
	def get(self):
		form = PaintingCreateForm()
		return make_response(render_template('paintings/create.html', form=form))

	@login_required
	def post(self):
		key = service.create_painting(request.get_json())
		if key is not None:
			return redirect(api.url_for(PaintingList), 301)

# public
api.add_resource(PaintingList, '/paintings', endpoint='paintings_list')

# admin
api.add_resource(PaintingCreate, '/admin/paintings/create', endpoint='painting_create')
api.add_resource(PaintingDetail, '/admin/paintings/<int:key>', endpoint='painting_detail')
api.add_resource(PaintingDelete, '/admin/paintings/delete/<int:key>', endpoint='painting_delete')
