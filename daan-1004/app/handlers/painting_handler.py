from google.appengine.ext import blobstore
from google.appengine.ext.webapp.blobstore_handlers import BlobstoreUploadHandler
from flask import request, make_response, render_template, redirect
from flask.ext.restful import Resource

from app.forms import PaintingCreateForm
from app.services import painting_service as service
from main import api, app
from app.models import Painting

__author__ = 'Stretchhog'


class PaintingList(Resource):
	def get(self):
		paintings, images = service.get_paintings()
		return make_response(
			render_template("paintings/list.html", title="Schilderijen", entries=zip(paintings, images)))


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
		return make_response(render_template('paintings/create.html', form=form,
		                                     upload_url=blobstore.create_upload_url('/admin/upload')))


class PhotoUploadHandler(Resource, BlobstoreUploadHandler):
	def post(self):
		try:
			upload = self.get_uploads()[0]
			form = PaintingCreateForm(data=request.get_json())
			painting = Painting(title=form.title.data, blob_key=upload.key(), notes=form.notes.data)
			painting.put()

			redirect('/admin/paintings/list')

		except():
			print 's'
			redirect('/admin/paintings/list')

# public
api.add_resource(PaintingList, '/main/paintings', endpoint='paintings')

# admin
api.add_resource(PaintingList, '/admin/paintings', endpoint='admin_paintings')
api.add_resource(PaintingCreate, '/admin/paintings/create', endpoint='painting_create')
api.add_resource(PaintingDetail, '/admin/paintings/<int:id>', endpoint='painting_detail')
api.add_resource(PaintingDelete, '/admin/paintings/delete/<int:id>', endpoint='painting_delete')
api.add_resource(PhotoUploadHandler, '/admin/upload', endpoint='painting_upload')
