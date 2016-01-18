from flask import make_response, render_template, request
from flask.ext.restful import Resource
from app.services import contact_service as service
from app.forms import ContactForm
from main import api

__author__ = 'tvancann'


class Contact(Resource):
	def get(self):
		form = ContactForm()
		return make_response(render_template("contact.html", form=form))

	def post(self):
		form = service.send_email(request.get_json())
		if form is None:
			return make_response(render_template("email_send.html"))
		else:
			return make_response(render_template("contact.html", form=form))


class ContactAdmin(Resource):
	def get(self):
		form = ContactForm()
		return make_response(render_template("contact_admin.html", form=form))

	def post(self):
		form = service.send_email(request.get_json())
		if form is None:
			return make_response(render_template("email_send.html"))
		else:
			return make_response(render_template("contact_admin.html", form=form))

api.add_resource(Contact, '/main/contact', endpoint='contact')
api.add_resource(ContactAdmin, '/admin/contact', endpoint='contact_admin')
