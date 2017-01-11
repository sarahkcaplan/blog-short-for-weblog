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

def render_str(template, **params):
  t = jinja_env.get_template(template)
    return t.render(params)

# Commonly used functions
class BaseHandler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.write(*a, **kw)

  def render_str(self, template, **params):
    return render_str(template, **params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

#### Begin blog code

# Google Datastore entities for blog posts i.e. db table plus post formatting
class Post(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now = True)

  def render(self):
    self._render_text = self.content.replace('\n', '<br>')
    return render_str("post.html", p = self)

# Generic parent entity
def blog_key(name = 'default'):
  return db.Key.from_path('blogs', name)

# Blog post formatting
def render_post(response, post):
  response.write('<b>' + post.subject + '</b><br>')
  response.write(post.content)

# Home page of blog display 10 latest entries
class Home(BaseHandler):
  def get(self, title="", body=""):
    articles = db.GqlQuery("SELECT * FROM Article ORDER BY created DESC LIMIT 10")
    self.render("home.html", posts = posts)

# Page for creating new posts. Successful post redirects to post's permalink location.
class NewPost(BaseHandler):
  def get(self):
    self.render("newpost.html")

  def post(self):
    subject = self.request.get("subject")
    content = self.request.get("content")

    if subject and content:
      p = Post(parent = blog_key(), subject = subject, content = content)
      p.put()
      self.redirect("/%s" % str(p.key().id()))
    else:
      error = "we need both a title and some text!"
      self.render("newpost.html", subject = subject, content = content, error = error)

# Handler for post's pages. Defines post's db key for URI.
class PostPage(BaseHandler):
  def get(self, post_id):
    key = db.Key.from_path('Post', int(post_id), parent =blog_key())
    post = db.get(key)

    if not post:
      self.error(404)
      return

    self.render("post.html", post = post)

class SignUp(BaseHandler):
  def get(self):
    self.render("signup.html")
    # username = val_un
    # password = val_pw
    # email = val_em
   #  self.render('signup.html', username = username, password = password, verify = verify, email = email)

  def post(self):
    user_username = self.request.get('username')
    self.valid_username(user_username)
    # user_password = self.request.get('password')
    # user_verify = self.request.get('verify')
    # user_email = self.request.get('email')

  def valid_username(user_username):
    if USER_RE.match(user_username):
      username = user_username
    else:
      get("signup.html", username = user_username)
      self.write(error_username)

  def complete():
    if(username, password, email):
      self.redirect("/thanks")

class Welcome(BaseHandler):
  def get(self):
    self.render("welcome.html")


# URI to Handler mapping
app = webapp2.WSGIApplication([
  ('/', Home),
  ('/newpost', NewPost ),
  ('/([0-9]+)', PostPage)
  # ('/welcome', Welcome)
  ],
  debug=True)


