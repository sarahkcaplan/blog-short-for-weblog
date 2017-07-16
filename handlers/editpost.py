import utils
from base import BaseHandler

# Handler for editing post
class EditPost(BaseHandler):
    # Checks for author handled on post.html template
    def get(self, post_id):
        post = Post.post_query(post_id)

        if self.user and self.user == post.author:
            self.render("editpost.html", post=post, post_id=post_id)

        else:
            self.redirect('/signup')

        if not post:
            self.error(404)
            return

    def post(self, post_id):
        post = Post.post_query(post_id)

        if self.user and self.user == post.author:
            subject = self.request.get("subject")
            content = self.request.get("content")

            if subject and content:
                post.subject = subject
                post.content = content
                post.put()
                self.redirect("/blog/%s" % str(post.key().id()))

            else:
                error = "We need both a title and some text"
                self.render("newpost.html", subject=subject, content=content,
                            error=error)
        else:
            self.redirect('/signup')

