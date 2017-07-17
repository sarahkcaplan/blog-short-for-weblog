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

import utils
# from blog.handlers.base import BaseHandler
from blog.handlers.comment import CommentPage, DeleteComment, EditComment, NewComment
from blog.handlers.post import PostPage, NewPost, EditPost, DeletePost
from blog.handlers.home import Home
from blog.handlers.login import Login
from blog.handlers.logout import Logout
from blog.handlers.register import Register
from blog.handlers.signup import SignUp
from blog.handlers.vote import VoteUp, VoteDown
from blog.models.comments import Comments
from blog.models.post import Post
from blog.models.user import User

# URI to Handler mapping
app = webapp2.WSGIApplication([
  ('/signup', Register),
  ('/login', Login),
  ('/blog/', Home),
  ('/blog/newpost', NewPost),
  ('/blog/([0-9]+)', PostPage),
  ('/blog/([0-9]+)/editpost', EditPost),
  ('/blog/([0-9]+)/deletepost', DeletePost),
  ('/blog/([0-9]+)/newcomment', NewComment),
  ('/blog/([0-9]+)/([0-9]+)', CommentPage),
  ('/blog/([0-9]+)/([0-9]+)/editcomment', EditComment),
  ('/blog/([0-9]+)/([0-9]+)/deletecomment', DeleteComment),
  ('/blog/([0-9]+)/voteuppost', VoteUpPost),
  ('/blog/([0-9]+)/votedownpost', VoteDownPost),
  ('/logout', Logout)
  ],
  debug=True)