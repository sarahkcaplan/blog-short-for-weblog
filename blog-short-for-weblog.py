import os
import jinja2
import webapp2
import cgi
import re
import random
import string
import hashlib
import hmac

# Importing db module from Google App Engine
# db supplies methods for developing with Google Datastore
from google.appengine.ext import db


# Sets variable "template_dir" to the pathname for the
# folder called "templates" by calling
# path.join and passing in the folder name "templates"
# When refactoring, can the os.path.join be replaced with
# jinja2.join_path?
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

# Sets variable "jinja_env" by calling Environment with the parameters
# "loader" and "autoescape". "Loader" is set to be what is returned when calling FileSystemLoader.
# When FileSystemLoader is called, the parameter "template_dir" is passed to it
# The variable "template_dir" comes from being defined above (as a gloabl variable?).
# The value for the parameter "autoescape" is also pre-defined to "true"; no values
# are passed to "loader" or "autoescape" as arguments when the function is called.
# This creates an instance of the Jinja Environment (class)
# The "Environment" is the core component of Jinja
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

secret = "evernote"

# Takes two parameters, including one keyword parameter.
# The function sets the variable "t" to what is returned
# when "get_templates" is called with the parameter "template".
# Then the function returns the result of rendering "t" with the
# keyword parameters "params".
# ... after reading documentation
# "t" is a new Template object.
# This is a template loader.
def render_str(template, **params):
  t = jinja_env.get_template(template)
  return t.render(params)

## Commonly used functions

# The class "BaseHandler" is-a "webapp2.RequestHandler"
# The class has eight functions definied within it
class BaseHandler(webapp2.RequestHandler):

# Class "BaseHandler" has-a function named "write"
# that takes "self"; multiple, optional arguments; multiple,
# optional keywords as parameters.
# The function calls "response" and "write" on "self".
# This writes out the response to either GET or POST method
# From WebApp "The method sets properties on self.response to prepare the response, then exits."
  def write(self, *a, **kw):
    self.response.write(*a, **kw)

# Class "BaseHandler" has-a function named "render_str" that takes
# "self", "template", and "**params" as parameters.
# The function calls the function "global_render_str" which has two
# parameters, "template" and "**params". By calling "global_render_str",
# this function brings that function into the BaseHandler (??)
  def render_str(self, template, **params):
    return render_str(template, **params)

# Function within BaseHandler class to "write out"
# the template called using GET method. In the handlers below where GET functionality
# is definied, the name of the template is given as an argument
  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

  def set_secure_cookie(self, name, val):
    cookie_val = make_secure_val(val)
    self.response.headers.add_header(
      'Set-Cookie',
      '%s=%s ; Path =/' % (name, cookie_val))

  def read_secure_cookie(self, name):
    cookie_val = self.request.cookies.get(name)
    return cookie_val and check_secure_val(cookie_val)

  def login(self, user):
    self.set_secure_cookie('user_id', str(user.key().id()))

  def logout(self):
    self.response.headers.add_header('Set-Cookie', 'user_id=; Path/')

# Class BaseHandler has-a __init__ that takes self; multiple, optional
# parameters; and multiple, optional keywords.
# First, the function calls initialize on RequestHandler; this function takes
# self; multiple, optional parameters; and multiple, optional keywords.
# Second, the function "read_secure_cookie" is called and it has
# "user_id" string set as the argument passed for the "name" parameter.
# The results of this function being called are assigned to the variable "uid".
# Finally, from "self" get the "user" attirbute and set it to the variable
# "uid" and set it to the "by_id" function (from the "User" class) and call
# it with parameter "uid"
# ?? Why doesn't "read_secure_cookie" need an explicit "self" argument
# ?? passed to it when it's called. Is it because it takes/assumes the "self"
# ?? being accessed here is the "self" it needs?
# ?? Where does the "user" attribute come from?
# ?? What does it mean to set the attribute to something?
# ?? Does the second uid override the first?
# ?? What does setting self.user to uid do?
# After reading some documentation...
# "uid = self.read_secure_cookie..." is creating a new "uid object" with the unique cookie
# for that user's 'user_id', also called 'name' in "set_secure_cookie" and "read_secure_cookie"

  def initialize(self, *a, **kw):
    webapp2.RequestHandler.initialize(self, *a, **kw)
    uid = self.read_secure_cookie('user_id')
    self.user = uid and User.by_id(uid)

#### Begin blog code

# Google Datastore entities for blog posts i.e. db tables
class Post(db.Model):
  # author = db.StringProperty(required = True)
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now = True)
  liked_by = db.ListProperty(int)

# ?? "p = self": What keyword is p? And why is it set to self?
# ?? What does setting it to self do?
  def render(self):
    self._render_text = self.content.replace('\n', '<br>')
    return render_str("post.html", p = self)

class Photo(db.Model):
  title = db.StringProperty(required = True)
  last_modified = db.DateTimeProperty(auto_now_add = True)

class User(db.Model):
  name = db.StringProperty(required = True)
  pw_hash = db.StringProperty(required = True)
  email = db.StringProperty(required = False)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now = True)


