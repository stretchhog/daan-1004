from google.appengine.ext import ndb
from flask import jsonify


class Painting(ndb.Model):
	title = ndb.IntegerProperty()
	image = ndb.BlobProperty()
	notes = ndb.StringProperty()
	date_added = ndb.DateTimeProperty(auto_now_add=True)


class User(ndb.Model):
	user = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.user
