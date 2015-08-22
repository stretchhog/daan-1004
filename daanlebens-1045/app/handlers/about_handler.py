from flask import make_response, render_template, request, redirect
from flask.ext.restful import Resource
from app.forms import GigForm
from main import api
from app.services import about_service as service

__author__ = 'tvancann'

class About(Resource):
	def get(self):
		gigs = service.get_all()
		return make_response(render_template("about/about.html", gigs=gigs))

class GigCreate(Resource):
	def get(self):
		form = GigForm()
		return make_response(render_template('about/create_gig.html', form=form))

	def post(self):
		key = service.create(request.get_json())
		if key is not None:
			return redirect(api.url_for(About), 301)

class GigDelete(Resource):
	def get(self, id):
		service.delete_by_id(id)
		return redirect(api.url_for(About), 301)

class GigDetail(Resource):
	def get(self, id):
		gig, form = service.get_by_id(id)
		return make_response(render_template('about/detail.html', gig=gig, form=form))

	def post(self, id):
		key = service.update_by_id(id, request.get_json())
		if key is not None:
			return redirect(api.url_for(About), 301)

# public
api.add_resource(About, '/main/about', endpoint='about')

# admin
api.add_resource(GigCreate, '/admin/about/create', endpoint='gig_create')
api.add_resource(GigDetail, '/admin/about/<int:id>', endpoint='gig_detail')
api.add_resource(GigDelete, '/admin/about/delete/<int:id>', endpoint='gig_delete')

