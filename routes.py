# routes for the app
from handler.TaskHandler import *
class Routes:
	def __init__(self):
		self.routes =[
				('/', BorrowedListHandler), 
				('/task', TaskListHandler), 
				(r'/task/([a-zA-Z0-9]+)', CommentHandler), 
				(r'/borrowed', BorrowedListHandler), 
		]
