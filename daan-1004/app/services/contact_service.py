from app.forms import ContactForm
from werkzeug.exceptions import abort
from google.appengine.api import mail
from google.appengine.api import users

__author__ = 'tvancann'


def send_email(data):
	form = ContactForm(data=data)
	if form.validate():
		pass
	else:
		return form

	message = mail.EmailMessage()
	message.sender = "d_lebens@hotmail.com"
	message.to = "d_lebens@hotmail.com"
	message.subject = "Bericht van daanlebens.com"
	message.body = """
AFZENDER:
%s
%s
%s

BERICHT:
%s
	""" % (form.name.data, form.email.data, form.phone.data, form.message.data)

	message.send()
	return None
