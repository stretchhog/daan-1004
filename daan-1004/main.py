import os
from flask.ext.login import LoginManager

from flask_restful import Api
from flask import Flask, render_template, make_response
from app.models import User

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'

api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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

# import routes
from app.handlers import user_handler, home_handler, painting_handler

if __name__ == '__main__':
	app.run()
