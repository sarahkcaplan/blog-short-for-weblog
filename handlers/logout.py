import blog.utils
from base import BaseHandler
from blog.models.user import User

# Logout handler
class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')