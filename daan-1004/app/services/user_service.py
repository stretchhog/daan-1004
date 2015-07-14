import logging
from google.appengine.ext import ndb
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import UserCreateForm, LoginForm
from app.models import User
from app.serializers import entity_from_dict
from main import login_manager
from google.appengine.api.logservice import logservice

__author__ = 'Stretchhog'


@login_manager.user_loader
def load_user(user_key):
	key = entity_from_dict(User, user_key)
	fetch = User.query(User.user == key.user and User.password == key.password).fetch(1)
	if len(fetch) == 1:
		return fetch[0]
	else:
		return None


def check_password(user_password, provided_password):
	return check_password_hash(user_password, provided_password)


def hash_password(password):
	return generate_password_hash(password)


def register_user(data):
	form = UserCreateForm(data=data)
	user = User()
	user.user = form.user.data
	user.password = hash_password(form.password.data)
	return user.put()


def login(data):
	form = LoginForm()
	if not form.validate_on_submit():
		return form.errors, 422

	res = User.query(User.user is form.user.data).fetch(0)
