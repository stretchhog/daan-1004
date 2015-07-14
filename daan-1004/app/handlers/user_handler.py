from flask.ext.login import login_user, logout_user, login_required
from marshmallow import Serializer
from app.forms import UserCreateForm, LoginForm
from app.handlers.home_handler import Home
from app.models import User
from flask import render_template, make_response, request, flash
from flask.ext.restful import Resource
from werkzeug.utils import redirect
from main import api
from app.services import user_service as service


class UserSerializer(Serializer):
	class Meta:
		fields = ("key", "email")


class Register(Resource):
	def get(self):
		return make_response(render_template("user/register.html", form=UserCreateForm()))

	def post(self):
		service.register_user(request.get_json())


class Login(Resource):
	def get(self):
		return make_response(render_template("user/login.html", form=LoginForm()))

	def post(self):
		error = None
		data = request.get_json()
		form = LoginForm(data=data)
		if form.validate_on_submit():
			res = User.query(User.email == form.email.data).fetch(0)
			if len(res) == 1 and res[0].password is form.password.data:
				user = res[0]
				login_user(user)
				flash('You were logged in')
				return redirect(api.url_for(Home))
			else:
				error = 'Invalid credentials. Please try again.'
		return make_response(render_template('user/login.html', form=form, error=error))


@login_required
class Logout(Resource):
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
api.add_resource(Register, '/users', endpoint='register')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
