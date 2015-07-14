from flask import make_response
from flask import render_template
from flask.ext.restful import Resource
from main import api

__author__ = 'Stretchhog'

class Home(Resource):
	def get(self):
		return make_response(render_template("home.html"))

api.add_resource(Home, '/', endpoint='home')
