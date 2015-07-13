from google.appengine.ext import ndb
from passlib.apps import custom_app_context as pwd_context


class Painting(ndb.Model):
	title = ndb.IntegerProperty()
	image = ndb.BlobProperty()
	notes = ndb.StringProperty()
	date_added = ndb.DateTimeProperty(auto_now_add=True)