class Comment(db.Model):
  # author = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  last_modified = db.DateTimeProperty(auto_now_add = True)

# This is a decorator. ??What's a decorator?
# It gets users from the database by their id.
# I think uid is the user's id as it's read/verified through
# the secure cookie.
# The User entity has a parent key called "users_key"
# So this returns the entry for the user of a particular
# id?
# ?? What's cls?
  @classmethod
  def by_id(cls, uid):
    return user.get_by_id(uid, parent = users_key())

# This returns the db entry for a user by name
  @classmethod
  def by_name(cls, name):
    u = cls.all().filter("name =", name).get()
    return u

# This registers the user ??by making an new entry
# in the User entity?? meanwhile it hashes the user's
# password so that just the hash is stored, not plain
# text pw
  @classmethod
  def register(cls, name, pw, email = None):
    pw_hash = make_pw_hash(name, pw)
    return cls(parent = users_key(),
            name = name,
            pw_hash = pw_hash,
            email = email)

# This returns the username if the user is logged in.
# A user is logged in if 1) there is a user by that username
# 2) that user has a valid password
  @classmethod
  def login(cls, name, pw):
    u = cls.by_name(name)
    if u and valid_pw(name, pw, u.pw_hash):
      return u


# TODO: Put this with their respective entities
# Might want posts and comments to have same parent
# Generic parent entities
# Returns a newly built Key object from the ancestor path.
# Returns the kind "blog" ??and the identifier "name"??
# ?? I think the ancestory is key/value pairs?
# I believe this creates the parent key and assigns it to
# "blog_key". I think it creates the parent key without creating an
# entity for a parent.
def blog_key(name = 'default'):
  return db.Key.from_path('blogs', name)

def users_key(group = 'default'):
  return db.Key.from_path('users', group)

# Blog post formatting
def render_post(response, post):
  response.write('<b>' + post.subject + '</b><br>')
  response.write(post.content)

# Home page of blog display 10 latest entries
# Request Handler for the Home ("/") page.
# On GET request, the function queries all posts
# and orders them with newest on top then sets the results
# of the query to variable "post"
# Response to GET request is "home.html" template rendered
# with queried posts as keyword argument

class Home(BaseHandler):
  def get(self):
    if self.user:
      posts = db.GqlQuery("SELECT * FROM Post ORDER BY last_modified DESC LIMIT 10")
      self.render("home.html", posts = posts)
    else:
      self.redirect("/signup")

# Page for creating new posts. Successful post redirects to post's permalink location.

class NewPost(BaseHandler):
  def get(self):
    if self.user:
      self.render("newpost.html")
    else:
      self.redirect("/signup")

# "self.request.get" is how the POST method gets the form data (using Webapp2/GAE)
# In particular it gets the data for "subject" and "content"
# "p = Post..." is creating a new Post object.
# "We are creating this object with the model constructor"
  def post(self):
    subject = self.request.get("subject")
    content = self.request.get("content")
    liked_by = int(self.request.cookies.get("user_id"))

    if subject and content:
      # This is invoking a model class constructor using keyword arguments
      p = Post(parent = blog_key(), subject = subject, content = content, liked_by = [liked_by])
      p.put()
      # l = Likes(parent = likes_key(), post_id = p.key().id())
      # l.put()

      # "p.key().id() first gets the key for the post object, then it gets the id from the key"
      # ( key = KIND + ID) Kind here is Post.
      # "The kind is normally the name of the model class to which the entity belongs"
      self.redirect("/%s" % str(p.key().id()))
    else:
      error = "we need both a title and some text!"
      self.render("newpost.html", subject = subject, content = content, error = error)

# Handler for post's pages. Defines post's db key for URI. (?? Or maybe gets post_id from URI or both??)
class PostPage(BaseHandler):
# On GET, get function creates a new instance of itself and it retrieves
# the post_id from the URL. It then queries the entry key based on post_id
# and then it queries the post entry based on that key. Finally, it renders
# the post template with that post entry's data
  def get(self, post_id):
    if self.user:
      post_key = db.Key.from_path('Post', int(post_id), parent =blog_key())
      post = db.get(post_key)
      if not post:
        self.error(404)
        return
      like_key = db.Key.from_path('Likes', int(post_id), parent = likes_key())
      likes = db.get(like_key)
# likes = Likes.all().filter('post_id =', post_id).get()

      comments = db.GqlQuery("SELECT * FROM Comment ORDER BY last_modified DESC LIMIT 10")
    else:
      self.render("post.html", post = post, comments = comments, likes = likes, post_id = post_id)

# On POST, post function retrieves post_id from the URL then redirects
# to a new URI using that post id. The system then goes down to where app is
# definied to find the matching URI and corresponding handler (EditPost)
  def post(self, post_id, **value):
    if value:
       post_like = Likes(parent = users_key(), like = True, post_id = post_id )
       post_like.put()
    else:
       post_like = Likes(parent = users_key(), like = False, post_id = post_id)
       post_like.put()

    content = self.request.get("content")

    if content:
       add_comment = Comment(parent = blog_key(), content = content)
       add_comment.put()
    else:
       None

    self.redirect("/%s/edit" % post_id)

