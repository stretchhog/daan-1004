from google.appengine.ext import ndb


class Painting(ndb.Model):
	title = ndb.StringProperty()
	blob_key = ndb.BlobKeyProperty()
	notes = ndb.StringProperty()
	date_added = ndb.DateTimeProperty(auto_now_add=True)


class Music(ndb.Model):
	title = ndb.StringProperty()
	url = ndb.StringProperty()
	notes = ndb.StringProperty()
	date_added = ndb.DateTimeProperty(auto_now_add=True)
