# render crud for any model
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class GenericHelper:
	def __init__(self, model):
		self.model = model

	def list(self):
		template_values = {}
		template_values['keys'] = [p for p in properties(self.model) ]
		return template.render('template/partial/list.html', template_values)

	
	def form(self):
		pass
