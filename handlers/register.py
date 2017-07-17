import blog-short-for-weblog.utils
from base import BaseHandler
from blog-short-for-weblog.models.user import User

# Register handler
class Register(SignUp):
    def done(self):
        u = User.by_name(self.username)

        if u:
            msg = "That user already exists."
            self.render('signup.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog/')