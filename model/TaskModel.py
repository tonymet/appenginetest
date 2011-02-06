import datetime
from google.appengine.ext import db

class TaskModel(db.Model):
	name = db.StringProperty(required=True)
	due_date = db.DateTimeProperty()
	progress = db.IntegerProperty()
	estimate = db.IntegerProperty()
	status = db.StringProperty(required=False, choices=set(["new","assigned", "in_progress", "complete"]))
	owner = db.EmailProperty(required=True)
	created = db.DateTimeProperty()
	
class CommentModel(db.Model):
	task = db.ReferenceProperty(TaskModel)
	created = db.DateTimeProperty()
	content = db.StringProperty(required=True)
