import utils
from base import BaseHandler

# Page for creating new posts.
# Successful post redirects to post's permalink location.
class NewPost(BaseHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")

        else:
            self.redirect('/signup')

    def post(self):
        if self.user:
            subject = self.request.get("subject")
            content = self.request.get("content")
            uid = int(self.read_secure_cookie('user_id'))
            user = User.by_id(uid)
            author = str(user.name)

            if subject and content:
                # This is invoking a model class constructor
                p = Post(parent=blog_key(), subject=subject, content=content,
                         author=author, liked_by=[])
                p.put()

                self.redirect("/blog/%s" % str(p.key().id()))

            else:
                error = "We need both a title and some text"
                self.render("newpost.html", subject=subject,
                            content=content, error=error)

        else:
            self.redirect('/signup')