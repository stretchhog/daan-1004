from app.forms import PaintingCreateForm, PaintingEditForm
from app.models import Painting, User
from flask import request, render_template, make_response, redirect, g
from flask.ext.restful import Resource, abort
from base64 import b64encode
from main import api, auth


class PaintingList(Resource):
	def get(self):
		paintings = Painting.query().order(-Painting.date_added).fetch()
		return make_response(
			render_template("paintings/list.html", title="Schilderijen", paintings=paintings))


@auth.verify_password
def verify_password(email, password):
	user = User.query(User.email == email).fetch()[0]
	if not user:
		return False
	g.user = user
	return user.password is password


class PaintingDelete(Resource):
	@auth.login_required
	def get(self, key):
		qry = Painting.query(Painting.key == key)
		qry.fetch(1)[0].delete()
		return redirect(api.url_for(PaintingList), 301)


class PaintingDetail(Resource):
	@auth.login_required
	def get(self, key):
		qry = Painting.query(Painting.key == key)
		painting = qry.fetch(1)[0]
		form = PaintingEditForm()
		form.title.data = painting.title
		form.notes.data = painting.notes
		form.key.data = painting.key
		return make_response(render_template('paintings/detail.html', painting=painting, form=form))

	@auth.login_required
	def post(self):
		form = PaintingEditForm(data=request.get_json())
		qry = Painting.query(Painting.key == form.key.data)
		painting = qry.fetch(1)[0]
		painting.title = form.title.data
		painting.notes = form.notes.data
		painting.put()
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

# public pages
api.add_resource(PaintingList, '/paintings', endpoint='paintings_list')

# admin pages
api.add_resource(PaintingCreate, '/admin/paintings/create', endpoint='painting_create')
api.add_resource(PaintingDetail, '/admin/paintings/<int:key>', endpoint='painting_detail')
api.add_resource(PaintingDelete, '/admin/paintings/delete/<int:key>', endpoint='painting_delete')
