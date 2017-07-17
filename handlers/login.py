import blog.utils
from base import BaseHandler
from blog.models.user import User

# Login handler
class Login(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)

        if u:
            self.login(u)
            self.redirect('/blog/')

        else:
            login_error = "Invalid login"
            self.render("login.html", login_error=login_error)