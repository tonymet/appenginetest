from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import logging
from model.TaskModel import *
from form.taskform import TaskForm


class BaseHandler(webapp.RequestHandler):
	def render(self, name, **template_data):
		self.response.out.write(template.render('template/%s.html' % name, template_data))

class MainHandler(BaseHandler):
	def get(self):
		logging.debug("received a %s response" % self.__class__)
		ts = TaskModel.all()

class TaskListHandler(BaseHandler):
	def get(self):
		ts = TaskModel.all()
		logging.debug("received a %s response" % self.__class__)
		tf = TaskForm()
		from google.appengine.api import users
		self.render('tasklist', tasks = ts, form =  tf)

	def post(self):
		tf = TaskForm(self.request.params)
		t = tf.save()
		t.put()
		self.redirect('/task');

class TaskHandler(BaseHandler):
	def get(self, key):
		task = TaskModel.get(key)
		tf = TaskForm()
		self.render('task', task = task, form = tf)
		

class CommentHandler(webapp.RequestHandler):
	def get(self):
		logging.debug("received a %s response" % self.__class__)
		print "hello commenter"
