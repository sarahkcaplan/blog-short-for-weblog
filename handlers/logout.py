import blog-short-for-weblog.utils
from base import BaseHandler
from blog-short-for-weblog.models.user import User

# Logout handler
class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')