import os
from google.appengine.api import users
from flask_restful import Api
from flask import Flask, render_template, make_response, redirect, session

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'

api = Api(app)
# import routes
from app.handlers import home_handler, painting_handler, music_handler, contact_handler, about_handler


@app.before_request
def before_request():
	user = users.get_current_user()
	if user:
		session['logged_in'] = True
		session['user_email'] = user.email()
		session['is_admin'] = users.is_current_user_admin()
	else:
		session['logged_in'] = False


@app.errorhandler(404)
def not_found(error):
	return make_response(render_template("404.html"))


@app.errorhandler(409)
def not_found(error):
	return make_response(render_template("409.html"))


@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
	return response
