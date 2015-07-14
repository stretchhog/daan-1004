from flask.ext.login import login_user, logout_user, login_required, user_logged_in, current_user
from app.forms import UserCreateForm, LoginForm
from app.handlers.home_handler import Home
from app.models import User
from flask import render_template, make_response, request, flash
from flask.ext.restful import Resource
from werkzeug.utils import redirect
from main import api, login_manager
from app.services import user_service as service
import logging
from google.appengine.api.logservice import logservice


class Register(Resource):
	def get(self):
		return make_response(render_template("user/register.html", form=UserCreateForm()))

	def post(self):
		print "JSON:", request.get_json()
		service.register_user(request.get_json())
		return redirect(api.url_for(Home))


class Login(Resource):
	def get(self):
		if current_user.is_authenticated():
			return redirect(api.url_for(Home))
		return make_response(render_template("user/login.html", form=LoginForm()))

	def post(self):
		error = None
		data = request.get_json()
		form = LoginForm(data=data)
		if form.validate_on_submit():
			res = User.query(User.user == form.user.data).fetch(1)
			if len(res) == 1 and res[0].password == form.password.data:
				user = res[0]
				login_user(user)
				flash('You were logged in')
				return redirect(api.url_for(Home))
			else:
				error = 'Invalid credentials. Please try again.'
		return make_response(render_template('user/login.html', form=form, error=error))


class Logout(Resource):
	@login_required
	def get(self):
		logout_user()
		flash('You were logged out.')
		return redirect(api.url_for(Home))


class BadRequest(Resource):
	def get(self):
		return make_response(render_template("500.html"))

# errors
api.add_resource(BadRequest, '/500', endpoint='bad_request')

# public pages
api.add_resource(Register, '/user/register', endpoint='register')
api.add_resource(Login, '/user/login', endpoint='login')
api.add_resource(Logout, '/user/logout', endpoint='logout')
