from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from model.TaskModel import TaskModel

# First, define a model class

# Now define a form class
class TaskForm(djangoforms.ModelForm):
  class Meta:
	model = TaskModel
