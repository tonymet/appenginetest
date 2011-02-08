# routes for the app
from handler.TaskHandler import *
class Routes:
	def __init__(self):
		self.routes =[
				('/', MainHandler), 
				('/task', TaskListHandler), 
				(r'/task/(\d+)', TaskHandler), 
				('/comment', CommentHandler)
		]
