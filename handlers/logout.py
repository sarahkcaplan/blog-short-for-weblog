from utils import *
from base import BaseHandler
from models.user import User

# Logout handler
class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')