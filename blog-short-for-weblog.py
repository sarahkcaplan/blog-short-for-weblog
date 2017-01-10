import os

import jinja2
import webapp2

import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.write(*a, **kw)

  def render(self, template, **kw):
    self.write(template, **kw))

class SignUp(Handler):
  def get(self):
    items = self.request.get_all("food")
    self.render("signup.html", items = items)

class Welcome(webapp2.RequestHandler):
  def get(self):
  self.render("welcome.html", username = username)


app = webapp2.WSGIApplication([
        ('/', SignUp),
        ('/welcome', Welcome)
        ],
        debug=True)

# import webapp2
# import cgi

# form="""
# <form method ="post">
# 	What is your birthday
# 	<br>
# 	<label>
# 		Month
# 		<input type="text" name="month" value="%(month)s">
# 	</label>
# 	<label>
# 		Day
# 		<input type="text" name="day" value="%(day)s">
# 	</label>
# 	<label>
# 		Year
# 		<input type="text" name="year" value="%(year)s">
# 	</label>
# 	<div style="color: red">%(error)s</div>
# 	<br>
# 	<br>
# 	<input type="submit">
# </form>
# """
# def escape_html(s):
#   return cgi.escape(s, quote = True)

# class MainPage(webapp2.RequestHandler):
#     def write_form(self, error="", month="", day="", year=""):
#     	self.response.write(form % {"error" : error,
#     								"month" : escape_html(month),
#     								"day": escape_html(day),
#     								"year": escape_html(year)})

#     def get(self):
#         # self.response.headers['Content-Type'] = 'text/plain'
#         self.write_form()

#     def post(self):
#     	user_month = self.request.get('month')
#     	user_day = self.request.get('day')
#     	user_year = self.request.get('year')

#     	month = valid_month(user_month)
#     	day = valid_day(user_day)
#     	year = valid_year(user_year)

#     	if not (month and day and year):
#     		self.write_form("That does not look like a valid date.", user_month, user_day, user_year)
#     	else:
#     		self.redirect("/thanks")

# class ThanksHandler(webapp2.RequestHandler):
#   def get (self):
#       self.response.write("Thank you!")

# # class TestHandler(webapp2.RequestHandler):
# # 	def post(self):
# # 		q = self.request.get("q")
# # 		self.response.write(q)

# months = ['January',
#           'February',
#           'March',
#           'April',
#           'May',
#           'June',
#           'July',
#           'August',
#           'September',
#           'October',
#           'November',
#           'December']

# month_abbvs = dict((m[:3].lower(),m) for m in months)
# def valid_month(month):
# 	if month:
# 		cap_month = month.capitalize()
# 		if cap_month in months:
# 			return cap_month

# def valid_day(day):
# 	if day and day.isdigit():
# 		day = int(day)
# 		if day > 0 and day <= 31:
# 			return day

# def valid_year(year):
# 	if year and year.isdigit():
# 		year = int(year)
# 		if year >1900 and year <2020:
# 			return year

# app = webapp2.WSGIApplication([
#     ('/', MainPage),
#     ('/thanks', ThanksHandler)
#     # ('/testform', TestHandler)
# ], debug=True)
