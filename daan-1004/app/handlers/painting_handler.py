from google.appengine.ext import blobstore
from google.appengine.ext.webapp.blobstore_handlers import BlobstoreUploadHandler

from flask import request, make_response, render_template, redirect
from flask.ext.restful import Resource
from app.forms import PaintingCreateForm
from app.services import painting_service as service
from main import api
from werkzeug.http import parse_options_header


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
			f = request.files['file']
			header = f.headers['Content-Type']
			parsed_header = parse_options_header(header)
			blob_key = parsed_header[1]['blob-key']
			service.create_painting(request.get_json(), blob_key)

			return redirect(api.url_for(PaintingList), 301)

		except():
			return self.redirect('/admin/paintings/failure')


class PaintingFailure(Resource):
	def get(self):
		return make_response(render_template('paintings/failure.html'))

# public
api.add_resource(PaintingList, '/main/paintings', endpoint='paintings')

# admin
api.add_resource(PaintingCreate, '/admin/paintings/create', endpoint='painting_create')
api.add_resource(PaintingFailure, '/admin/paintings/failure', endpoint='painting_failure')
api.add_resource(PaintingDetail, '/admin/paintings/<int:id>', endpoint='painting_detail')
api.add_resource(PaintingDelete, '/admin/paintings/delete/<int:id>', endpoint='painting_delete')
api.add_resource(PhotoUploadHandler, '/admin/upload', endpoint='painting_upload')
