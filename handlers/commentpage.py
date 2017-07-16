import utils
from base import BaseHandler

# Handler for Comment's permalink page
class CommentPage(BaseHandler):
    def get(self, post_id, comment_id):
        if self.user:

            self.render("comment.html", comment=comment, post_id=post_id,
                        comment_id=comment_id)
        else:
            self.redirect('/signup')