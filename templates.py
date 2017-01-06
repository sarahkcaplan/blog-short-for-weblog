import os

import webapp2

html ="""
<form>
<h2>Add a Food</h2>
<input type="text" name="food">
<button>Add</button>
</form>
"""

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

class MainPage(Handler):
	def get(self):
		self.write("Hello, Sarah!!!")

app = webapp2.WSGIApplication([
				('/', MainPage),
				],
				debug=True)