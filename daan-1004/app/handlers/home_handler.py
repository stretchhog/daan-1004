from google.appengine.api import users

from flask import render_template, redirect, make_response
from flask.ext.restful import Resource
from main import api


__author__ = 'Stretchhog'


class Root(Resource):
	def get(self):
		return redirect(api.url_for(Home))


class Home(Resource):
	def get(self):
		return make_response(render_template("home.html"))


class Login(Resource):
	def get(self):
		return redirect(users.create_login_url(dest_url='/main/home'))


class Logout(Resource):
	def get(self):
		return redirect(users.create_logout_url(dest_url='/main/home'))


api.add_resource(Root, '/', endpoint='root')
api.add_resource(Home, '/main/home', endpoint='home')

api.add_resource(Login, '/main/login', endpoint='login')
api.add_resource(Logout, '/admin/logout', endpoint='logout')
