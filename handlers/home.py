from base import BaseHandler
from blog-short-for-weblog.models.user import User
from blog-short-for-weblog.models.post import Post

# Handler Home page
class Home(BaseHandler):
    def get(self):
        if self.user:
            posts = db.GqlQuery("""SELECT * FROM Post
                               ORDER BY last_modified DESC LIMIT 10""")
            self.render("home.html", posts=posts)

        else:
            self.redirect('/signup')