import logging
import sys
import traceback

from app.forms import ContactForm
from google.appengine.api import mail

__author__ = 'tvancann'


def send_email(data):
	form = ContactForm(data=data)
	if form.validate():
		pass
	else:
		return form

	message = mail.EmailMessage()
	message.sender = "dlebens1987@gmail.com"
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

	try:
		message.send()
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
		logging.error(''.join('!! ' + line for line in lines))
	finally:
		return None
