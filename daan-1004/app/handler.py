from marshmallow import Serializer
from app.forms import UserCreateForm, SessionCreateForm
from app.models import User
from flask import render_template, make_response, g
from flask.ext.restful import Resource
from main import api, auth


class UserSerializer(Serializer):
	class Meta:
		fields = ("key", "email")


class Register(Resource):
	def get(self):
		return make_response(render_template("register.html", form=UserCreateForm()))

	def post(self):
		form = UserCreateForm()
		user = User()
		user.email = form.email.data
		user.password = form.password.data
		user.put()
		return UserSerializer(user).data


class Login(Resource):
	def get(self):
		return make_response(render_template("login.html", form=SessionCreateForm()))

	def post(self):
		form = SessionCreateForm()
		if not form.validate_on_submit():
			return form.errors, 422

		res = User.query(User.email is form.email.data).fetch(0)
		if len(res) == 1:
			user = res[0]
			if user.password is form.password.data:
				return UserSerializer(user).data, 201
		return '', 401


@auth.verify_password
def verify_password(email, password):
	user = User.query(User.email == email).fetch()[0]
	if not user:
		return False
	g.user = user
	return user.password is password


class BadRequest(Resource):
	def get(self):
		return make_response(render_template("500.html"))

# errors
api.add_resource(BadRequest, '/500', endpoint='bad_request')

# public pages
api.add_resource(Register, '/users')
api.add_resource(Login, '/login')
