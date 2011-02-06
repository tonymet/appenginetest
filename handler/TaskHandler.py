from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import logging
from model.TaskModel import *
class TaskHandler(webapp.RequestHandler):
	def get(self):
		ts = TaskModel.all()
		logging.debug("received a %s response" % self.__class__)
		self.response.out.write(template.render('template/task.html', {'tasks': ts}))

	def post(self):
		t = TaskModel(name = self.request.get('name'), status=self.request.get('status'), owner=self.request.get('owner'))
		t.put()
		self.redirect('/task');

		

class CommentHandler(webapp.RequestHandler):
	def get(self):
		logging.debug("received a %s response" % self.__class__)
		print "hello commenter"
