# routes for the app
from handler.TaskHandler import *
class Routes:
	def __init__(self):
		self.routes =[
				('/', TaskListHandler), 
				('/task', TaskListHandler), 
				(r'/task/([a-zA-Z0-9]+)', TaskHandler), 
				('/comment', CommentHandler)
		]
