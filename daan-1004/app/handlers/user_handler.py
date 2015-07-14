from flask.ext.login import login_required, current_user
from app.forms import UserCreateForm, LoginForm
from app.handlers.home_handler import Home
from flask import render_template, make_response, request
from flask.ext.restful import Resource
from werkzeug.utils import redirect
from app.services.user_service import login, logout
from main import api
from app.services import user_service as service


class Register(Resource):
	def get(self):
		return make_response(render_template("user/register.html", form=UserCreateForm()))

	def post(self):
		service.register_user(request.get_json())
		return redirect(api.url_for(Home))


class Login(Resource):
	def get(self):
		if current_user.is_authenticated():
			return redirect(api.url_for(Home))
		return make_response(render_template("user/login.html", form=LoginForm()))

	def post(self):
		return login(request.get_json())


class Logout(Resource):
	@login_required
	def get(self):
		return logout()


class BadRequest(Resource):
	def get(self):
		return make_response(render_template("500.html"))

# errors
api.add_resource(BadRequest, '/500', endpoint='bad_request')

# public pages
api.add_resource(Register, '/user/register', endpoint='register')
api.add_resource(Login, '/user/login', endpoint='login')
api.add_resource(Logout, '/user/logout', endpoint='logout')
