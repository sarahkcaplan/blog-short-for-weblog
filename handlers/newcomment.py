import utils
from base import BaseHandler

# Handler for adding a comment to a post.
class NewComment(BaseHandler):
    def get(self, post_id):
        if self.user:
            self.render('newcomment.html', post_id=post_id)

        else:
            self.redirect('/signup')

    def post(self, post_id):
        if self.user:
            content = self.request.get("content")

            if content:
                uid = int(self.read_secure_cookie('user_id'))
                user = User.by_id(uid)
                author = str(user.name)

                comment = Comments(parent=comment_key(), author=author,
                                   content=content, post_id=post_id)
                comment.put()
                comment_id = comment.key().id()

                self.redirect("/blog/%s/%s" % (post_id, comment_id))

            else:
                error = "Comment needs content"
                self.render('newcomment.html', error=error, post_id=post_id)
        else:
            self.redirect('/signup')