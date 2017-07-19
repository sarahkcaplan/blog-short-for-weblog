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

from handlers.utils import Utils
from handlers.base import BaseHandler
from handlers.comment import CommentPage, DeleteComment, EditComment, NewComment
from handlers.post import PostPage, NewPost, EditPost, DeletePost
from handlers.home import Home
from handlers.login import Login
from handlers.logout import Logout
from handlers.register import Register
from handlers.signup import SignUp
from handlers.vote import VoteUpPost, VoteDownPost
from models.comments import Comments
from models.post import Post
from models.user import User

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