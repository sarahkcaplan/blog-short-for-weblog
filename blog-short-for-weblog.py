import os
import jinja2
import webapp2
import cgi
import re
import random
import string
import hashlib
import hmac

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

secret = "evernote"

def render_str(template, **params):
  t = jinja_env.get_template(template)
  return t.render(params)

## Commonly used functions
#Hashing functions
def hash_str(s):
  return haslib.md5(s).hexdigest()

def make_secure_val(val):
  return "%s|%s" % (val, hmac.new(secret,val).hexdigest())


def check_secure_val(secure_val):
  val = secure_val.split('|')[0]
  if secure_val == make_secure_val(val):
    return val


## Commonly used functions
# The class "BaseHandler" is-a "webapp2.RequestHandler"
# The class has eight functions definied within it

## Commonly used functions
class BaseHandler(webapp2.RequestHandler):

  def write(self, *a, **kw):
    self.response.write(*a, **kw)

  def render_str(self, template, **params):
    params['user'] = self.user
    return render_str(template, **params)

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

  def initialize(self, *a, **kw):
    webapp2.RequestHandler.initialize(self, *a, **kw)
    uid = self.read_secure_cookie('user_id')
    self.user = uid and User.by_id(int(uid))

#### Begin blog code

# Google Datastore entities for blog posts i.e. db tables
class Post(db.Model):
  author = db.StringProperty(required = True)
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now = True)
  liked_by = db.ListProperty(int)

  def render(self):
    self._render_text = self.content.replace('\n', '<br>')
    return render_str("post.html", p = self)

class Comments(db.Model):
  author = db.StringProperty(required = True)
  post_id = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  last_modified = db.DateTimeProperty(auto_now_add = True)

class User(db.Model):
  name = db.StringProperty(required = True)
  pw_hash = db.StringProperty(required = True)
  email = db.StringProperty(required = False)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now = True)

  @classmethod
  def by_id(cls, uid):
    return User.get_by_id(uid, parent = users_key())

# This returns the db entry for a user by name
  @classmethod
  def by_name(cls, name):
    u = cls.all().filter("name =", name).get()
    return u

  @classmethod
  def register(cls, name, pw, email = None):
    pw_hash = make_pw_hash(name, pw)
    return cls(parent = users_key(),
            name = name,
            pw_hash = pw_hash,
            email = email)

  @classmethod
  def login(cls, name, pw):
    u = cls.by_name(name)
    if u and valid_pw(name, pw, u.pw_hash):
      return u

def blog_key(name = 'default'):
  return db.Key.from_path('blogs', name)

def users_key(group = 'default'):
  return db.Key.from_path('users', group)

def likes_key(group = 'default'):
  return db.Key.from_path('likes', group)

def comment_key(group = 'default'):
  return db.Key.from_path('comment', group)

# Blog post formatting
def render_post(response, post):
  response.write('<b>' + post.subject + '</b><br>')
  response.write(post.content)

class Home(BaseHandler):
  def get(self):
    if self.user:
      posts = db.GqlQuery("SELECT * FROM Post ORDER BY last_modified DESC LIMIT 10")
      self.render("home.html", posts = posts)
    else:
      self.redirect('/signup')

# Page for creating new posts. Successful post redirects to post's permalink location.

class NewPost(BaseHandler):
  def get(self):
    if self.user:
      self.render("newpost.html")
    else:
      self.redirect('/signup')

  def post(self):
    subject = self.request.get("subject")
    content = self.request.get("content")
    uid = int(self.read_secure_cookie('user_id'))
    user = User.by_id(uid)
    author = str(user.name)

    if subject and content:
      # This is invoking a model class constructor using keyword arguments
      p = Post(parent = blog_key(), subject = subject, content = content, author = author, liked_by = [])
      p.put()

      self.redirect("/%s" % str(p.key().id()))
    else:
      error = "we need both a title and some text!"
      self.render("newpost.html", subject = subject, content = content, error = error)


# Handler for post's pages. Defines post's db key for URI. (?? Or maybe gets post_id from URI or both??)
class PostPage(BaseHandler):
  def get(self, post_id, comment_id = None):
    if self.user:
      post_key = db.Key.from_path('Post', int(post_id), parent =blog_key())
      post = db.get(post_key)

      uid = int(self.read_secure_cookie('user_id'))
      user = User.by_id(uid)
      current_user = str(user.name)

      if uid in post.liked_by:
        liking_user = uid
      else:
        liking_user = None

      if not post:
        self.error(404)
        return

      comment = Comments.all().order("-last_modified")
      comments = comment.filter("post_id =", post_id)

      likes_count = len(post.liked_by)

      self.render("post.html", liking_user = liking_user, current_user = current_user, post = post, likes_count = likes_count, comments = comments, post_id = post_id)

    else:
      self.redirect('/signup')

