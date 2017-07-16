import utils
from base import BaseHandler

# Logout handler
class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')