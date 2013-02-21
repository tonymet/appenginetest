import datetime
from google.appengine.ext import db
from model.Facebook import Facebook

class TaskModel(db.Model):
	STATUS_IN_PROGRESS=0x01
	STATUS_NEW=0x02
	STATUS_COMPLETE=0x04

	name = db.StringProperty(required=True)
	due_date = db.DateTimeProperty()
	progress = db.IntegerProperty()
	estimate = db.IntegerProperty()
	status = db.IntegerProperty(required=False, choices=set([STATUS_IN_PROGRESS, STATUS_NEW, STATUS_COMPLETE]) )
	owner_id = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now = True)

	@property
	def status_message(self):
		if(self.status == self.STATUS_IN_PROGRESS):
			return "In Progress"
		elif(self.status == self.STATUS_COMPLETE):
			return "Complete"
		elif(self.status == self.STATUS_NEW):
			return "New"
		return None
	
class CommentModel(db.Model):
	task = db.ReferenceProperty(TaskModel, collection_name="comments")
	created = db.DateTimeProperty(auto_now_add = True)
	content = db.StringProperty(required=True)

class UserModel(db.Model):
	user_id = db.StringProperty(required=True)
	access_token = db.StringProperty()
	name = db.StringProperty(required=True)
	picture = db.StringProperty(required=True)
	email = db.StringProperty()
	friends = db.StringListProperty()
	dirty = db.BooleanProperty()


	def refresh_data(self):
		"""Refresh this user's data using the Facebook Graph API"""
		me = Facebook().api(u'/me',
			{u'fields': u'picture,friends', u'access_token': self.access_token})
		self.dirty = False
		self.name = me[u'name']
		self.email = me.get(u'email')
		self.picture = me[u'picture'][u'url']
		self.friends = [user[u'id'] for user in me[u'friends'][u'data']]
		return self.put()

	@staticmethod
	def from_facebook(facebook, id):
		me = facebook.api(u'/%s' % id, {'fields':'first_name,last_name,email,picture,name'})
		user = UserModel(key_name=me['id'],
			user_id=me['id'],
			name=me[u'name'],
			email=me.get(u'email'),  # optional
			picture=me[u'picture'][u'data'][u'url'],
			)
		return user

class BorrowedModel(db.Model):
	STATUS_BORROWED=0x0
	STATUS_RETURNED=0x01

	borrower = db.ReferenceProperty(UserModel,required = True, collection_name="borrowed_items")
	lender = db.ReferenceProperty(UserModel,required = True, collection_name="lent_items")
	title = db.StringProperty(required = True)
	when = db.DateTimeProperty(auto_now_add=True)
	picture = db.StringProperty()
	due = db.DateTimeProperty()
	status = db.IntegerProperty(default = STATUS_BORROWED, choices=set([STATUS_BORROWED, STATUS_RETURNED]) )

	@property
	def status_message(self):
		if(self.status == self.STATUS_BORROWED):
			return "Borrowed"
		elif(self.status == self.STATUS_RETURNED):
			return "Returned"
		return None
