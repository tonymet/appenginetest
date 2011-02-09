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
		self.render('tasklist', tasks = ts, form =  tf, request=self.request)

	def post(self):
		tf = TaskForm(self.request.params)
		t = tf.save()
		t.put()
		self.redirect('/task');

class TaskHandler(BaseHandler):
	def get(self, key):
		tf = TaskForm()
		self.render('task', task = task, form = tf)
		

class CommentHandler(BaseHandler):
	def get(self, key):
		try:
			task = TaskModel.get(key)
		except db.BadKeyError:
			self.error(404)
			return
		self.render('commentlist', task = task, comments=task.comments, request = self.request)
	
	def post(self, key):
		task = TaskModel.get(self.request.get('task_key'))
		comment = CommentModel(task=task, content = self.request.get('content'))
		comment.put()
		self.redirect(self.request.url)
