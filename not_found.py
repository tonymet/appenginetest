from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from model.TaskModel import *
import logging
from routes import Routes

class NotFoundHandler(webapp.RequestHandler):
	def get(self):
		self.error(404)
		return

def main():
	logging.getLogger().setLevel(logging.DEBUG)
	r = Routes()
	application = webapp.WSGIApplication([('.*', NotFoundHandler)],
										 debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
