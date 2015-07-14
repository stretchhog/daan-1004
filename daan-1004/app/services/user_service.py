import logging
from flask import make_response, render_template
from flask.ext.login import login_user, logout_user
from google.appengine.ext import ndb
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from app.forms import UserCreateForm, LoginForm
from app.handlers.home_handler import Home
from app.models import User
from app.serializers import entity_from_dict
from main import login_manager, api
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
	form = LoginForm(data=data)
	error = None
	if form.validate_on_submit():
		res = User.query(User.user == form.user.data).fetch(1)
		if len(res) == 1 and check_password(res[0].password, form.password.data):
			user = res[0]
			login_user(user)
			retval = redirect(api.url_for(Home))
		else:
			error = 'Invalid credentials. Please try again.'
			retval = make_response(render_template('user/login.html', form=form, error=error))
	else:
		retval = make_response(render_template('user/login.html', form=form, error=error))
	return retval

def logout():
	logout_user()
	return redirect(api.url_for(Home))
