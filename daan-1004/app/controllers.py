from google.appengine.ext.webapp.util import login_required

from app.forms import PaintingCreateForm, PaintingEditForm
from app.models import Painting
from flask import request, render_template, make_response, redirect, send_file
from flask.ext.restful import Resource, abort
from main import api
from base64 import b64encode


class PaintingList(Resource):
	def get(self):
		paintings = Painting.query().order(-Painting.date_added).fetch()
		return make_response(
			render_template("paintings/list.html", title="Schilderijen", paintings=paintings, form=ComicCreateForm()))


@login_required
class PaintingDelete(Resource):
	def get(self, key):
		qry = Painting.query(Painting.key == key)
		qry.fetch(1)[0].delete()
		return redirect(api.url_for(PaintingList), 301)


@login_required
class PaintingDetail(Resource):
	def get(self, key):
		qry = Painting.query(Painting.key == key)
		painting = qry.fetch(1)[0]
		form = PaintingEditForm()
		form.title.data = painting.title
		form.notes.data = painting.notes
		form.key.data = painting.key
		return make_response(render_template('paintings/detail.html', painting=painting, form=form))

	def post(self):
		form = PaintingEditForm(data=request.get_json())
		qry = Painting.query(Painting.key == form.key.data)
		painting = qry.fetch(1)[0]
		painting.title = form.title.data
		painting.notes = form.notes.data
		painting.put()
		return redirect(api.url_for(PaintingList), 301)


@login_required
class PaintingCreate(Resource):
	def get(self):
		form = PaintingCreateForm(data=request.get_json())
		return make_response(render_template('paintings/create.html', form=form))

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


# public pages
api.add_resource(PaintingList, '/paintings/list', endpoint='comic_list')

# admin pages
api.add_resource(PaintingCreate, '/paintings/admin/create', endpoint='painting_create')
api.add_resource(PaintingDetail, '/paintings/admin/<int:key>', endpoint='painting_detail')
api.add_resource(PaintingDelete, '/paintings/admin/delete/<int:key>', endpoint='painting_delete')
