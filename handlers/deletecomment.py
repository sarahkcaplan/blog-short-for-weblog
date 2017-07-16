import utils
from base import BaseHandler

# Handler for deleteing a comment
class DeleteComment(BaseHandler):
    # Checks for author handled on post.html template
    def get(self, post_id, comment_id):
        comment = Comment.comment_query(comment_id)

        if self.user and self.user == comment.author:

            comment.delete()

            self.redirect("/blog/%s" % str(post_id))

        else:
            self.redirect('/signup')