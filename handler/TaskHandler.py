from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import logging
from model.TaskModel import *
from form.taskform import TaskForm


class MainHandler(webapp.RequestHandler):
	def get(self):
		logging.debug("received a %s response" % self.__class__)
		ts = TaskModel.all()

class TaskListHandler(webapp.RequestHandler):
	def get(self):
		ts = TaskModel.all()
		logging.debug("received a %s response" % self.__class__)
		tf = TaskForm()
		from google.appengine.api import users
		self.response.out.write(template.render('template/task.html', {'tasks': ts, 'form': tf.as_ul()}))

	def post(self):
		tf = TaskForm(self.request.params)
		t = tf.save()
		t.put()
		self.redirect('/task');

class TaskHandler(webapp.RequestHandler):
	def get(self, groups):
		print groups
		

class CommentHandler(webapp.RequestHandler):
	def get(self):
		logging.debug("received a %s response" % self.__class__)
		print "hello commenter"
