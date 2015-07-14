from base64 import b64encode
from flask import request, make_response, render_template
from flask.ext.restful import Resource
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from app.forms import PaintingCreateForm
from app.models import Painting
from app.painting_service import update_painting, get_painting
from main import api, auth

__author__ = 'Stretchhog'


class PaintingList(Resource):
	def get(self):
		paintings = Painting.query().order(-Painting.date_added).fetch()
		return make_response(
			render_template("paintings/list.html", title="Schilderijen", paintings=paintings))


class PaintingDelete(Resource):
	@auth.login_required
	def get(self, key):
		qry = Painting.query(Painting.key == key)
		qry.fetch(1)[0].delete()
		return redirect(api.url_for(PaintingList), 301)


class PaintingDetail(Resource):
	@auth.login_required
	def get(self, key):
		painting, form = get_painting(key)
		return make_response(render_template('paintings/detail.html', painting=painting, form=form))

	@auth.login_required
	def post(self):
		data = request.get_json()
		key = update_painting(data)
		if key is not None:
			return redirect(api.url_for(PaintingList), 301)


class PaintingCreate(Resource):
	@auth.login_required
	def get(self):
		form = PaintingCreateForm()
		return make_response(render_template('paintings/create.html', form=form))

	@auth.login_required
	def post(self):
		form = PaintingCreateForm(data=request.get_json())
		if form.validate():
			pass
		else:
			abort(400)
		painting = Painting()
		painting.title = form.title.data
		painting.notes = form.notes.data
		image = form.image.data
		painting.image = b64encode(image)
		painting.put()
		return redirect(api.url_for(PaintingList), 301)


api.add_resource(PaintingList, '/paintings', endpoint='paintings_list')
api.add_resource(PaintingCreate, '/admin/paintings/create', endpoint='painting_create')
api.add_resource(PaintingDetail, '/admin/paintings/<int:key>', endpoint='painting_detail')
api.add_resource(PaintingDelete, '/admin/paintings/delete/<int:key>', endpoint='painting_delete')
