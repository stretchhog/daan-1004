import logging
from google.appengine.ext import ndb
from app.forms import UserCreateForm, LoginForm
from app.models import User
from main import login_manager
from google.appengine.api.logservice import logservice

__author__ = 'Stretchhog'


@login_manager.user_loader
def load_user(key):
	fetch = User.query(User.user == key).fetch(1)
	if len(fetch) == 1:
		return fetch[0]
	else:
		return None


def register_user(data):
	form = UserCreateForm(data=data)
	user = User()
	user.user = form.user.data
	user.password = form.password.data
	return user.put()


def login(data):
	form = LoginForm()
	if not form.validate_on_submit():
		return form.errors, 422

	res = User.query(User.user is form.user.data).fetch(0)
