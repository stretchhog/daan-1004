from google.appengine.ext import ndb


class Painting(ndb.Model):
	title = ndb.IntegerProperty()
	image = ndb.BlobProperty()
	notes = ndb.StringProperty()
	date_added = ndb.DateTimeProperty(auto_now_add=True)
