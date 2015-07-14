from flask import make_response
from flask import render_template
from flask.ext.restful import Resource
from main import api
from flask.ext.login import login_user, logout_user, login_required, user_logged_in, current_user

__author__ = 'Stretchhog'

class Home(Resource):
	def get(self):
		return make_response(render_template("home.html"))

api.add_resource(Home, '/', endpoint='home')
