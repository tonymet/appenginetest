from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import logging
from model.TaskModel import *
from model.Facebook import *
from form.taskform import TaskForm
from form.borrowedform import BorrowedForm
from handler.BaseHandler import BaseHandler


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
	
class BorrowedListHandler(BaseHandler):
	def get(self):
		try:
			borrowed_items = BorrowedModel.all()
			form = BorrowedForm()
		except db.BadKeyError:
			self.error(404)
			return
		self.render('borrowedlist', borrowed_items = borrowed_items, request = self.request, form=form)
	
	def post(self):
		if not self.facebook:
			raise Exception('facebook not initialized')
		bf = BorrowedForm(self.request.params)
		friend = UserModel.get_by_key_name(self.request.params['friend'])
		logging.debug('friend: %s' % self.request.params['friend'])
		if not friend:
			friend = UserModel.from_facebook(self.facebook, self.request.params['friend'])
			friend.put()
		if self.request.params['verb'] == 'lent':
			borrowed = BorrowedModel(borrower=friend, lender=self.user, title=self.request.params['title'])
		else:
			borrowed = BorrowedModel(borrower=self.user, lender=friend, title=self.request.params['title'])
		borrowed.put()
		self.redirect(self.request.path)