#Hashing functions
def hash_str(s):
  return haslib.md5(s).hexdigest()

def make_secure_val(val):
  return "%s | %s" % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
  val = secure_val.split('|')[0]
  if secure_val == make_secure_val(val):
    return val

#making and using salts
def make_salt():
    salt = random.sample(string.hexdigits,5)
    return string.join(salt,'')

def make_pw_hash(username, password, salt = None):
    if not salt:
      salt = make_salt()
    h = hashlib.sha256(username + password + salt).hexdigest()
    return "%s, %s" % (h, salt)

def valid_pw(name, pw, h):
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

# ?? I don't understand how this is saving users to the db?? <-- It doesn't
# The SignUp class is used to create the logic for validating the sign up page
# Below the Register class is-a SignUp class and Register is where users are written
# to the db
# ?? But i still don't quite understand self.username = self.request.get('username')
  def post(self):
    have_error = False
    self.username = self.request.get('username')
    self.password = self.request.get('password')
    self.verify = self.request.get('verify')
    self.email = self.request.get('email')

# This dictionary is used to re-populate the fields with the
# data given by the user when the form is returned due to errors
    params = dict(username = self.username, email = self.email)

    if not valid_username(self.username):
      params['error_username'] = "That's not a valid username."
      have_error = True

    if not valid_password(self.password):
      params['error_password'] = "That's not a valid password."
      have_error = True
    elif self.password != self.verify:
      params['error_verify'] = "Your passwords didn't match."
      have_error = True

    if not valid_email(self.email):
      params['error_email'] = "That's not a valid email."
      have_error = True

    if have_error:
      self.render('signup.html', **params)
    else:
      self.redirect('/welcome')

class EditPost(BaseHandler):
  def get(self, post_id):
    if self.user:
      key = db.Key.from_path('Post', int(post_id), parent =blog_key())
      post = db.get(key)

      if not post:
        self.error(404)
        return

      self.render("editpost.html", post = post)
    else:
      self.redirect("/signup")

  def post(self, post_id):
    key = db.Key.from_path('Post', int(post_id), parent =blog_key())
    post = db.get(key)
    post.subject = self.request.get("subject")
    post.content = self.request.get("content")

    if post.subject and post.content:
      post.put()
      self.redirect("/%s" % str(post.key().id()))
    else:
      error = "we need both a title and some text!"
      self.render("newpost.html", subject = subject, content = content, error = error)


# Register handler
class Register(SignUp):
  def done(self):
    #make sure the user doesn't already exist
# Find User with the by_name decorator
# ?? Does it need "self" + username because this is part of a class
# ?? and we need to specifiy/ reiterate that we're looking for the username
# ?? for this instance (/or this object?)

    u = User.by_name(self.username)
    if u:
      msg = "That user already exists."
      self.render('signup.html', error_username = msg)
# ?? Again, why use a decortaor here? Also again, why "self."...?
    else:
      u = User.register(self.username, self.password, self.email)
      u.put()

      self.login(u)
      self.redirect('/welcome')

# Blog welcome page after signup
class Welcome(BaseHandler):
  def get(self):
    if self.user:
      self.render('welcome.html')
    else:
      self.redirect('/signup')

#Login handler
class Login(BaseHandler):
  def get(self):
    self.render("login.html")

# ?? Why isn't this one self.username = self.request.get('username')
  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')

    u = User.login(username, password)
    if u:
      self.login(u)
      self.redirect('/welcome')

    else:
      login_error = "Invalid login"
      self.render("login.html", login_error = login_error)

#Logout handler
class Logout(BaseHandler):
  def get(self):
    self.logout()
    self.redirect('/signup')


class VoteUp(BaseHandler):
  def get(self, post_id):
    if self.user:
      self.render('welcome.html')
      like_q = Likes.all().filter('post_id =', post_id).get()
      likes = Likes(post_id = int(post_id), like_count = 1)
      likes.put()
      self.redirect("/%s" % post_id)
    else:
      self.redirect('/signup')
    # post_id = post_id
    # likeObj = Likes('post_id =', post_id)
    # likeObj.like_count


# class VoteUp(BaseHandler):
#   def get(self, post_id):
#     1. fetch the post by id #<a href='/voteup/123123'>Like</a>
#     2. fetch the likeObj by post_id
#     3. check if the logged in user is the author of the post
#     4. liked_by = likeObj.liked_by
#     5. for l in liked_by:
#           if l == self.user.key().id():
#             Dont allow
#             and return to postpage
#       liked_by.append(self.user.key().id())
#       likeObj.like_count+=1
#     redirect to postpage handler

# URI to Handler mapping
app = webapp2.WSGIApplication([
  ('/', Home),
  #('/newcomment', NewComment),
  ('/voteup/([0-9]+)', VoteUp),
  ('/newpost', NewPost ),
  ('/([0-9]+)', PostPage),
  ('/signup', Register),
  ('/welcome', Welcome),
  ('/login', Login),
  ('/logout', Logout),
  ('/([0-9]+)/edit', EditPost)
  ],
  debug=True)


