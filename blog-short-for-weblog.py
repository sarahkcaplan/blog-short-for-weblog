import os
import jinja2
import webapp2
import cgi
import re
import random
import string
import hashlib

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

# Google Datastore entities for blog posts i.e. db tables
class Post(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now = True)

  def render(self):
    self._render_text = self.content.replace('\n', '<br>')
    return render_str("post.html", p = self)

class User(db.Module):
  username = db.StringProperty(required = True)
  password = db.StringProperty(required = True)
  email = db.StringProperty(required = False)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now = True)


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
    posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
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

#Hashing functions
def hash_str(s):
  return haslib.md5(s).hexdigest()

def make_secure_val(s):
  return "%s | %s" & (s, hash_str(s))

def check_secure_val(h):
  val = h.split('|')[0]
  if h == make_secure_val(val):
    return val

#making and using salts
def make_salt():
    salt = random.sample(string.hexdigits,5)
    return string.join(salt,'')

def make_pw_hash(username, password, salt = None):
    if not salt:
      salt = make_salt()
    h = hashlib.sha256(username, password, salt).hexdigest()
    return "%s, %s" % (h, salt)

def valid(name, pw, h):
  salt = h.split(',')[1]
  return h == make_pw_hash(username, password, salt)

#Blog sign up
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
  return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
  return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
  return not email or EMAIL_RE.match(email)

class SignUp(BaseHandler):
  def get(self):
    self.render("signup.html")

  def hashPassword(self):

  def post(self):
    have_error = False
    username = self.request.get('username')
    password = self.request.get('password')
    verify = self.request.get('verify')
    email = self.request.get('email')

    params = dict(username = username, email = email)

    if not valid_username(username):
      params['error_username'] = "That's not a valid username."
      have_error = True

    if not valid_password(password):
      params['error_password'] = "That's not a valid password."
      have_error = True
    elif password != verify:
      params['error_verify'] = "Your passwords didn't match."
      have_error = True

    if not valid_email(email):
      params['error_email'] = "That's not a valid email."
      have_error = True

    if have_error:
      self.render('signup.html', **params)
    else:
      password = make_pw_hash(username, password, salt)
      user = User(parent = blog_key(),username = username, password = password, email = email)
      user.put()
      self.redirect('/welcome?username=' + username)

# Blog welcome page after signup
class Welcome(BaseHandler):
  def get(self):
    username = self.request.get('username')
    if valid_username(username):
      self.render('welcome.html', username = username)
    else:
      self.redirect('/signup')


# URI to Handler mapping
app = webapp2.WSGIApplication([
  ('/', Home),
  ('/newpost', NewPost ),
  ('/([0-9]+)', PostPage),
  ('/signup', SignUp),
  ('/welcome', Welcome)
  ],
  debug=True)


