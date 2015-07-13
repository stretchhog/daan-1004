from google.appengine.ext import ndb
from wtforms_components import Email


class Painting(ndb.Model):
	title = ndb.IntegerProperty()
	image = ndb.BlobProperty()
	notes = ndb.StringProperty()
	date_added = ndb.DateTimeProperty(auto_now_add=True)


class User(ndb.Model):
	email = ndb.StringProperty(required=True, validator=Email())
	password = ndb.StringProperty(required=True)
