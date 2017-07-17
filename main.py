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

import blog-short-for-weblog.utils
from blog-short-for-weblog.handlers.base import BaseHandler
from blog-short-for-weblog.handlers.commentpage import CommentPage
from blog-short-for-weblog.handlers.deletecomment import DeleteComment
from blog-short-for-weblog.handlers.deletepost import DeletePost
from blog-short-for-weblog.handlers.editcomment import EditComment
from blog-short-for-weblog.handlers.editpost import EditPost
from blog-short-for-weblog.handlers.home import Home
from blog-short-for-weblog.handlers.login import Login
from blog-short-for-weblog.handlers.logout import Logout
from blog-short-for-weblog.handlers.newcomment import NewComment
from blog-short-for-weblog.handlers.newpost import NewPost
from blog-short-for-weblog.handlers.postpage import PostPage
from blog-short-for-weblog.handlers.register import Register
from blog-short-for-weblog.handlers.signup import SignUp
from blog-short-for-weblog.handlers.votedown import VoteDown
from blog-short-for-weblog.handlers.voteup import VoteUp
from blog-short-for-weblog.models.comments import Comments
from blog-short-for-weblog.models.post import Post
from blog-short-for-weblog.models.user import User

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