import webapp2
from model.TaskModel import *
import logging
from routes import Routes

class NotFoundHandler(webapp2.RequestHandler):
	def get(self):
		self.error(404)
		return

def main():
	logging.getLogger().setLevel(logging.DEBUG)
	r = Routes()
	application = webapp2.WSGIApplication([('.*', NotFoundHandler)],
										 debug=True)
	application.run()

if __name__ == '__main__':
	main()
