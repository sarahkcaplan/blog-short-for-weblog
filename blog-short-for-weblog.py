import os
import jinja2
import webapp2
import cgi
import re

# Methods for developing with Google Datastore
from google.appengine.ext import db

# File paths for pointing to HTML Templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

#Envoking Jinja2
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#### Begin blog code

# Google Datastore entities i.e. db tables
class Article(db.Model):
  title = db.StringProperty(required = True)
  body = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)

# Commonly used functions
class BaseHandler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

# Home page of blog display 10 latest entries
class Home(BaseHandler):
  def get(self, title="", body=""):
    articles = db.GqlQuery("SELECT * FROM Article ORDER BY created DESC LIMIT 10")
    self.render("home.html", title=title, body=body, articles=articles)

# Page for creating new posts. Successful post redirects to post's permalink location.
class newPost(BaseHandler):
  def render_new(self, title="", body="", error=""):
    self.render("newpost.html", title=title, body=body, error=error)
    pass

  def get(self):
    self.render_new()

  def post(self):
    title = self.request.get("title")
    body = self.request.get("body")

    if title and body:
      article = Article(title = title, body=body)
      article.put()
      article_id = key.id()
      self.redirect("/<article_id>")
    else:
      error = "we need both a title and some text!"
      self.render_new(title, body, error = error)

# Handler for post's pages. Creates permalink.
class Post(BaseHandler):
  def get(self):
    article = db.GqlQuery("SELECT * FROM Article WHERE ID = article_id")
    self.render("post.html", title, body, article)

# class SignUp(BaseHandler):
#   def get(self):
#     self.render("signup.html")
#     # username = val_un
#     # password = val_pw
#     # email = val_em
#    #  self.render('signup.html', username = username, password = password, verify = verify, email = email)

#   def post(self):
#     user_username = self.request.get('username')
#     self.valid_username(user_username)
#     # user_password = self.request.get('password')
#     # user_verify = self.request.get('verify')
#     # user_email = self.request.get('email')

#   def valid_username(user_username):
#     if USER_RE.match(user_username):
#       username = user_username
#     else:
#       get("signup.html", username = user_username)
#       self.write(error_username)

#   def complete():
#     if(username, password, email):
#       self.redirect("/thanks")

# class Welcome(BaseHandler):
#   def get(self):
#     self.render("welcome.html")


# URI to Handler mapping
app = webapp2.WSGIApplication([
  ('/', Home),
  ('/newpost', newPost ),
  ('/<article_id>', Post)
  # ('/welcome', Welcome)
  ],
  debug=True)