class NewComment(BaseHandler):
  def get(self, post_id):

    self.render('newcomment.html')

  def post(self, post_id):
    content = self.request.get("content")

    if content:
      uid = int(self.read_secure_cookie('user_id'))
      user = User.by_id(uid)
      author = str(user.name)

      comment = Comments(parent = comment_key(), author = author, content = content, post_id = post_id)
      comment.put()
      comment_id = comment.key().id()
      print "comment_id",comment_id

      self.redirect("/%s/%s" % (post_id, comment_id))

class Comment(BaseHandler):
  def get (self, post_id, comment_id):
    if self.user:
      c_key = db.Key.from_path('Comments', int(comment_id), parent= comment_key())
      comment = db.get(c_key)

      self.render("comment.html", comment = comment, post_id = post_id, comment_id = comment_id)


class EditComment(BaseHandler):
  def get(self, post_id, comment_id):
    if self.user:
      c_key = db.Key.from_path('Comments', int(comment_id), parent= comment_key())
      comment = db.get(c_key)
      content = comment.content

      self.render('editcomment.html', post_id = post_id, comment_id = comment_id, content = content)

  def post (self, post_id, comment_id):
    c_key = db.Key.from_path('Comments', int(comment_id), parent= comment_key())
    comment = db.get(c_key)
    comment.content = self.request.get("content")
    comment.put()

    self.redirect("/%s" % str(post_id))

class DeleteComment(BaseHandler):
  def get(self, post_id):
    content = self.request.get("content")
    comment = Comments.all().filter("post_id =", post_id)
    spec_comment = comment.filter("content =", content)
    del sepc_comment

    self.redirect("/%s" % str(post.key().id()))

#making and using salts
def make_salt(length = 5):
    return ''.join(random.SystemRandom().choice(string.ascii_letters) for x in range(length))

def make_pw_hash(name, pw, salt = None):
  if not salt:
    salt = make_salt()
  h = hashlib.sha256(name + pw + salt).hexdigest()
  return "%s,%s" % (salt,h)

def valid_pw(name, password, h):
  salt = h.split(',')[0]
  return h == make_pw_hash(name, password, salt)

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

  def post(self):
    have_error = False
    self.username = self.request.get('username')
    self.password = self.request.get('password')
    self.verify = self.request.get('verify')
    self.email = self.request.get('email')

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
      self.done()

# Register handler
class Register(SignUp):
  def done(self):
    u = User.by_name(self.username)
    if u:
      msg = "That user already exists."
      self.render('signup.html', error_username = msg)
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

class DeletePost(BaseHandler):
  def get(self, post_id):
    key = db.Key.from_path('Post', int(post_id), parent =blog_key())
    post = db.get(key)

    del post

    self.redirect('/')

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
      self.redirect('/signup')

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


class VoteUp(BaseHandler):
  def get(self, post_id):
    key = db.Key.from_path('Post', int(post_id), parent =blog_key())
    post = db.get(key)

    uid = int(self.read_secure_cookie('user_id'))

    post.liked_by += [uid]
    post.put()

    self.redirect("/%s" % str(post.key().id()))

class VoteDown(BaseHandler):
  def get(self, post_id):
    uid = int(self.read_secure_cookie('user_id'))

    key = db.Key.from_path('Post', int(post_id), parent =blog_key())
    post = db.get(key)

    liked_by_position = post.liked_by.index(uid)
    del post.liked_by[liked_by_position]

    post.put()

    self.redirect("/%s" % str(post.key().id()))

# URI to Handler mapping
app = webapp2.WSGIApplication([
  ('/', Home),
  ('/([0-9]+)/([0-9]+)', Comment),
  ('/([0-9]+)/newcomment', NewComment),
  ('/([0-9]+)/([0-9]+)/edit', EditComment),
  ('/comment/([0-9]+)/delete', DeleteComment),
  ('/voteup/([0-9]+)', VoteUp),
  ('/votedown/([0-9]+)', VoteDown),
  ('/newpost', NewPost ),
  ('/([0-9]+)', PostPage),
  ('/deletepost/([0-9]+)', DeletePost),
  ('/signup', Register),
  ('/welcome', Welcome),
  ('/login', Login),
  ('/logout', Logout),
  ('/([0-9]+)/edit', EditPost)
  ],
  debug=True)