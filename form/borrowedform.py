from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from model.TaskModel import BorrowedModel

# First, define a model class

# Now define a form class
class BorrowedForm(djangoforms.ModelForm):
  class Meta:
	model = BorrowedModel
