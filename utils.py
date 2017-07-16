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

# Load templates and envoke Jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# Render templates
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


# Blog post formatting
def render_post(response, post):
    response.write('<b>' + post.subject + '</b><br>')
    response.write(post.content)


# Hashing functions
secret = "evernote"


def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


# Making and using salts for hashing passwords
def make_salt(length=5):
    return ''.join(random.SystemRandom().choice(string.ascii_letters)
                   for x in range(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s,%s" % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)