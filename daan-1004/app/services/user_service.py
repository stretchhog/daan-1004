from app.forms import UserCreateForm, LoginForm
from app.models import User
from main import login_manager

__author__ = 'Stretchhog'

@login_manager
def load_user(user_id):
	return User.query(User.key == user_id).fetch(1)[0]

def register_user(data):
	form = UserCreateForm()
	user = User()
	user.email = form.email.data
	user.password = form.password.data
	return user.put()

def login(data):
	form = LoginForm()
	if not form.validate_on_submit():
		return form.errors, 422

	res = User.query(User.email is form.email.data).fetch(0)
